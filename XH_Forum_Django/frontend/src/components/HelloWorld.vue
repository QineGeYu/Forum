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
  <el-menu-item index="1">首页</el-menu-item>
  <el-submenu index="2">
    <template slot="title">板块分类</template>
    <el-menu-item index="2-1" @click="filterByTag('影评')">影评</el-menu-item>
    <el-menu-item index="2-2" @click="filterByTag('旅游')">旅游</el-menu-item>
    <el-menu-item index="2-3" @click="filterByTag('编程')">编程</el-menu-item>
    <el-menu-item index="2-4" @click="filterByTag('其它')">其它</el-menu-item>
  </el-submenu>
  <el-menu-item index="3" @click="redirectToMessageCentre">消息中心</el-menu-item>
  <el-menu-item index="4" @click="redirectToUserPage"> 个人主页 </el-menu-item>
  <el-avatar class="profile user pull-right" :src="avatar_url">{{ user }}</el-avatar>
    <div class="search-container">
      <el-input
      v-model="searchText"
      placeholder="请输入关键词"
      @enter="performSearch"
      clearable
    >
      <el-button slot="append" icon="el-icon-search" @click="performSearch"></el-button>
    </el-input>
    </div>
</el-menu>

     <el-button class="floating-control" type="primary" round @click="toggleSort">
      {{ sortText }}
    </el-button>

<div class="block">
  <el-timeline class="card-line">
    <el-timeline-item v-for="item in displayData" :key="item.id" :timestamp="item.created_at" placement="top">
      <el-card class="card">
          <div class="avatar-wrapper" @click="goToUserPage(item.author_id)">
             <el-avatar class="profile author"
             :src="item.avatarUrl"
             >{{ item.author_id }}
             </el-avatar>

          </div>
        <h4 class="card-title">标题:{{ item.title }}</h4>
        <p class="card-description">摘要:  {{ item.description }}</p>
          <div class="like-section">
           <el-button v-if="!isSearching" @click="likePost(item)">
            <i class="el-icon-magic-stick"></i>  赞
            <span class="like-count">{{ item.likeCount }}</span>
            </el-button>
            <el-button @click="goToPostDetail(item)">
            <i class="el-icon-chat-line-round"></i>  评论
            <span class="like-count">{{ item.comments }}</span>
            </el-button>
        </div>
        <div class="tag-section">#{{ item.tag }}</div>
      </el-card>
    </el-timeline-item>
  </el-timeline>
</div>
</div>
</template>

<script>
export default{
  data () {
    return {
      cards: [],
      user: null,
      activeIndex: '1',
      activeIndex2: '1',
      searchText: '',
      sortText: '最新',
      searchResults: [],
      filteredPosts: [],
      avatar_url: ''
    }
  },
  computed: {
    displayData () {
      if (this.searchText && this.searchResults.length > 0) {
        return this.searchResults
      } else if (this.filteredPosts.length > 0) {
        return this.filteredPosts
      } else {
        return this.cards
      }
    },
    isSearching () {
      return this.searchText !== '' && this.searchResults.length > 0
    }
  },
  mounted () {
    this.user = sessionStorage.getItem('user').replace(/"/g, '')
    sessionStorage.setItem('user', JSON.stringify(this.user))
    console.log(this.user)
    this.getPost()
    this.saveKey()
    this.getAvatar()
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.searchResults = []
      this.filteredPosts = []
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
    getPost () {
      this.$axios.get('show_post/')
        .then(response => {
          this.cards = JSON.parse(response.data.posts)
          if (this.sortText === '最新') {
            this.cards.reverse()
          } else {
            this.cards.sort((a, b) => {
              const hotnessA = a.likeCount + a.comments // 帖子A的热度
              const hotnessB = b.likeCount + b.comments // 帖子B的热度
              return hotnessB - hotnessA // 按热度排序，降序排列
            })
          }

          Promise.all(this.cards.map(item => this.getOtherAvatar(item.author_id)))
            .then(avatarUrls => {
              // 将获取到的头像URL分别存储在帖子对象中
              avatarUrls.forEach((avatarUrl, index) => {
                this.cards[index].avatarUrl = avatarUrl
              })
              console.log(this.cards)
            })
            .catch(error => {
              console.error('Error fetching avatars:', error)
            })

          this.performSearch()
        })
        .catch(error => {
          alert('请登录后再访问')
          console.error('Error:', error)
          this.$axios.push({
            path: '/Login'
          })
        })
    },
    goToUserPage (authorId) {
      // 在当前网页中进行导航，并传递 authorId 参数
      this.$router.push({
        path: '/UserPage', query: { authorId: authorId }
      })
    },
    redirectToUserPage () {
      this.$router.push({
        path: '/usermessage'
      })
    },
    redirectToMessageCentre () {
      this.$router.push({
        path: '/MessageCentre'
      })
    },
    performSearch () {
      this.$axios.get('search/', {
        params: {
          keyword: this.searchText
        }
      })
        .then(response => {
          this.searchResults = response.data
        })
        .catch(error => {
          console.error('搜索失败:', error)
        })
    },
    async saveKey () {
      const jse = new this.$jsEncrypt()
      jse.getKey()
      this.$axios.post('savePublicKey/', {
        publicKey: jse.getPublicKey(),
        privateKey: jse.getPrivateKey()
      })
        .then(response => {
          // 请求成功后的处理逻辑
          console.log(response.data)
        })
        .catch(error => {
          // 请求失败后的处理逻辑
          console.error(error)
        })
    },
    filterByTag (tag) {
      this.filteredPosts = this.cards.filter(post => {
        return post.tag === tag
      })
      console.log(this.filteredPosts)
    },
    toggleSort () {
      this.sortText = this.sortText === '最新' ? '最热' : '最新'
    },
    getOtherAvatar (username) {
      return this.$axios.get(`/get_avatar2/${username}`, {
        responseType: 'arraybuffer' // 告诉 Axios 以二进制数组的形式接收响应
      })
        .then(response => {
          const blob = new Blob([response.data], { type: 'image/png' })
          return new Promise((resolve, reject) => {
            const url = URL.createObjectURL(blob)
            resolve(url)
          })
        })
        .catch(error => {
          console.error('Error fetching avatar:', error)
          return Promise.resolve('')
        })
    },
    getAvatar () {
      this.$axios.get('get_avatar/', {
        responseType: 'arraybuffer' // 告诉 Axios 以二进制数组的形式接收响应
      })
        .then(response => {
          const blob = new Blob([response.data], { type: 'image/png' })
          const imageUrl = URL.createObjectURL(blob)
          this.avatar_url = imageUrl
        })
        .catch(error => console.error('Error fetching avatar:', error))
    }
  }
}
</script>

<style scoped>
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
.profile.user {
 margin-left: 10px;
}
.profile.author {
  position: absolute;
  top: 10px;
  left: 10px;
}
.pull-right {
  margin-left: auto;
}
.search-container {
  width: 300px; /* 设置容器宽度 */
}
.avatar-wrapper {
  cursor: pointer;
}
.floating-control {
  position: fixed;
  top: 70px; /* 距离顶部20px */
  right: 70px; /* 距离右侧20px */
  z-index: 999; /* 控件位于最顶层 */
}
.tag-section {
  position: absolute;
  bottom: 0px;
  left: 30px;
  background-color: #acebe9;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  color: #333;
}
</style>
