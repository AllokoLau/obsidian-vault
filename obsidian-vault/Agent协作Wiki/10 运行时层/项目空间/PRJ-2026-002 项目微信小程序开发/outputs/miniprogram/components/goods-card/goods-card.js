/**
 * File: components/goods-card/goods-card.js
 * Description: 商品卡片组件 — 展示商品缩略图、名称、价格、标签
 */

Component({
  properties: {
    name: { type: String, value: '' },
    price: { type: Number, value: 0 },
    image: { type: String, value: '' },
    tag: { type: String, value: '' },
    tagType: { type: String, value: 'hot' }
  }
})
