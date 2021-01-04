// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
// 引入element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/css/global.css'



Vue.use(ElementUI, { size: 'medium', zIndex: 3000 })

Vue.config.productionTip = false


// axios请求拦截
axios.interceptors.request.use(function (config) {
  let token = window.sessionStorage.getItem('token')
  if(token){
    config.headers.common['Authorization'] = 'Bearer ' + token
  }
  return config
}, function (error) {
    return Promise.reject(error)
})

// 响应拦截
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response.status == 401) {
      window.sessionStorage.removeItem('token')
    }
    return Promise.reject(error.response)   // 返回接口返回的错误信息
  });
export default axios;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  // 定义请求地址为全局变量，引用方式：this.$root.URL
  data: function(){
          return {
               URL: 'http://localhost:8000/ytwapi',
          }
      },
  components: { App },
  template: '<App/>'
})
