/**
 * File: components/order-item/order-item.js
 * Description: 订单卡片组件 — 展示订单摘要信息
 */

Component({
  properties: {
    orderNo: { type: String, value: '' },
    statusText: { type: String, value: '' },
    products: { type: Array, value: [] }
  }
})
