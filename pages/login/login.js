Page({
  data: {
    studentId: '',
    name_curr:'',
    password: ''
  },

  // 绑定学号输入
  bindStudentIdInput: function(e) {
    this.setData({ studentId: e.detail.value });
  },
 // 绑定姓名输入
 bindNameInput: function(e) {
  this.setData({ name_curr: e.detail.value });
},
  // 绑定密码输入
  bindPasswordInput: function(e) {
    this.setData({ password: e.detail.value });
  },

  // 登录
  login: function() {
    const { studentId,name_curr , password } = this.data;

    // 模拟的用户数据
   const data = {
    user_id: studentId,
    name:name_curr,
    passwd: password
  };

    wx.request({
    url: 'http://127.0.0.1:5000/comm/login', // 注意：确保 URL 是正确的，且 Flask 服务器可以被微信小程序访问
    method: 'POST',
    data: data,
    header: {
      'content-type': 'application/json' // 设置正确的请求头
    },
    success: (res) => {
      // 请求成功后的处理
      if (res.statusCode === 200 && res.data.status === 'success') {
        // 登录成功
        wx.setStorageSync('user', studentId);
        wx.showToast({
          title: res.data.data.message, // 使用后端返回的成功消息
          icon: 'success'
        });
        if(res.data.data.message === "欢迎管理员登录"){
         this.navigateToAdminHome();
        }else if(res.data.data.message === "欢迎窗口工作者登录"){
            this.navigateToAuntHome();
        }else{
            this.navigateToHome();
        }
      //  this.navigateToHome();
      } else {
        // 登录失败，可能是服务器返回了错误状态码或错误信息
        wx.showToast({
          title: res.data.message || '登录失败，请稍后再试',
          icon: 'none'
        });
      }
    },
    fail: (err) => {
      // 请求失败的处理
      console.error('请求失败:', err); // 打印错误信息到控制台
      wx.showToast({
        title: '网络错误，请检查您的网络连接',
        icon: 'none'
      });
    }
  });
},
register: function() {
    const { studentId, name_curr, password } = this.data;
    const data = {
        user_id: studentId,
        name: name_curr,
        passwd: password
    };
    wx.request({
        url: 'http://127.0.0.1:5000/comm/register',
        method: 'POST',
        data: data,
        header: {
            'content-type': 'application/json' // 设置正确的请求头
        },
        success: (res) => {
            console.log('注册响应:', res); // 打印响应内容，确保返回的格式是正确的
            if (res.statusCode === 200 && res.data.status === 'success') {
                // 注册成功后的处理
                wx.showToast({
                    title: '注册成功',
                    icon: 'success',
                    duration: 2000 // 设置2秒后自动消失
                });

                // 注册成功后跳转到登录页面
                setTimeout(() => {
                    wx.redirectTo({ url: '/pages/login/login' });
                }, 2000);  // 延时跳转，确保提示信息能显示
            } else {
                // 注册失败的处理
                wx.showToast({
                    title: res.data.message || '注册失败，请稍后再试',
                    icon: 'none'
                });
            }
        },
        fail: (err) => {
            // 请求失败的处理
            console.error('请求失败:', err); // 打印错误信息到控制台
            wx.showToast({
                title: '网络错误，请检查您的网络连接',
                icon: 'none'
            });
        }
    });
},
  navigateToHome: function() {
    wx.redirectTo({ url: '/pages/home/home' });
  },
  navigateToAdminHome: function() {
    wx.redirectTo({ url: '/pages/manager/manager' });
 },
  navigateToAuntHome: function() {
    wx.redirectTo({ url: '/pages/canteen-aunt/canteen-aunt' });
 }
});