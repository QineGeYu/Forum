import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './router/index'
import VueRouter from 'vue-router'
import axios from 'axios'
import JSEncrypt from 'jsencrypt'
Vue.prototype.$jsEncrypt = JSEncrypt
Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.config.productionTip = false
axios.defaults.baseURL = 'http://localhost:8000/api'
axios.defaults.withCredentials = true
Vue.prototype.$axios = axios
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
}).$mount('#app')

// createApp(App).use('#app')
