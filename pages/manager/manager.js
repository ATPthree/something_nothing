Page({
  data: {
    tab: 'view-orders',
    dishes: [],
    orders: [],
    newDish: {
      name: '',
      price: ''
    }
  },

  onLoad: function() {
    const user = wx.getStorageSync('user');
    if (!user.startsWith('manager')) {
      wx.showToast({ title: '权限不足', icon: 'none' });
      wx.navigateBack();
      return; // 确保在权限不足时不执行后续代码
    }

    // 从本地存储中获取订单列表和菜品列表
    const orders = wx.getStorageSync('orders') || [];
    const dishes = wx.getStorageSync('dishes') || [];
    this.setData({ orders, dishes }); // 同时设置订单和菜品列表
  },

  // 格式化日期的方法
  formatDate: function(timestamp) {
    const date = new Date(timestamp);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  },

  // 处理订单内容的方法
  getOrderDetails: function(items) {
    return items.map(item => `${item.name} x ${item.quantity}`).join(', ');
  },

  // 切换标签的方法
  switchTab: function(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ tab });
  },

  // 添加菜品的方法
  addDish: function() {
    const { newDish } = this.data;
    // 校验名称和价格是否已填写
    if (!newDish.name || !newDish.price) {
      wx.showToast({ title: '请填写完整信息', icon: 'none' });
      return;
    }

    const newDishWithId = { ...newDish, id: Date.now() };
    // 添加新菜品到菜品列表
    const dishes = [...this.data.dishes, newDishWithId];
    this.setData({ dishes, newDish: { name: '', price: '' } }); // 添加后重置新菜品信息

    // 保存更新后的菜品列表到本地存储
    wx.setStorageSync('dishes', dishes);
    wx.showToast({ title: '添加成功', icon: 'success' });
  },

  // 删除菜品的方法
  deleteDish: function(e) {
    const dishId = e.currentTarget.dataset.id;
    const dishes = this.data.dishes.filter(dish => dish.id !== dishId);
    this.setData({ dishes });

    // 保存更新后的菜品列表到本地存储
    wx.setStorageSync('dishes', dishes);
    wx.showToast({ title: '删除成功', icon: 'success' });
  },

  // 更新新菜品信息的方法
  updateNewDish: function(e) {
    const { name, value } = e.detail;
    this.setData({ ['newDish.' + name]: value });
  },

  // 更新订单状态的方法
  updateOrderStatus: function(e) {
    const orderId = e.currentTarget.dataset.orderId;
    const newItemStatus = e.currentTarget.dataset.newStatus;
    let orders = this.data.orders.slice(); // 深拷贝订单列表

    const orderIndex = orders.findIndex(order => order.id === orderId);
    if (orderIndex !== -1) {
      orders[orderIndex].status = newItemStatus; // 更新订单状态
      this.setData({ orders });

      // 保存更新后的订单列表到本地存储
      wx.setStorageSync('orders', orders);
    }
  }
});