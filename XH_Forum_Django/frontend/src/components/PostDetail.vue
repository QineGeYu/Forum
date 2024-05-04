<template>
  <div class="post-detail">
<el-page-header @back="goBack" content="详情页面">
</el-page-header>
    <el-divider></el-divider>
    <el-card class="card">
            <el-avatar class="profile user" >{{ post.author_id }}</el-avatar>
      <h2 class="card-title">标题：{{ post.title }}</h2>
      <p class="card-description">摘要：{{ post.description }}</p>
      <div class="card-content">
        主要内容：{{ post.content }}
      </div>
    </el-card>
        <el-divider></el-divider>
    <div class="card-footer">
        <el-input v-model="input" placeholder="请输入评论"></el-input>
            <el-divider></el-divider>
        <el-button type="primary" @click="publish_comment">发表评论</el-button>
        <el-button type="primary" @click="goBack">返回</el-button>
    </div>

    <div class="block">
  <el-timeline class="card-line">
    <el-timeline-item v-for="item in comments" :key="item.id" :timestamp="item.created_at" placement="top">
      <el-card class="card">
        <el-avatar class="profile author"> {{ item.author }} </el-avatar>
        <p class="card-description">{{ item.content }}</p>
          <div class="like-section">
           <el-button @click="likeComment(item)">
            <i class="el-icon-magic-stick"></i>  赞
            <span class="like-count">{{ item.like_count }}</span>
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
      user: null,
      post: {}, // 帖子详情数据
      comments: [],
      input: null
    }
  },
  methods: {
    goBack () {
      this.$router.go(-1) // 返回上一页
    },
    get_post_detail () {
      const postId = this.$route.params.postId
      console.log(postId)
      // 获取帖子详情数据的异步请求示例（假设使用axios）
      this.$axios.get(`/posts/${postId}`)
        .then(response => {
          this.post = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    get_post_comments () {
      const postId = this.$route.params.postId
      this.$axios.get(`/comments/${postId}`)
        .then(response => {
          this.comments = response.data.comments
          console.log(this.comments)
        })
        .catch(error => {
          console.error(error)
        })
    },
    publish_comment () {
      const commentData = {
        content: this.input,
        user: this.user,
        postId: this.$route.params.postId
      }
      this.$axios.post('/publish_comment/', commentData)
        .then(response => {
          // 处理请求成功的响应
          alert('评论发布成功')
          this.input = ''
          window.location.reload()
        })
        .catch(error => {
          console.error('评论发布失败', error)
        })
        .finally(() => {
          // 请求完成后的清理工作，可选
        })
    },
    likeComment (item) {
      console.log(item.id)
      this.$axios.post('/like_comment/', {
        commentId: item.id
      })
        .then(response => {
          item.like_count = response.data.like_count
        })
        .catch(error => {
          console.error('点赞失败:', error)
        })
    }
  },
  mounted () {
    this.user = sessionStorage.getItem('user').replace(/"/g, '')
    console.log(this.user)
    this.get_post_detail()
    this.get_post_comments()
  }
}
</script>

<style scoped>
.post-detail {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 250px;
  background-color: #f5f5f5;
}

.card {
  width: 200px;
  padding: 20px;
}

.card-title {
  font-size: 24px;
  margin-bottom: 10px;
}
.profile.user {
  position: absolute;
  top: 10px;
  left: 10px;
}
.profile.author {
  position: absolute;
  top: 10px;
  left: 10px;
}
