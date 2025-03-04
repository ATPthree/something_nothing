Page({
  data: {
    currentTab: 'floor1', // 默认选中一楼
    floor1Dishes: [
      {
        id: 1,
        name: '宫保鸡丁',
        image: 'https://www.helloimg.com/i/2024/10/16/670fa9f98ff7b.jpg', 
        price: 25
      },
      {
        id: 2,
        name: '麻婆豆腐',
        image: 'https://www.helloimg.com/i/2024/10/16/670faa32607ac.jpeg', 
        price: 18
      },
      {
        id: 3,
        name: '鱼香肉丝',
        image: 'https://www.helloimg.com/i/2024/10/16/670faa5d55fe4.jpg',
        price: 22
      },
      {
        id: 4,
        name: '番茄炒蛋',
        image: 'https://www.helloimg.com/i/2024/10/16/670faaa33da67.jpg', // 替换为实际的图片URL
        price: 12
      }
    ],
    floor2Dishes: [
      {
        id: 5,
        name: '鱼香肉丝',
        image: 'https://example.com/yuxiangrousi.jpg', // 替换为实际的图片URL
        price: 22
      },
      {
        id: 6,
        name: '金陵烤鸭',
        image: 'https://example.com/fanqiechaodan.jpg', // 替换为实际的图片URL
        price: 12
      },
      {
        id: 7,
        name: '糖醋排骨',
        image: 'https://example.com/yuxiangrousi.jpg', // 替换为实际的图片URL
        price: 22
      },
      {
        id: 8,
        name: '炒白菜',
        image: 'https://example.com/fanqiechaodan.jpg', // 替换为实际的图片URL
        price: 12
      }
    ],
    cart: [],
    isCartVisible: false
  },

  onLoad: function() {
    // 页面加载时获取购物车数据
    const storedCart = wx.getStorageSync('cart') || [];
    this.setData({ cart: storedCart });
  },

  onUnload: function() {
    // 页面关闭时保存购物车数据
    wx.setStorageSync('cart', this.data.cart);
  },

  // 切换标签
  switchTab: function(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ currentTab: tab });
  },

  // 将菜品添加到购物车
  addToCart: function(e) {
    const dish = e.currentTarget.dataset.dish;

    // 获取当前购物车数据
    let cart = this.data.cart;

    // 检查菜品是否已经在购物车中
    const existingDishIndex = cart.findIndex(item => item.id === dish.id);

    if (existingDishIndex !== -1) {
      // 如果菜品已在购物车中，增加数量
      cart[existingDishIndex].quantity += 1;
    } else {
      // 否则，将菜品添加到购物车
      dish.quantity = 1;
      cart.push(dish);
    }

    // 更新购物车数据并保存到本地存储
    this.setData({ cart: cart });
    wx.setStorageSync('cart', cart);
    wx.showToast({ title: '已加入购物车', icon: 'success' });
  },

  toggleCart: function() {
    this.setData({ isCartVisible: !this.data.isCartVisible });
  },

  increaseQuantity: function(e) {
    const index = e.currentTarget.dataset.index;
    let cart = this.data.cart;

    // 增加数量
    cart[index].quantity += 1;

    // 更新购物车数据并保存到本地存储
    this.setData({ cart: cart });
    wx.setStorageSync('cart', cart);
  },

  decreaseQuantity: function(e) {
    const index = e.currentTarget.dataset.index;
    let cart = this.data.cart;

    // 减少数量
    cart[index].quantity -= 1;

    // 如果数量为0，移除菜品
    if (cart[index].quantity <= 0) {
      cart.splice(index, 1);
    }

    // 更新购物车数据并保存到本地存储
    this.setData({ cart: cart });
    wx.setStorageSync('cart', cart);
  },

submitOrder: function() {
  const cart = this.data.cart;
  if (cart.length === 0) {
    wx.showToast({ title: '购物车为空', icon: 'none' });
    return;
  }
  // 创建订单对象
 // const orderContent = cart.map(item => Array(item.quantity).fill(item.id).join(' ')).join(' ');
 // const orderContent = cart.map(item => `${item.id}`).join(' ');
  const orderContent = cart.map(item => `${item.quantity}*${item.id}`).join(' ');
  const user = wx.getStorageSync('user');

  const order = {
    window_id: 11, // 假设窗口ID为1，实际应根据实际情况获取
    id: parseInt(user), // 假设用户ID为1，实际应根据实际情况获取
    order_content: orderContent
  };

  // 发送订单数据到服务器
  wx.request({
    url: 'http://127.0.0.1:5000/cus/order/add',
    method: 'POST',
    data: order,
    header: {
      'content-type': 'application/json', // 默认值
      'cookie': wx.getStorageSync('session') // session存储在本地存储中
    },
    success (res) {
      console.log('订单提交成功:', res.data);
      // 检查后端返回的订单ID（int型）
      // if (res.data !== undefined && res.data !== null) {
        // 提示用户订单已提交
        wx.showToast({ title: '订单已提交', icon: 'success' });
        // 清空购物车
        this.setData({ cart: [] });
        wx.removeStorageSync('cart');

        // 导航到订单页面，可以传递订单ID
        wx.navigateTo({ url: `/pages/orders/orders?orderId=${res.data}` });
      // } else {
      //   // 如果没有返回订单ID，提示用户订单提交失败
      //   wx.showToast({ title: '订单提交失败', icon: 'none' });
      // }
    },
    fail (err) {
      console.error('订单提交失败:', err);
      wx.showToast({ title: '订单提交失败', icon: 'none' });
    }
  });
}
});