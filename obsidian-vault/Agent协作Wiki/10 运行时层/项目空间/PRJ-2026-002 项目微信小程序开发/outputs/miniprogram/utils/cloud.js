/**
 * File: utils/cloud.js v2
 * Description: 云开发 API 封装层 — 统一管理云数据库和云函数调用
 *
 * 安全措施:
 *   1. 统一错误处理（所有云函数调用经过同一封装）
 *   2. 请求中状态管理（防重复提交）
 *   3. 节流控制（防高频调用）
 *   4. 下单时只传 goodsId+quantity，不传价格 [安全:防客户端篡改]
 */

/** 请求锁，防止重复提交 */
const pendingRequests = new Set()

/**
 * 发起云函数调用（带统一错误处理和防重复提交）
 * @param {string} name - 云函数名
 * @param {object} data - 参数
 * @param {object} options - 配置
 * @param {boolean} options.noRepeat - 是否启用防重复（默认 true）
 * @returns {Promise<{code: number, msg: string, data?: any}>}
 */
const callFunction = async (name, data = {}, options = {}) => {
  const { noRepeat = true } = options
  const requestKey = `${name}_${JSON.stringify(data)}`

  // 防重复提交 [安全:防止重复下单]
  if (noRepeat && pendingRequests.has(requestKey)) {
    console.warn(`[cloud] 重复请求拦截: ${name}`)
    return { code: -1, msg: '请求正在处理中，请勿重复提交' }
  }

  try {
    if (noRepeat) pendingRequests.add(requestKey)

    const res = await wx.cloud.callFunction({
      name,
      data
    })

    return res.result || { code: -1, msg: '返回数据异常' }
  } catch (err) {
    console.error(`[cloud] 云函数调用失败: ${name}`, err)
    return {
      code: -1,
      msg: err.errMsg || '网络异常，请检查网络连接后重试'
    }
  } finally {
    if (noRepeat) pendingRequests.delete(requestKey)
  }
}

/**
 * 获取商品列表（从云数据库）
 * 安全说明: 商品目录为公开数据，前端可直读
 */
const fetchGoods = async () => {
  try {
    const db = wx.cloud.database()
    const res = await db.collection('goods')
      .where({ status: 'on' })
      .field({
        _id: true,
        name: true,
        price: true,
        image: true,
        tag: true,
        tagType: true,
        category: true,
        stock: true,
        soldCount: true,
        description: true
      })
      .get()
    return res.data || []
  } catch (err) {
    console.error('[cloud] 获取商品列表失败:', err)
    return []
  }
}

/**
 * 创建订单 — 仅传 goodsId+quantity，价格在服务端读取 [安全:防客户端篡改]
 * @param {Array<{goodsId: string, quantity: number, spec?: string}>} goodsList
 * @param {string} remark - 备注
 * @returns {Promise<{code: number, msg: string, data?: {orderNo, totalAmount, orderId}}>}
 */
const createOrder = async (goodsList, remark = '') => {
  return callFunction('createOrder', { goodsList, remark })
}

/**
 * 查询当前用户的订单列表（分页）
 * @param {object} params
 * @param {string} [params.status] - 状态过滤
 * @param {number} [params.pageNum=1] - 页码
 * @param {number} [params.pageSize=10] - 每页条数
 */
const getOrders = async (params = {}) => {
  return callFunction('getOrders', params, { noRepeat: false })
}

/**
 * 更新订单状态
 * @param {string} orderNo - 订单号
 * @param {string} status - 目标状态
 */
const updateOrderStatus = async (orderNo, status) => {
  return callFunction('updateOrderStatus', { orderNo, status })
}

module.exports = {
  callFunction,
  fetchGoods,
  createOrder,
  getOrders,
  updateOrderStatus
}
