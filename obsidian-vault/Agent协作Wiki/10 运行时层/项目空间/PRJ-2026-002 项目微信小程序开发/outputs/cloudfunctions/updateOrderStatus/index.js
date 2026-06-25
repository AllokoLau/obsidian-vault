/**
 * 云函数: updateOrderStatus v2
 * 功能: 更新订单状态（安全加固版本）
 * 变更说明:
 *   v1 - 白名单校验 status，但允许任意跳级变更
 *   v2 - 状态机约束，禁止跳级，记录状态变更时间
 *
 * 安全措施:
 *   1. 状态机流转规则（禁止跳级）
 *   2. 校验订单归属（只能操作自己的订单）
 *   3. orderNo 格式校验
 *   4. 记录 updateTime
 *
 * 状态流转规则:
 *   pending ──→ confirmed ──→ completed
 *       │                        ↑
 *       └──→ cancelled ──────────┘
 *
 *   pending    → confirmed（商家/系统确认）
 *   pending    → cancelled（用户取消）
 *   confirmed  → completed（完成）
 *   confirmed  → cancelled（取消确认的订单，如退款）
 *   completed  → （终态，不可变更）
 *   cancelled  → （终态，不可变更）
 */

const cloud = require('wx-server-sdk')
cloud.init()
const db = cloud.database()

/**
 * 订单状态机：定义每种状态可流转到的下一状态
 * key = 当前状态, value = 允许流转到的状态列表
 */
const STATE_MACHINE = {
  'pending':    ['confirmed', 'cancelled'],
  'confirmed':  ['completed', 'cancelled'],
  'completed':  [],       // 终态
  'cancelled':  []        // 终态
}

/**
 * 验证 orderNo 格式
 * 格式: ORD + 8位日期 + 6-10位随机/标识字符
 */
const isValidOrderNo = (no) => /^ORD\d{8}[a-f\d]{10,14}$/i.test(no)

/**
 * 检查状态流转是否合法
 */
const isValidTransition = (currentStatus, newStatus) => {
  const allowed = STATE_MACHINE[currentStatus]
  return allowed && allowed.includes(newStatus)
}

exports.main = async (event, context) => {
  const { orderNo, status } = event
  const wxContext = cloud.getWXContext()

  // ============================================
  // 参数校验
  // ============================================

  if (!orderNo || !status) {
    return { code: -1, msg: '参数不完整' }
  }

  // orderNo 格式校验
  if (!isValidOrderNo(orderNo)) {
    return { code: -1, msg: '订单号格式无效' }
  }

  // status 白名单校验
  const validStatuses = Object.keys(STATE_MACHINE)
  if (!validStatuses.includes(status)) {
    return { code: -2, msg: '无效的订单状态' }
  }

  try {
    // ============================================
    // 读取当前订单状态
    // ============================================

    const res = await db.collection('orders')
      .where({
        orderNo,
        _openid: wxContext.OPENID  // 只能操作自己的订单 [安全:水平越权防护]
      })
      .field({
        status: true,
        _id: true
      })
      .get()

    if (res.data.length === 0) {
      return { code: -3, msg: '订单不存在或无权操作' }
    }

    const currentStatus = res.data[0].status
    const orderId = res.data[0]._id

    // ============================================
    // 状态机校验
    // ============================================

    // 检查是否已是终态
    if (STATE_MACHINE[currentStatus].length === 0) {
      return { code: -4, msg: `订单已是 ${currentStatus} 状态，不可变更` }
    }

    // 不能变更为相同状态
    if (currentStatus === status) {
      return { code: 0, msg: '状态未变化' }
    }

    // 检查流转合法性
    if (!isValidTransition(currentStatus, status)) {
      return {
        code: -4,
        msg: `不允许从 ${currentStatus} 流转到 ${status}`
      }
    }

    // ============================================
    // 更新状态
    // ============================================

    const now = new Date().toISOString()
    await db.collection('orders').doc(orderId).update({
      data: {
        status,
        updateTime: now
      }
    })

    return {
      code: 0,
      msg: '状态更新成功',
      data: {
        orderNo,
        fromStatus: currentStatus,
        toStatus: status,
        updateTime: now
      }
    }
  } catch (err) {
    console.error('[updateOrderStatus] 更新失败:', err)
    return { code: -5, msg: '更新失败，请稍后重试' }
  }
}
