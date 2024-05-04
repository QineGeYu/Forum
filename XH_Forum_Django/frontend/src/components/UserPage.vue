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
  <el-menu-item index="1">{{ user }}的主页</el-menu-item>
  <el-avatar class="profile user pull-right" >{{ user }}</el-avatar>
</el-menu>
  <div class="button-container">
  <el-button class="custom-button" icon="el-icon-message" @click="chat">私信</el-button>
  </div>
  <div class="descriptions-container">
  <el-descriptions class="margin-top" title="个人信息" :column="3" border size="medium">

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
    <el-timeline-item v-for="item in cards" :key="item.id" :timestamp="item.created_at" placement="top">
      <el-card class="card">
        <!-- <el-avatar class="profile author" @click="goToUserPage(item.author_id)"> {{ item.author_id }} </el-avatar> -->
          <div class="avatar-wrapper">
             <el-avatar class="profile author">{{ item.author_id }}</el-avatar>
          </div>
        <h4 class="card-title">标题:{{ item.title }}</h4>
        <p class="card-description">摘要:  {{ item.description }}</p>
          <div class="like-section">
           <el-button @click="likePost(item)">
            <i class="el-icon-magic-stick"></i>  赞
            <span class="like-count">{{ item.likeCount }}</span>
            </el-button>
            <el-button @click="goToPostDetail(item)">
            <i class="el-icon-chat-line-round"></i>  评论
            <span class="like-count">{{ item.comments }}</span>
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
      activeIndex2: '4',
      dialogFormVisible: false,
      form: {},
      title: null,
      description: null,
      content: null

    }
  },
  mounted () {
    this.user = this.$route.query.authorId
    this.main_user = sessionStorage.getItem('user').replace(/"/g, '')
    console.log(this.user)
    console.log(this.main_user)
    this.getPost()
    this.getUserMessage()
  },
  methods: {
    chat () {
      this.$axios.post('save_contact/', {
        contacted_users: this.user
      })
      this.$router.push({
        path: '/MessageCentre'
      })
    },
    likePost (item) {
      console.log(item.id)
      this.$axios.post('like_post/', {
        postId: item.id
      })
        .then(response => {
          item.likeCount = response.data.likeCount
        })
        .catch(error => {
          console.error('点赞失败:', error)
        })
    },
    goToPostDetail (item) {
      console.log(item.id)
      this.$router.push({ name: 'PostDetail', params: { postId: item.id } })
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    },
    getPost () {
      this.$axios.get('show_user_post2/', {
        params: {
          username: this.user
        }
      })
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
      this.$axios.get('show_user_message2/', {
        params: {
          username: this.user
        }
      })
        .then(response => {
          this.message = response.data
          console.log(this.message)
        })
        .catch(error => {
          console.error('Error:', error)
        })
    },
    publishPost () {
      console.log('click here')
      const postData = {
        title: this.title,
        description: this.description,
        content: this.content,
        user: this.user
      }
      console.log(postData)
      this.$axios.post('publish_post/', postData)
        .then(response => {
          // 处理请求成功的响应
          alert('帖子发布成功')
          this.title = ''
          this.description = ''
          this.content = ''
          window.location.reload()
        })
        .catch(error => {
          console.error('帖子发布失败', error)
        })
        .finally(() => {
          // 请求完成后的清理工作，可选
        })
      this.dialogFormVisible = false
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
.button-container {
  display: flex;
  justify-content: flex-end;
}
.custom-button {
  font-size: 18px;
  padding: 10px 20px;
  background-color: hsl(221, 71%, 53%);
  color: #ffffff;
}
</style>
