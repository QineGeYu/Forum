<template>
  <div>
    <el-menu
  :default-active="activeIndex2"
  class="el-menu-demo"
  mode="horizontal"
  @select="handleSelect"
  background-color="#545c64"
  text-color="#fff"
  active-text-color="#ffd04b">
  <el-menu-item index="1" @click="redirectTofirstPage">首页</el-menu-item>
  <el-submenu index="2">
    <template slot="title">板块分类</template>
    <el-menu-item index="2-1">选项1</el-menu-item>
    <el-menu-item index="2-2">选项2</el-menu-item>
    <el-menu-item index="2-3">选项3</el-menu-item>
    <el-submenu index="2-4">
      <template slot="title">选项4</template>
      <el-menu-item index="2-4-1">选项1</el-menu-item>
      <el-menu-item index="2-4-2">选项2</el-menu-item>
      <el-menu-item index="2-4-3">选项3</el-menu-item>
    </el-submenu>
  </el-submenu>
  <el-menu-item index="3">消息中心</el-menu-item>
  <el-menu-item index="4" @click="redirectToUserPage"> 个人主页 </el-menu-item>
  <el-avatar class="profile user pull-right" >{{ user }}</el-avatar>
</el-menu>
  <div class="descriptions-container">
  <el-descriptions class="margin-top" title="个人信息" :column="3" border size="medium">
   <template slot="extra">
      <el-button type="primary" >编辑</el-button>
    </template>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-user"></i>
        用户名
      </template>
      {{ message.username }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-message"></i>
        电子邮箱
      </template>
      {{ message.email }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-tickets"></i>
        昵称
      </template>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-timer"></i>
        加入时间
      </template>
      {{ message.date_joined }}
    </el-descriptions-item>
  </el-descriptions>
  </div>
  <div class="block">
  <el-timeline class="card-line">
    <el-timeline-item v-for="card in cards" :key="card.id" :timestamp="card.created_at" placement="top">
      <el-card class="card">
        <el-avatar class="profile author"> {{ card.author_id }} </el-avatar>
        <h4 class="card-title">标题:{{ card.title }}</h4>
        <p class="card-description">摘要:  {{ card.description }}</p>
          <div class="like-section">
           <el-button @click="likePost(card.id-1)">
            <i class="el-icon-magic-stick"></i>  赞
            <span class="like-count">{{ card.likeCount }}</span>
            </el-button>
        </div>
      </el-card>
    </el-timeline-item>
  </el-timeline>
</div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      cards: [],
      user: null,
      message: [],
      activeIndex: '4',
      activeIndex2: '4'
    }
  },
  mounted () {
    this.user = sessionStorage.getItem('user').replace(/"/g, '')
    console.log(this.user)
    this.getPost()
    this.getUserMessage()
  },
  methods: {
    likePost (id) {
      this.cards[id].likeCount++
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    },
    redirectTofirstPage () {
      this.$router.push({
        path: '/HelloWorld'
      })
    },
    redirectToUserPage () {
      this.$router.push({
        path: '/usermessage'
      }) // 根据您的路由配置，将'usermessage'替换为目标页面的路由路径
    },
    getPost () {
      this.$axios.get('show_user_post/')
        .then(response => {
          this.cards = JSON.parse(response.data.posts)
          console.log(this.cards)
        })
        .catch(error => {
          alert('请登录后再访问')
          console.error('Error:', error)
        })
    },
    getUserMessage () {
      this.$axios.get('show_user_message/')
        .then(response => {
          this.message = response.data
          console.log(this.message)
        })
        .catch(error => {
          console.error('Error:', error)
        })
    }
  }
}
</script>
<style>
@import url("//unpkg.com/element-ui@2.15.14/lib/theme-chalk/index.css");
.el-menu-demo {
  display: flex;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9999;
}
.profile.author {
  position: absolute;
  top: 10px;
  left: 10px;
}
.card-line {
  width: 60%; /* 调整卡片容器的宽度 */
}
.card {
  margin: 0 auto; /* 水平居中 */
  max-width: 100%; /* 确保卡片不超过父容器的宽度 */
}
.block {
  display: flex;
  justify-content: center;
}
.like-section {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  align-items: center;
}
.card-description {
  word-wrap: break-word;
  word-break: break-all;
  text-align: left;
}
.card-title {
  text-align: left;
}

</style>
