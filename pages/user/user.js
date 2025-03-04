Page({
  data: {},

  /**
   * 退出登录功能
   */
  logout: function() {
    // 清除本地存储的数据
    try {
      wx.removeStorageSync('studentId'); // 清除学生ID
      console.log('studentId removed');
      wx.removeStorageSync('cart'); // 清除购物车数据
      console.log('cart removed');
      wx.removeStorageSync('orders'); // 清除订单数据
      console.log('orders removed');

      // 显示退出登录成功的提示
      wx.showToast({ title: '已退出登录', icon: 'success' });

      // 重新加载登录页面
      wx.reLaunch({ url: '/pages/login/login' }); // 假设有一个登录页
    } catch (e) {
      console.error('Error clearing storage:', e);
    }
  }
});