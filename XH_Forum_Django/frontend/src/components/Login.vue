<template>
 <el-form @submit.native.prevent ="submitForm" class="login-form">
  <el-form-item label="用户名" prop="username">
    <el-input v-model="username" required></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="password">
    <el-input type="password" v-model="password" required></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" native-type="submit">登录</el-button><br>
    <router-link to="/Register">注册</router-link>
  </el-form-item>
 </el-form>
</template>

<script>
import { Button, Form, FormItem, Input } from 'element-ui'
export default {
  components: {
    'el-button': Button,
    'el-form': Form,
    'el-from-item': FormItem,
    'el-input': Input
  },
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submitForm () {
      const requestBody = {
        username: this.username,
        password: this.password
      }
      // const sessionId = localStorage.getItem('sessionId')
      this.$axios.post('login/', requestBody)
        .then((response) => {
          console.log('Login successful')
          sessionStorage.setItem('user', JSON.stringify(this.username))
          this.$router.push({
            path: '/HelloWorld'
          })
        })
        .catch(error => {
          console.error('Login failed', error)
        })
    }
  }
}

</script>

<style scoped>
.login-form {
    max-width: 300px;
    margin: 0 auto;
}

.el-form-item {
    line-height: 40px;
}

.el-button {
    margin-top: 20px;
}
</style>
