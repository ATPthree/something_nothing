Page({
  // 页面的数据对象
  data: {
    featuredDishes: [
      { id: 1, name: '招牌牛肉面', image: 'https://www.helloimg.com/i/2024/10/14/670d1a917718b.jpg' },
      { id: 2, name: '麻辣香锅', image: 'https://www.helloimg.com/i/2024/10/14/670d1a9076218.jpg' },
      // 更多菜品...
    ],
    promotions: [
      { id: 1, title: '买一赠一', description: '购买任意主菜即可获得一份免费小吃！' },
      { id: 2, title: '午餐特惠', description: '午餐时段享受八折优惠！' },
      // 更多优惠...
    ],
    studentId: ''  // 存储用户ID
  },

  // 页面加载时触发
  onLoad: function() {
    // 从本地存储中获取学生ID
    const studentId = wx.getStorageSync('studentId');
    
    // 如果存在学生ID，则设置到页面数据中
    if (studentId) {
      this.setData({ studentId });
    } else {
      // 如果没有学生ID，提示用户登录并返回上一页
      wx.showToast({ title: '请先登录', icon: 'none' });
      wx.navigateBack();
    }
  },

  // 导航到订单创建页面
  navigateToOrder: function() {
    // 使用wx.navigateTo跳转到订单创建页面
    wx.navigateTo({ url: '/pages/order/order' });
  },

  // 导航到订单列表页面
  navigateToOrders: function() {
    // 使用wx.navigateTo跳转到订单列表页面
    wx.navigateTo({ url: '/pages/orders/orders' });
  },

  // 导航到个人中心页面
  navigateToProfile: function() {
    // 使用wx.navigateTo跳转到个人中心页面
    wx.navigateTo({ url: '/pages/user/user' });
  },

  // 用户退出登录
  logout: function() {
    // 清除本地存储中的学生ID
    wx.removeStorageSync('studentId');

    // 清除本地存储中的购物车数据
    wx.removeStorageSync('cart');

    // 清除本地存储中的订单数据
    wx.removeStorageSync('orders');

    // 显示退出登录成功的提示
    wx.showToast({ title: '已退出登录', icon: 'success' });

    // 重定向到登录页面
    wx.redirectTo({ url: '/pages/login/login' });
  }
});