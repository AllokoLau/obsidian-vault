/**
 * File: utils/util.js
 * Description: 通用工具函数
 */

/**
 * 格式化金额（保留2位小数）
 */
const formatPrice = (price) => {
  return Number(price).toFixed(2)
}

/**
 * 生成订单号
 */
const generateOrderNo = () => {
  const now = new Date()
  const date = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
  const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
  return `ORD${date}${random}`
}

/**
 * 获取当前时间 ISO 字符串
 */
const getNow = () => new Date().toISOString()

/**
 * 节流函数
 */
const throttle = (fn, delay = 300) => {
  let last = 0
  return function (...args) {
    const now = Date.now()
    if (now - last >= delay) {
      last = now
      fn.apply(this, args)
    }
  }
}

module.exports = {
  formatPrice,
  generateOrderNo,
  getNow,
  throttle
}
