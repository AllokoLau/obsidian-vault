/**
 * File: app.js
 * Project: 微信小程序开发 (PRJ-2026-002)
 * Description: 小程序入口 — 初始化云开发环境
 * Dependencies: 微信开放能力 / 云开发
 */

App({
  onLaunch() {
    // 云开发环境初始化
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
    } else {
      wx.cloud.init({
        env: 'alloko-ordering', // 云环境 ID，创建后替换
        traceUser: true
      })
    }

    // 获取系统信息
    const sysInfo = wx.getSystemInfoSync()
    this.globalData.systemInfo = sysInfo
  },

  globalData: {
    systemInfo: null,
    // 当前用户信息（从微信获取）
    userInfo: null
  }
})
