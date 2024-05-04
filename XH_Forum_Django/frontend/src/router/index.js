import Vue from 'vue'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Login from '@/components/Login.vue'
import Register from '../components/Register.vue'
import HelloWorld from '../components/HelloWorld.vue'
import Router from 'vue-router'
import usermessage from '../components/usermessage.vue'
import PostDetail from '../components/PostDetail.vue'
import UserPage from '../components/UserPage.vue'
import MessageCentre from '../components/MessageCentre.vue'
Vue.use(Element)
Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/usermessage',
      name: 'usermessage',
      component: usermessage
    },
    {
      path: '/PostDetail/:postId',
      name: 'PostDetail',
      component: PostDetail
    },
    {
      path: '/UserPage',
      name: 'UserPage',
      component: UserPage
    },
    {
      path: '/MessageCentre',
      name: 'MessageCentre',
      component: MessageCentre
    }
  ]
})
export default router
