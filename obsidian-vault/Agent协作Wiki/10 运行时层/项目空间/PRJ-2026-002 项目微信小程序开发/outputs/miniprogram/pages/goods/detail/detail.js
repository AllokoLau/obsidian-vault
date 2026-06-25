/**
 * File: pages/goods/detail/detail.js
 * Description: 商品详情页 — 展示商品信息、加入购物车
 */

const MOCK_GOODS = {
  'g001': {
    _id: 'g001', name: '经典牛肉汉堡套餐', price: 32.90, originalPrice: 39.00,
    image: '', tag: '热销',
    description: '选用澳洲进口牛肉饼，搭配新鲜生菜、番茄片、车打芝士，配以秘制酱料。套餐含中份薯条 + 可乐一杯。',
    category: '主食', stock: 100, soldCount: 236,
    specs: [
      { name: '标准份', priceAdd: 0 },
      { name: '大份', priceAdd: 5.00 }
    ]
  },
  'g002': {
    _id: 'g002', name: '招牌鸡肉沙拉', price: 26.00, originalPrice: 0,
    image: '', tag: '',
    description: '新鲜混合生菜、烤鸡胸肉、樱桃番茄、水煮蛋、凯撒酱。低卡健康之选。',
    category: '主食', stock: 50, soldCount: 128,
    specs: []
  },
  'g003': {
    _id: 'g003', name: '冰美式咖啡（大杯）', price: 18.00, originalPrice: 0,
    image: '', tag: '新品',
    description: '精选阿拉比卡咖啡豆，每日新鲜萃取。大杯 500ml，可选少冰/去冰。',
    category: '饮品', stock: 200, soldCount: 312,
    specs: [
      { name: '标准冰', priceAdd: 0 },
      { name: '少冰', priceAdd: 0 },
      { name: '去冰', priceAdd: 0 }
    ]
  },
  'g004': {
    _id: 'g004', name: '炸薯条（大份）', price: 12.90, originalPrice: 0,
    image: '', tag: '',
    description: '选用优质土豆，现炸至金黄酥脆。大份约 200g。',
    category: '小食', stock: 150, soldCount: 89,
    specs: []
  },
  'g005': {
    _id: 'g005', name: '抹茶拿铁', price: 22.00, originalPrice: 0,
    image: '', tag: '',
    description: '日式抹茶搭配鲜牛奶，可选冷/热饮。',
    category: '饮品', stock: 80, soldCount: 45,
    specs: [
      { name: '冷饮', priceAdd: 0 },
      { name: '热饮', priceAdd: 0 }
    ]
  },
  'g006': {
    _id: 'g006', name: '提拉米苏', price: 28.00, originalPrice: 0,
    image: '', tag: '招牌',
    description: '经典意式提拉米苏，采用马斯卡彭芝士，每日手工制作。',
    category: '甜品', stock: 30, soldCount: 67,
    specs: []
  }
}

Page({
  data: {
    goods: {},
    specs: [],
    currentSpec: 0,
    cartCount: 0,
    totalPrice: '0.00'
  },

  onLoad(options) {
    const id = options.id || 'g001'
    const goods = MOCK_GOODS[id] || MOCK_GOODS['g001']
    const specs = goods.specs || []
    this.setData({
      goods,
      specs,
      currentSpec: 0
    })
    this.calcCartInfo()
  },

  onSelectSpec(e) {
    const idx = e.currentTarget.dataset.index
    this.setData({ currentSpec: idx })
    this.calcCartInfo()
  },

  calcCartInfo() {
    const cart = wx.getStorageSync('cart') || []
    const goodsId = this.data.goods._id
    const item = cart.find(c => c.goodsId === goodsId)
    if (item) {
      const price = this.data.goods.price + (this.data.specs[this.data.currentSpec]?.priceAdd || 0)
      this.setData({
        cartCount: item.quantity,
        totalPrice: (item.quantity * price).toFixed(2)
      })
    } else {
      this.setData({ cartCount: 0, totalPrice: '0.00' })
    }
  },

  onAddToCart() {
    const goods = this.data.goods
    if (goods.stock <= 0) {
      wx.showToast({ title: '暂时缺货', icon: 'none' })
      return
    }

    // 从缓存获取购物车
    let cart = wx.getStorageSync('cart') || []
    const price = goods.price + (this.data.specs[this.data.currentSpec]?.priceAdd || 0)
    const specName = this.data.specs[this.data.currentSpec]?.name || ''
    const existIdx = cart.findIndex(c => c.goodsId === goods._id && c.spec === specName)

    if (existIdx > -1) {
      cart[existIdx].quantity += 1
    } else {
      cart.push({
        goodsId: goods._id,
        name: goods.name,
        price: price,
        spec: specName,
        image: goods.image,
        quantity: 1,
        stock: goods.stock
      })
    }

    wx.setStorageSync('cart', cart)
    this.calcCartInfo()

    // 更新 TabBar 角标
    const totalCount = cart.reduce((s, i) => s + i.quantity, 0)
    wx.setTabBarBadge({ index: 1, text: String(totalCount) })

    wx.showToast({ title: '已加入购物车', icon: 'success', duration: 1000 })
  }
})
