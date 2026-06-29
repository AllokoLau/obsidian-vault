/**
 * File: pages/cart/cart.js
 * Description: 购物车页 — 管理已选商品、调整数量、去结算
 */

Page({
  data: {
    cartItems: [],
    allSelected: true,
    selectedCount: 0,
    totalAmount: '0.00'
  },

  onShow() {
    this.loadCart()
  },

  loadCart() {
    const cart = wx.getStorageSync('cart') || []
    const items = cart.map(item => ({
      ...item,
      selected: item.selected !== false // 默认选中
    }))
    wx.setStorageSync('cart', items)
    this.setData({ cartItems: items })
    this.calcTotal()
  },

  calcTotal() {
    const items = this.data.cartItems
    const selected = items.filter(i => i.selected)
    const allSelected = items.length > 0 && items.every(i => i.selected)
    const total = selected.reduce((s, i) => s + i.price * i.quantity, 0)

    this.setData({
      allSelected,
      selectedCount: selected.reduce((s, i) => s + i.quantity, 0),
      totalAmount: total.toFixed(2)
    })
  },

  onToggleSelect(e) {
    const idx = e.currentTarget.dataset.index
    const items = this.data.cartItems
    items[idx].selected = !items[idx].selected
    wx.setStorageSync('cart', items)
    this.setData({ cartItems: items })
    this.calcTotal()
  },

  onToggleAll() {
    const newState = !this.data.allSelected
    const items = this.data.cartItems.map(i => ({ ...i, selected: newState }))
    wx.setStorageSync('cart', items)
    this.setData({ cartItems: items })
    this.calcTotal()
  },

  onDecrease(e) {
    const idx = e.currentTarget.dataset.index
    const items = this.data.cartItems
    if (items[idx].quantity <= 1) {
      // 数量为1时删除
      wx.showModal({
        title: '提示',
        content: '确定要移除该商品吗？',
        success: (res) => {
          if (res.confirm) {
            items.splice(idx, 1)
            wx.setStorageSync('cart', items)
            this.setData({ cartItems: items })
            this.calcTotal()
            this.updateBadge()
          }
        }
      })
      return
    }
    items[idx].quantity -= 1
    wx.setStorageSync('cart', items)
    this.setData({ cartItems: items })
    this.calcTotal()
    this.updateBadge()
  },

  onIncrease(e) {
    const idx = e.currentTarget.dataset.index
    const items = this.data.cartItems
    if (items[idx].quantity >= items[idx].stock) {
      wx.showToast({ title: '已达库存上限', icon: 'none' })
      return
    }
    items[idx].quantity += 1
    wx.setStorageSync('cart', items)
    this.setData({ cartItems: items })
    this.calcTotal()
    this.updateBadge()
  },

  onCheckout() {
    const selected = this.data.cartItems.filter(i => i.selected)
    if (selected.length === 0) return

    // 将选中的商品传给结算页
    wx.setStorageSync('checkoutItems', selected)
    wx.navigateTo({ url: '/pages/order/checkout' })
  },

  updateBadge() {
    const cart = wx.getStorageSync('cart') || []
    const count = cart.reduce((s, i) => s + i.quantity, 0)
    if (count > 0) {
      wx.setTabBarBadge({ index: 1, text: String(count) })
    } else {
      wx.removeTabBarBadge({ index: 1 })
    }
  }
})
