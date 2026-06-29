/**
 * File: pages/order/checkout/checkout.js v2
 * Description: 订单结算页（安全加固版本）
 *
 * 安全变更:
 *   v1 - 客户端生成订单号、本地计算金额、写入 localStorage
 *   v2 - 仅传 goodsId+quantity 给云函数，服务端定价 [安全:防价格篡改]
 *       - 服务端生成订单号、计算金额、写入云数据库
 *       - 使用事务保证数据一致性
 *       - 防重复提交（submitting 状态锁）
 *
 * 数据流:
 *   [购物车] → checkoutItems (含价格,仅展示用途)
 *       ↓
 *   用户点击"提交订单"
 *       ↓
 *   [提取 goodsId + quantity] → 云函数 createOrder
 *       ↓
 *   [云函数] 从数据库读取价格 → 计算金额 → 事务写入 → 返回结果
 *       ↓
 *   [展示] 服务端返回的真实金额
 */

const cloud = require('../../utils/cloud')

Page({
  data: {
    items: [],           // 商品列表（含价格，仅展示用途）
    subtotal: '0.00',    // 客户端本地计算的小计（仅供参考）
    totalAmount: '0.00', // 最终以云函数返回为准
    remark: '',
    submitting: false,   // 防重复提交锁
    orderResult: null    // 下单成功后展示
  },

  onLoad() {
    const items = wx.getStorageSync('checkoutItems') || []
    if (items.length === 0) {
      wx.showToast({ title: '请先选择商品', icon: 'none' })
      setTimeout(() => wx.navigateBack(), 500)
      return
    }

    // 客户端仅作展示计算 [安全:最终价格以服务端为准]
    const total = items.reduce((s, i) => s + i.price * i.quantity, 0)
    this.setData({
      items,
      subtotal: total.toFixed(2),
      totalAmount: total.toFixed(2)
    })
  },

  onRemarkInput(e) {
    const remark = e.detail.value || ''
    // 限制备注长度 [安全:防止提交过长数据]
    if (remark.length > 200) return
    this.setData({ remark })
  },

  async onPlaceOrder() {
    const items = this.data.items
    if (items.length === 0) return

    // 防重复提交 [安全:防止重复下单]
    if (this.data.submitting) {
      wx.showToast({ title: '正在提交，请勿重复操作', icon: 'none' })
      return
    }

    // 二次确认 [安全:防止误操作]
    const confirm = await new Promise(resolve => {
      wx.showModal({
        title: '确认下单',
        content: `共 ${items.length} 件商品，请确认订单信息无误`,
        success: (res) => resolve(res.confirm)
      })
    })
    if (!confirm) return

    this.setData({ submitting: true })
    wx.showLoading({ title: '提交中...' })

    try {
      // 提取下单参数：仅传 goodsId 和 quantity [安全:不传价格]
      const goodsList = items.map(item => ({
        goodsId: item.goodsId,
        quantity: item.quantity,
        spec: item.spec || ''
      }))

      // 调用云函数下单
      const result = await cloud.createOrder(goodsList, this.data.remark)

      wx.hideLoading()

      if (result.code === 0) {
        // 下单成功
        const { orderNo, totalAmount } = result.data

        // 清空购物车中的已结算商品
        const cart = wx.getStorageSync('cart') || []
        const selectedIds = items.map(i => i.goodsId + '|' + (i.spec || ''))
        const newCart = cart.filter(i => {
          const key = i.goodsId + '|' + (i.spec || '')
          return !selectedIds.includes(key)
        })
        wx.setStorageSync('cart', newCart)

        // 更新角标
        const count = newCart.reduce((s, i) => s + i.quantity, 0)
        if (count > 0) {
          wx.setTabBarBadge({ index: 1, text: String(count) })
        } else {
          wx.removeTabBarBadge({ index: 1 })
        }

        // 展示成功结果（用服务端返回的真实金额覆盖本地计算值）
        this.setData({
          orderResult: { orderNo, totalAmount },
          totalAmount: totalAmount.toFixed(2)
        })

        wx.showToast({ title: '下单成功', icon: 'success' })

        // 跳转到订单列表
        setTimeout(() => {
          wx.redirectTo({
            url: `/pages/order/list?newOrder=${orderNo}`
          })
        }, 1500)

      } else {
        // 下单失败（库存不足、商品已下架等）
        wx.showModal({
          title: '下单失败',
          content: result.msg || '请稍后重试',
          showCancel: false
        })
        this.setData({ submitting: false })
      }

    } catch (err) {
      wx.hideLoading()
      console.error('[checkout] 下单异常:', err)
      wx.showToast({ title: '网络异常，请重试', icon: 'none' })
      this.setData({ submitting: false })
    }
  }
})
