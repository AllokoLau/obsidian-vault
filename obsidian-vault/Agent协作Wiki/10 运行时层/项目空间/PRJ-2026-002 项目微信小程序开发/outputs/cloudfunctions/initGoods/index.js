/**
 * 云函数: initGoods v2
 * 功能: 初始化商品数据到云数据库（仅管理员可调用）
 * 变更说明:
 *   v1 - 无权限控制，任意用户可调用
 *   v2 - 添加管理员 openid 白名单校验
 *
 * 安全措施:
 *   1. 管理员 openid 白名单校验 [安全:权限控制]
 *   2. 初始化后自动标记数据来源，便于审计
 */

const cloud = require('wx-server-sdk')
cloud.init()
const db = cloud.database()

/**
 * 管理员 OpenID 白名单
 * 部署前将你的微信 openid 填入此处
 * 获取方式: 在云函数中调用 cloud.getWXContext().OPENID 打印到日志
 */
const ADMIN_OPENIDS = [
  '管理员openid_请替换'  // TODO: 部署前替换为真实 openid
]

const INITIAL_GOODS = [
  {
    name: '经典牛肉汉堡套餐', price: 32.90,
    image: '', tag: '热销', tagType: 'hot',
    category: '主食', stock: 100, soldCount: 236,
    description: '选用澳洲进口牛肉饼，搭配新鲜生菜、番茄片、车打芝士，配以秘制酱料。套餐含中份薯条 + 可乐一杯。'
  },
  {
    name: '招牌鸡肉沙拉', price: 26.00,
    image: '', tag: '', tagType: '',
    category: '主食', stock: 50, soldCount: 128,
    description: '新鲜混合生菜、烤鸡胸肉、樱桃番茄、水煮蛋、凯撒酱。低卡健康之选。'
  },
  {
    name: '冰美式咖啡（大杯）', price: 18.00,
    image: '', tag: '新品', tagType: 'new',
    category: '饮品', stock: 200, soldCount: 312,
    description: '精选阿拉比卡咖啡豆，每日新鲜萃取。大杯 500ml，可选少冰/去冰。'
  },
  {
    name: '炸薯条（大份）', price: 12.90,
    image: '', tag: '', tagType: '',
    category: '小食', stock: 150, soldCount: 89,
    description: '选用优质土豆，现炸至金黄酥脆。大份约 200g。'
  },
  {
    name: '抹茶拿铁', price: 22.00,
    image: '', tag: '', tagType: '',
    category: '饮品', stock: 80, soldCount: 45,
    description: '日式抹茶搭配鲜牛奶，可选冷/热饮。'
  },
  {
    name: '提拉米苏', price: 28.00,
    image: '', tag: '招牌', tagType: 'hot',
    category: '甜品', stock: 30, soldCount: 67,
    description: '经典意式提拉米苏，采用马斯卡彭芝士，每日手工制作。'
  }
]

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const _openid = wxContext.OPENID

  // ============================================
  // 管理员权限校验 [安全:防止未授权调用]
  // ============================================

  if (!ADMIN_OPENIDS.includes(_openid)) {
    console.warn(`[initGoods] 未授权访问: ${_openid}`)
    return { code: -403, msg: '无权限，仅管理员可初始化商品数据' }
  }

  try {
    // 检查是否已有数据
    const countRes = await db.collection('goods').count()
    if (countRes.total > 0) {
      return {
        code: -1,
        msg: `已有 ${countRes.total} 条商品数据，跳过初始化`,
        data: { existCount: countRes.total }
      }
    }

    // 批量写入，附带初始化标记
    const now = new Date().toISOString()
    const tasks = INITIAL_GOODS.map(goods => {
      return db.collection('goods').add({
        data: {
          ...goods,
          status: 'on',
          createTime: now,
          updateTime: now,
          _createdBy: 'initGoods'   // 数据来源标记 [安全:审计追踪]
        }
      })
    })

    const results = await Promise.all(tasks)
    const created = results.filter(r => r._id).length

    return {
      code: 0,
      msg: `成功初始化 ${created}/${INITIAL_GOODS.length} 条商品数据`
    }
  } catch (err) {
    console.error('[initGoods] 初始化失败:', err)
    return { code: -2, msg: '初始化失败: ' + err.message }
  }
}
