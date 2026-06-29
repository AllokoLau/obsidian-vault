/**
 * 云函数: createOrder v2
 * 功能: 创建订单（安全加固版本）
 * 变更说明:
 *   v1 - 接收客户端 price，无事务，前端生成订单
 *   v2 - 仅接收 goodsId+quantity，服务端定价，事务原子操作
 *
 * 安全措施:
 *   1. 事务保证订单写入+库存扣减原子性
 *   2. 服务端从数据库读取价格（不信任客户端传价）
 *   3. 参数白名单校验（类型、格式、范围）
 *   4. 订单快照保存（商品信息写入时固定，不受后续修改影响）
 */

const cloud = require('wx-server-sdk')
cloud.init()
const db = cloud.database()
const _ = db.command

/**
 * 验证 goodsId 是否为合法的 MongoDB ObjectId 格式
 * 微信云数据库 _id 为 24 位十六进制字符串
 */
const isValidId = (id) => /^[a-f\d]{24}$/i.test(id)

/**
 * 验证数量是否在合法范围内
 */
const isValidQuantity = (q) => Number.isInteger(q) && q > 0 && q <= 99

/**
 * 生成唯一订单号
 * 格式: ORD + yyyyMMdd + 6位随机数 + openid后4位
 * 示例: ORD20260625123456abcd
 */
const generateOrderNo = (openid) => {
  const now = new Date()
  const date = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
  const random = String(Math.floor(Math.random() * 1000000)).padStart(6, '0')
  const suffix = (openid || '').slice(-4)
  return `ORD${date}${random}${suffix}`
}

/**
 * 验证 remark 长度（防止提交过长数据）
 */
const isValidRemark = (remark) => {
  if (!remark) return true
  return typeof remark === 'string' && remark.length <= 200
}

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const _openid = wxContext.OPENID

  if (!_openid) {
    return { code: -401, msg: '用户未登录' }
  }

  // ============================================
  // 阶段1：参数校验
  // ============================================

  const { goodsList, remark } = event

  // 1.1 验证 goodsList
  if (!Array.isArray(goodsList) || goodsList.length === 0) {
    return { code: -1, msg: '商品列表不能为空' }
  }

  if (goodsList.length > 20) {
    return { code: -1, msg: '单次最多下单20件商品' }
  }

  // 1.2 逐项校验
  for (const item of goodsList) {
    if (!isValidId(item.goodsId)) {
      return { code: -2, msg: `商品ID格式无效: ${item.goodsId || ''}` }
    }
    if (!isValidQuantity(item.quantity)) {
      return { code: -2, msg: `商品数量无效: ${item.quantity}（需为1-99的整数）` }
    }
    if (item.spec && typeof item.spec !== 'string') {
      return { code: -2, msg: '规格参数格式无效' }
    }
  }

  // 1.3 验证 remark
  if (!isValidRemark(remark)) {
    return { code: -2, msg: '备注不能超过200个字符' }
  }

  // ============================================
  // 阶段2：服务端读取商品信息 + 校验库存
  // ============================================

  const resolvedItems = []

  try {
    for (const item of goodsList) {
      const res = await db.collection('goods').doc(item.goodsId).get()
      if (!res.data) {
        return { code: -3, msg: `商品不存在: ${item.goodsId}` }
      }

      const goods = res.data

      // 检查商品状态
      if (goods.status !== 'on') {
        return { code: -3, msg: `${goods.name} 已下架` }
      }

      // 检查库存
      if (goods.stock < item.quantity) {
        return { code: -3, msg: `${goods.name} 库存不足（剩余 ${goods.stock}）` }
      }

      // 服务端组装订单项（以数据库中的价格为准）
      resolvedItems.push({
        goodsId: item.goodsId,
        name: goods.name,           // 商品名快照
        price: goods.price,         // 价格以数据库为准 [安全:防客户端篡改]
        quantity: item.quantity,
        image: goods.image || '',
        spec: item.spec || ''
      })
    }
  } catch (err) {
    console.error('[createOrder] 读取商品失败:', err)
    return { code: -5, msg: '读取商品信息失败' }
  }

  // ============================================
  // 阶段3：事务 — 订单写入 + 库存扣减（原子操作）
  // ============================================

  const orderNo = generateOrderNo(_openid)
  const totalAmount = resolvedItems.reduce((sum, i) => sum + i.price * i.quantity, 0)
  const now = new Date().toISOString()

  const orderData = {
    orderNo,
    _openid,
    items: resolvedItems,
    totalAmount,
    status: 'pending',
    remark: (remark || '').trim(),
    createTime: now,
    updateTime: now
  }

  const transaction = await db.startTransaction()

  try {
    // 3.1 写入订单
    const orderRes = await transaction.collection('orders').add({ data: orderData })
    if (!orderRes._id) {
      throw new Error('订单写入失败')
    }

    // 3.2 逐项扣减库存（在事务中再次校验库存，防止并发超卖）
    for (const item of goodsList) {
      const stockRes = await transaction.collection('goods').doc(item.goodsId).get()
      if (!stockRes.data) {
        throw new Error(`商品 ${item.goodsId} 已不存在`)
      }
      if (stockRes.data.stock < item.quantity) {
        throw new Error(`${stockRes.data.name} 库存不足（剩余 ${stockRes.data.stock}）`)
      }

      await transaction.collection('goods').doc(item.goodsId).update({
        data: {
          stock: _.inc(-item.quantity),
          updateTime: now
        }
      })
    }

    // 3.3 提交事务
    await transaction.commit()

    return {
      code: 0,
      msg: '下单成功',
      data: {
        orderNo,
        totalAmount,
        orderId: orderRes._id
      }
    }
  } catch (err) {
    // 回滚事务
    await transaction.rollback().catch(e => console.error('[createOrder] 回滚失败:', e))

    console.error('[createOrder] 事务失败:', err.message)
    return { code: -4, msg: err.message || '下单失败，请稍后重试' }
  }
}
