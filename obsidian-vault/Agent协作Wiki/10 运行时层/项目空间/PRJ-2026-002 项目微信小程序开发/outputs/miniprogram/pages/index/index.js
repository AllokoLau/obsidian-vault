/**
 * File: pages/index/index.js
 * Description: 首页 - 商品列表
 */

// 模拟商品数据（后续迁移到云数据库）
const MOCK_GOODS = [
  {
    _id: 'g001', name: '经典牛肉汉堡套餐', price: 32.90,
    image: '', tag: '热销', tagType: 'hot',
    category: '主食', stock: 100
  },
  {
    _id: 'g002', name: '招牌鸡肉沙拉', price: 26.00,
    image: '', tag: '', tagType: '',
    category: '主食', stock: 50
  },
  {
    _id: 'g003', name: '冰美式咖啡（大杯）', price: 18.00,
    image: '', tag: '新品', tagType: 'new',
    category: '饮品', stock: 200
  },
  {
    _id: 'g004', name: '炸薯条（大份）', price: 12.90,
    image: '', tag: '', tagType: '',
    category: '小食', stock: 150
  },
  {
    _id: 'g005', name: '抹茶拿铁', price: 22.00,
    image: '', tag: '', tagType: '',
    category: '饮品', stock: 80
  },
  {
    _id: 'g006', name: '提拉米苏', price: 28.00,
    image: '', tag: '招牌', tagType: 'hot',
    category: '甜品', stock: 30
  }
]

Page({
  data: {
    goodsList: [],
    categories: ['全部', '主食', '小食', '饮品', '甜品'],
    currentCat: 0,
    allGoods: []
  },

  onLoad() {
    this.setData({
      allGoods: MOCK_GOODS,
      goodsList: MOCK_GOODS
    })
  },

  onShow() {
    // 每次显示时刷新购物车角标
    this.updateCartBadge()
  },

  onSwitchCategory(e) {
    const idx = e.currentTarget.dataset.index
    const cat = this.data.categories[idx]
    let filtered = this.data.allGoods

    if (idx !== 0) {
      filtered = this.data.allGoods.filter(g => g.category === cat)
    }

    this.setData({
      currentCat: idx,
      goodsList: filtered
    })
  },

  onGoDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/goods/detail?id=${id}`
    })
  },

  updateCartBadge() {
    // 从本地缓存获取购物车数据
    const cart = wx.getStorageSync('cart') || []
    const count = cart.reduce((sum, item) => sum + item.quantity, 0)
    if (count > 0) {
      wx.setTabBarBadge({ index: 1, text: String(count) })
    } else {
      wx.removeTabBarBadge({ index: 1 })
    }
  }
})
