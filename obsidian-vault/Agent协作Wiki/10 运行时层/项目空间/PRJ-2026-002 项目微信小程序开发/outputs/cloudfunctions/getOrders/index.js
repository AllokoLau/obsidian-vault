/**
 * 云函数: getOrders v2
 * 功能: 查询当前用户的订单列表（安全加固版本）
 * 变更说明:
 *   v1 - 无条件查询全部订单
 *   v2 - 分页查询 + 字段限制 + 状态过滤器白名单
 *
 * 安全措施:
 *   1. 分页限制（防止一次拉取过多数据）
 *   2. 每页上限 20 条
 *   3. 状态过滤器白名单（防止 NoSQL 注入）
 *   4. 仅返回必要字段
 *   5. 仅查询用户自己的订单
 */

const cloud = require('wx-server-sdk')
cloud.init()
const db = cloud.database()
const _ = db.command

/** 每页最大条数 */
const MAX_PAGE_SIZE = 20
/** 默认每页条数 */
const DEFAULT_PAGE_SIZE = 10
/** 合法状态过滤器 */
const VALID_STATUSES = ['pending', 'confirmed', 'completed', 'cancelled']

/**
 * 分页参数校验：pageNum 从 1 开始
 */
const normalizePageParam = (val, min, max, defaultVal) => {
  const num = Number(val)
  if (Number.isInteger(num) && num >= min && num <= max) return num
  return defaultVal
}

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()

  // ============================================
  // 参数校验与归一化
  // ============================================

  // 分页参数
  const pageNum = normalizePageParam(event.pageNum, 1, 100, 1)
  const pageSize = normalizePageParam(event.pageSize, 1, MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE)

  // 状态过滤器
  const statusFilter = event.status
  const hasStatusFilter = statusFilter && statusFilter !== 'all' && VALID_STATUSES.includes(statusFilter)

  try {
    // ============================================
    // 构建查询条件
    // ============================================

    // 基础条件：仅查询用户自己的订单 [安全:水平越权防护]
    const queryCondition = { _openid: wxContext.OPENID }

    // 仅状态过滤器的值在白名单中时，才加入查询条件 [安全:防NoSQL注入]
    if (hasStatusFilter) {
      queryCondition.status = statusFilter
    }

    // ============================================
    // 先获取总数（用于前端分页展示）
    // ============================================

    const countRes = await db.collection('orders')
      .where(queryCondition)
      .count()
    const total = countRes.total

    // ============================================
    // 分页查询（跳过的条数 = (页码-1) * 每页条数）
    // ============================================

    const skip = (pageNum - 1) * pageSize

    const res = await db.collection('orders')
      .where(queryCondition)
      .orderBy('createTime', 'desc')
      .skip(skip)
      .limit(pageSize)
      .field({
        _id: true,
        orderNo: true,
        totalAmount: true,
        status: true,
        items: true,
        remark: true,
        createTime: true,
        updateTime: true
        // _openid 不返回（前端不需要）
      })
      .get()

    return {
      code: 0,
      data: {
        list: res.data,
        total,
        pageNum,
        pageSize,
        hasMore: skip + pageSize < total
      }
    }
  } catch (err) {
    console.error('[getOrders] 查询失败:', err)
    return { code: -1, msg: '查询失败，请稍后重试' }
  }
}
