/**
 * File: pages/order/list/list.js
 * Description: 订单列表页 — 查看历史订单、取消订单、再次购买
 */

Page({
  data: {
    orders: [],
    filteredOrders: [],
    statusFilter: 'all'
  },

  onShow() {
    this.loadOrders()
  },

  onLoad(options) {
    if (options.newOrder) {
      // 从结算页跳转过来，定位到新订单
      this.setData({ statusFilter: 'all' })
    }
  },

  loadOrders() {
    const orders = wx.getStorageSync('orders') || []
    this.setData({ orders })
    this.filterOrders()
  },

  filterOrders() {
    const { orders, statusFilter } = this.data
    if (statusFilter === 'all') {
      this.setData({ filteredOrders: orders })
    } else {
      this.setData({
        filteredOrders: orders.filter(o => o.status === statusFilter)
      })
    }
  },

  onSwitchFilter(e) {
    const status = e.currentTarget.dataset.status
    this.setData({ statusFilter: status })
    this.filterOrders()
  },

  statusText(status) {
    const map = {
      pending: '⏳ 待处理',
      confirmed: '✅ 已确认',
      completed: '✓ 已完成',
      cancelled: '已取消'
    }
    return map[status] || status
  },

  onCancelOrder(e) {
    const orderNo = e.currentTarget.dataset.order
    wx.showModal({
      title: '取消订单',
      content: '确定要取消该订单吗？',
      success: (res) => {
        if (res.confirm) {
          const orders = this.data.orders.map(o => {
            if (o.orderNo === orderNo) {
              return { ...o, status: 'cancelled' }
            }
            return o
          })
          wx.setStorageSync('orders', orders)
          this.setData({ orders })
          this.filterOrders()
          wx.showToast({ title: '订单已取消', icon: 'success' })
        }
      }
    })
  },

  onReorder(e) {
    const items = e.currentTarget.dataset.items
    // 将商品加入购物车
    let cart = wx.getStorageSync('cart') || []
    items.forEach(item => {
      const existIdx = cart.findIndex(
        c => c.goodsId === item.goodsId && c.spec === (item.spec || '')
      )
      if (existIdx > -1) {
        cart[existIdx].quantity += item.quantity
      } else {
        cart.push({
          goodsId: item.goodsId,
          name: item.name,
          price: item.price,
          spec: item.spec || '',
          image: item.image,
          quantity: item.quantity,
          stock: 999
        })
      }
    })
    wx.setStorageSync('cart', cart)

    // 更新角标
    const count = cart.reduce((s, i) => s + i.quantity, 0)
    wx.setTabBarBadge({ index: 1, text: String(count) })

    // 跳转到购物车
    wx.switchTab({ url: '/pages/cart/index' })
  }
})
