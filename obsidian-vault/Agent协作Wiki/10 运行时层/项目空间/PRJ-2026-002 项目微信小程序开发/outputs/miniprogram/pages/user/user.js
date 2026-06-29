/**
 * File: pages/user/user.js
 * Description: "我的"页面 — 用户信息、订单统计、功能入口
 */

Page({
  data: {
    avatarUrl: '',
    nickName: '',
    orderCount: { all: 0, pending: 0, completed: 0, cancelled: 0 }
  },

  onShow() {
    this.loadUserInfo()
    this.loadOrderStats()
  },

  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({
        avatarUrl: userInfo.avatarUrl || '',
        nickName: userInfo.nickName || ''
      })
    }
  },

  loadOrderStats() {
    const orders = wx.getStorageSync('orders') || []
    const count = { all: orders.length, pending: 0, completed: 0, cancelled: 0 }
    orders.forEach(o => {
      if (count[o.status] !== undefined) count[o.status]++
    })
    this.setData({ orderCount: count })
  },

  onGetUserInfo() {
    // 获取微信用户信息（仅展示用，不涉及敏感权限）
    if (this.data.nickName) return // 已登录

    wx.getUserProfile({
      desc: '用于展示用户信息',
      success: (res) => {
        const { avatarUrl, nickName } = res.userInfo
        wx.setStorageSync('userInfo', { avatarUrl, nickName })
        this.setData({ avatarUrl, nickName })
      },
      fail: () => {
        // 用户拒绝授权，使用默认昵称
        const fallback = '微信用户'
        wx.setStorageSync('userInfo', { avatarUrl: '', nickName: fallback })
        this.setData({ nickName: fallback })
      }
    })
  },

  goToOrders(e) {
    const status = e.currentTarget.dataset.status
    // 切换到订单Tab，并传状态参数
    wx.switchTab({ url: '/pages/order/list' })
  },

  onClearData() {
    wx.showModal({
      title: '清除数据',
      content: '确定要清除所有本地数据（订单、购物车、用户信息）吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync()
          this.setData({
            avatarUrl: '',
            nickName: '',
            orderCount: { all: 0, pending: 0, completed: 0, cancelled: 0 }
          })
          wx.removeTabBarBadge({ index: 1 })
          wx.showToast({ title: '已清除', icon: 'success' })
        }
      }
    })
  }
})
