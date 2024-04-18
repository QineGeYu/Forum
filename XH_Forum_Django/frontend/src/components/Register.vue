<template>
 <el-form @submit.native.prevent ="submit" class="register-form">
  <el-form-item label="用户名" prop="username">
    <el-input v-model="username" required></el-input>
  </el-form-item>
  <el-form-item label="邮箱" prop="email">
    <el-input v-model="email" required></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="password1">
    <el-input type="password" v-model="password1" required></el-input>
  </el-form-item>
  <el-form-item label="确认密码" prop="password2">
    <el-input type="password" v-model="password2" required></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" native-type="submit">注册</el-button><br>
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
      email: '',
      password1: '',
      password2: ''
    }
  },
  methods: {
    submit () {
      if (this.password1 !== this.password2) {
        console.log('请确认两次密码输入相同')
      } else {
        const requestBody = {
          username: this.username,
          password: this.password1,
          email: this.email
        }
        console.log(requestBody.username)
        console.log(requestBody.password)
        this.$axios.post('register/', requestBody)
          .then((response) => {
            console.log('registration successful')
            alert('注册成功！')
            this.$router.push('/Login')
          })
          .catch(error => {
            console.log('registration failed', error)
            alert('注册失败，请检查用户名密码是否正确。')
          })
      }
    }
  }
}
</script>

<style scoped>
.register-form {
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
