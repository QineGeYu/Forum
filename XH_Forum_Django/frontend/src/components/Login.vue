<template>
<el-card>
 <el-form @submit.native.prevent ="submitForm" class="login-form">
  <el-form-item label="用户名" prop="username">
    <el-input v-model="username" required></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="password">
    <el-input type="password" v-model="password" required></el-input>
  </el-form-item>

     <el-button type="primary" @click="dialogFormVisible = true">忘记密码</el-button>

<el-dialog title="找回密码" :visible.sync="dialogFormVisible">
    <el-button :aria-disabled="isSending" @click="sendEmail" :class="{ 'disabled': isSending }">
      <span v-if="isSending">发送中...</span>
      <span v-else>发送验证码给邮箱</span>
    </el-button>
    <span v-if="countdown > 0">倒计时：{{ countdown }}s</span>
  <el-form :model="form">

        <el-form-item label="验证码">
          <el-input v-model="code" placeholder="请输入验证码"></el-input>
        </el-form-item>

  </el-form>

  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="verifyCode">验 证</el-button>
  </div>

</el-dialog>
<el-dialog title="重置密码" :visible.sync="dialogFormVisible2">
  <el-form :model="form2">

        <el-form-item label="新密码">
          <el-input v-model="newPassword" placeholder="请输入新密码"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="newPassword2" placeholder="请确认新密码"></el-input>
        </el-form-item>

  </el-form>

  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible2 = false">取 消</el-button>
    <el-button type="primary" @click="resetPassword">验 证</el-button>
  </div>
</el-dialog>
   <Vcode
    :imgs="[ img1,img2,img3 ]"
    :show="isShow"
    @success="onSuccess"
    @close="onClose"
  />
  <el-form-item>
    <el-button type="primary" native-type="submit">登录</el-button>
    <el-button type="primary" @click="goToRegister">注册</el-button>
  </el-form-item>
 </el-form>
 </el-card>
</template>

<script>
import Vcode from 'vue-puzzle-vcode'
import img1 from '../assets/img1.jpeg'
import img2 from '../assets/img2.jpeg'
import img3 from '../assets/img3.jpeg'
import { Button, Form, FormItem, Input } from 'element-ui'
export default {
  components: {
    'el-button': Button,
    'el-form': Form,
    'el-from-item': FormItem,
    'el-input': Input,
    Vcode
  },
  data () {
    return {
      dialogFormVisible: false,
      dialogFormVisible2: false,
      form: {},
      form2: {},
      newPassword: '',
      newPassword2: '',
      isShow: false,
      username: '',
      password: '',
      code: '',
      img1,
      img2,
      img3,
      email: null,
      isSending: false,
      countdown: 0

    }
  },
  methods: {
    submitForm () {
      this.isShow = true
    },
    goToRegister () {
      this.$router.push('/Register')
    },
    // 用户通过了验证
    onSuccess (msg) {
      this.isShow = false // 通过验证后，需要手动隐藏模态框
      const requestBody = {
        username: this.username,
        password: this.password
      }
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
          alert('登录失败，请检查账号密码输入正确')
        })
    },
    // 用户点击遮罩层，应该关闭模态框
    onClose () {
      this.isShow = false
    },
    sendEmail () {
      if (this.isSending) {
        return
      }
      this.isSending = true
      this.countdown = 60
      this.$axios.post('getEmail/', { username: this.username })
        .then((response) => {
          this.email = response.data.email
          this.startCountdown()
        })
        .catch(error => {
          console.error('账号不存在或邮箱不存在', error)
          alert('账号不存在或邮箱不存在')
          this.isSending = false
        })
    },
    verifyCode () {
      this.$axios.post('verifyCode/', { code: this.code })
        .then(response => {
          console.log('验证码验证成功！')
          this.dialogFormVisible = false
          this.dialogFormVisible2 = true
        })
        .catch(error => {
          console.error('验证码验证失败', error)
          alert('验证失败，请确认验证码是否正确！')
        })
    },
    resetPassword () {
      if (this.newPassword !== this.newPassword2) {
        alert('请确认两次密码输入相同!')
      } else {
        const requestBody = {
          username: this.username,
          password: this.newPassword
        }
        this.$axios.post('resetPassword/', requestBody)
          .then((response) => {
            console.log('registration successful')
            alert('修改成功！')
            this.dialogFormVisible2 = false
          })
          .catch(error => {
            console.log('failed', error)
          })
      }
    },
    startCountdown () {
      const timer = setInterval(() => {
        this.countdown--
        if (this.countdown === 0) {
          clearInterval(timer)
          this.isSending = false
        }
      }, 1000)
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
.el-button.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
