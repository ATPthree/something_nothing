Page({
  data: {
    tab: 'view-orders',
    orders: []
  },

  onLoad: function() {
    const user = wx.getStorageSync('user');
    if (!user.startsWith('aunt')) {
      wx.showToast({ title: '权限不足', icon: 'none' });
      wx.navigateBack();
    }

    // 初始化本地订单数据
    this.fetchOrders();
  },

  // 初始化本地订单数据
  fetchOrders: function() {
    const user = wx.getStorageSync('user');
    const windowId = parseInt(user.slice(-2),10);
    wx.request({
      url: `http://127.0.0.1:5000/mgr/orders/${windowId}`, // 替换为你的Flask服务器URL
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          const orders = res.data.map(order => ({
            id: order.id,
            user: order.user_id,
            //timeStamp: this.formatDate(new Date(order.order_time.repace(/-/g, '/')).getTime()),
            //timestamp: new Date(order.order_time.replace(/-/g, '/')).getTime(),
            order_time: order.order_time,     //格式原因直接改为字符串显示
            status: this.mapStatus(order.status),
            items2: order.order_content, // 用于显示的订单内容
          //  items2: order.order_content.replace(/[TZ]/g, ""), // 用于显示的订单内容
           // items: this.parseOrderContent(order.order_content) // 假设有一个方法可以解析订单内容
          }));
          this.setData({ orders });
       //   wx.setStorageSync('order_id', orders.id);
        } else {
          wx.showToast({ title: '获取订单失败', icon: 'none' });
        }
      },
      fail: () => {
        wx.showToast({ title: '网络请求失败', icon: 'none' });
      }
    });
  },

  // 假设的方法：解析订单内容
 parseOrderContent: function(orderContent) {
  // 使用split方法分割字符串，返回一个包含所有菜品的数组
  var dishes = orderContent.split(/\s+/); // 使用正则表达式分割，可以处理多个连续空格

  // 过滤掉空字符串，以防输入中有连续空格
  dishes = dishes.filter(function(dish) {
    return dish !== '';
  });
  return dishes;
},
  // 将后端的状态映射到前端的状态
  mapStatus: function(status) {
    const statusMap = {
      0: '等待中',
      1: '制作中',
      2: '已完成'
    };
    return statusMap[status] || '未知状态';
  },
  // 用于格式化日期
  // formatDate: function(timestamp) {
  //   const date = new Date(timestamp);
  //   return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  // },

  // 用于处理订单内容
  getOrderDetails: function(items) {
    return items.map(item => `${item.name} x ${item.quantity}`).join(', ');
  },

  switchTab: function(e) {
    const tab = e.currentTarget.dataset.tab;
    if (tab === 'personal-center') {
      wx.navigateTo({ url: '/pages/user/user' });
    } else {
      this.setData({ tab });
    }
  },

  updateOrderStatus: function(e) {
  const orderId = e.currentTarget.dataset.orderId;
  const newItemStatus = e.currentTarget.dataset.newStatus;
  // 只处理状态为“已完成”的情况
  if (newItemStatus === '已完成') {
    // 更新本地订单状态
    const orders = this.data.orders.map(order => {
      if (order.id === orderId) {
        order.status = newItemStatus;
      }
      return order;
    });
    this.setData({ orders });
   // wx.setStorageSync('orders', orders);
    wx.request({
      url: 'http://127.0.0.1:5000/mgr/order_queue/finished',
      method: 'POST',
      header: {
        'content-type': 'application/json'
      },
      data: {order_id:orderId},
      success: (res) => {
        if (res.data==='success') {
          wx.showToast({ title: '更新成功', icon: 'success' });
          this.fetchOrders();
        } else {
          wx.showToast({ title: '更新失败', icon: 'none' });
          console.error('后端返回错误', res.data);
        }
      },
      fail: () => {
        wx.showToast({ title: '网络错误', icon: 'none' });
      }
    });
  }
}

});