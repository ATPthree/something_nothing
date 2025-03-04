Page({
  // 页面的数据对象，用于存储页面的状态
  data: {
    orders: []  // 存储订单数据的数组
  },

  // 页面加载时触发的生命周期函数
  onLoad: function() {
    // 从本地存储中获取订单数据，如果不存在则使用空数组
    const storedOrders = wx.getStorageSync('orders') || [];
    
    // 将获取到的订单数据设置到页面的数据对象中
    this.setData({ orders: storedOrders });
  },

  // 格式化时间戳为可读的日期和时间字符串
  formatTimestamp: function(timestamp) {
    // 创建一个新的Date对象，传入时间戳
    const date = new Date(timestamp);
    
    // 使用padZero函数格式化月份、日期、小时、分钟和秒数，确保它们都是两位数
    return `${date.getFullYear()}-${padZero(date.getMonth() + 1)}-${padZero(date.getDate())} ${padZero(date.getHours())}:${padZero(date.getMinutes())}:${padZero(date.getSeconds())}`;
  }
});

// 辅助函数：补零
function padZero(num) {
  // 如果数字小于10，则在前面补一个0，否则直接返回该数字
  return num < 10 ? '0' + num : num;
}