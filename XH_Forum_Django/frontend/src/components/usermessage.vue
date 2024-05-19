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
  <el-menu-item index="3" @click="redirectToMessageCentre">消息中心</el-menu-item>
  <el-menu-item index="4" @click="redirectToUserPage"> 个人主页 </el-menu-item>

  <div @click="showUploadDialog = true" style="cursor: pointer;">
  <el-avatar
    class="profile user pull-right"
    :src="avatar_url"
     >{{ user }}</el-avatar>
     </div>

         <el-dialog
      title="上传头像"
      :visible.sync="showUploadDialog"
      width="30%"
      :close-on-click-modal="false"
    >
          <img v-if="dialogImageUrl" :src="dialogImageUrl" class="circular-image" />
           <el-upload
              action="publish_singleMessage/"
              :on-change="handleFileChange"
              :show-file-list="false"
              :file-list="fileList"
           >
        <el-button size="small" type="primary">点击上传</el-button>
      </el-upload>
      <br>
      <el-button size="small" type="primary" @click="handleConfirm">确定</el-button>
    </el-dialog>
</el-menu>
  <div class="descriptions-container">
  <el-descriptions class="margin-top" title="个人信息" :column="3" border size="medium">
   <template slot="extra">
   <el-button type="primary" @click="dialogFormVisible2 = true">编辑资料</el-button>
   <el-dialog title="编辑资料" :visible.sync="dialogFormVisible2">
  <el-form :model="form2">
        <el-form-item label="电子邮箱">
          <el-input v-model="email"></el-input>
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="name"></el-input>
        </el-form-item>
        <el-form-item label="个性签名">
          <el-input type="textarea" v-model="PersonalSignature"></el-input>
        </el-form-item>

  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible2 = false">取 消</el-button>
    <el-button type="primary" @click="publishSingleMessage">确 定</el-button>
  </div>
</el-dialog>

   <el-button type="primary" @click="dialogFormVisible = true">发布</el-button>
<el-dialog title="发布帖子" :visible.sync="dialogFormVisible">
  <el-form :model="form">

        <el-form-item label="标题">
          <el-input v-model="title"></el-input>
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="description"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-input type="textarea" v-model="content"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="tag"></el-input>
        </el-form-item>
        <el-form-item label="隐私帖子">
          <el-checkbox v-model="isPrivate">设置为隐私帖子</el-checkbox>
        </el-form-item>

  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="publishPost">确 定</el-button>
  </div>
</el-dialog>
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
      {{ message.name }}
    </el-descriptions-item>

    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-timer"></i>
        加入时间
      </template>
      {{ message.date_joined }}
    </el-descriptions-item>

    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-milk-tea"></i>
        个性签名
      </template>
      {{ message.PersonalSignature }}
    </el-descriptions-item>

  </el-descriptions>
  </div>
<div class="block">
  <el-timeline class="card-line">
    <el-timeline-item v-for="item in cards" :key="item.id" :timestamp="item.created_at" placement="top">
      <el-card class="card">
         <div class="privacy-icon" @click="togglePrivacy(item)">
            <i class="el-icon-lock" v-if="item.is_private"></i>
            <i class="el-icon-unlock" v-else></i>
        </div>
          <div class="avatar-wrapper">
             <el-avatar class="profile author" :src="avatar_url">{{ item.author_id }}</el-avatar>
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
        <div class="tag-section">#{{ item.tag }}</div>
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
      dialogFormVisible2: false,
      showUploadDialog: false,
      form: {},
      title: null,
      description: null,
      content: null,
      isPrivate: false,
      form2: {},
      email: null,
      name: null,
      tag: null,
      PersonalSignature: null,
      fileList: [],
      dialogImageUrl: '',
      avatar_url: ''
    }
  },
  mounted () {
    this.user = sessionStorage.getItem('user').replace(/"/g, '')
    console.log(this.user)
    this.getPost()
    this.getUserMessage()
    this.getAvatar()
  },
  methods: {
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
    redirectToMessageCentre () {
      this.$router.push({
        path: '/MessageCentre'
      })
    },
    getPost () {
      this.$axios.get('show_user_post/')
        .then(response => {
          this.cards = JSON.parse(response.data.posts)
          this.cards.reverse()
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
        user: this.user,
        isPrivate: this.isPrivate,
        tag: this.tag
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
    },
    publishSingleMessage () {
      const SingleMessageData = {
        name: this.name,
        email: this.email,
        PersonalSignature: this.PersonalSignature
      }
      this.$axios.post('publish_singleMessage/', SingleMessageData)
        .then(response => {
          // 处理请求成功的响应
          alert('编辑资料成功')
          this.name = ''
          this.email = ''
          this.PersonalSignature = ''
          window.location.reload()
        })
        .catch(error => {
          console.error('资料编辑失败', error)
        })
        .finally(() => {
          // 请求完成后的清理工作，可选
        })
      this.dialogFormVisible2 = false
    },
    togglePrivacy (item) {
      item.is_private = !item.is_private // 切换is_private字段的值
      // 发送异步请求将更改保存到后端
      this.$axios.post('update_post_privacy/', { post_id: item.id, is_private: item.is_private })
        .then(response => {
          // 处理成功响应
          console.log('Post privacy updated successfully')
        })
        .catch(error => {
          // 处理错误
          console.error('Failed to update post privacy', error)
          // 恢复is_private字段的值，以保持与后端同步
          item.is_private = !item.is_private
        })
    },
    handleFileChange (file) {
      this.fileList.push(file)
      console.log('文件已选中：', file)
      this.fileList = [file]
      this.dialogImageUrl = URL.createObjectURL(file.raw)
    },
    handleConfirm () {
      if (this.fileList.length === 0) {
        alert('请先选择要上传的头像文件')
        return
      }

      // 构建 FormData 对象，用于包装上传的头像文件和其他数据
      const formData = new FormData()
      formData.append('avatar', this.fileList[0].raw)
      // 其他数据
      formData.append('username', this.username)

      // 发送数据到后端进行处理
      this.$axios.post('edit_profile/', formData)
        .then(response => {
          // 处理请求成功的响应
          alert('头像上传成功')
          // 可以根据需要执行其他操作，例如关闭对话框或刷新页面等
        })
        .catch(error => {
          console.error('上传失败', error)
          alert('头像上传失败，请重试')
        })
    },
    getAvatar () {
      this.$axios.get('get_avatar/', {
        responseType: 'arraybuffer' // 告诉 Axios 以二进制数组的形式接收响应
      })
        .then(response => {
          const blob = new Blob([response.data], { type: 'image/png' })
          const imageUrl = URL.createObjectURL(blob)
          console.log(imageUrl)
          this.avatar_url = imageUrl
        })
        .catch(error => console.error('Error fetching avatar:', error))
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
.privacy-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  color: #888;
}

.privacy-icon i {
  margin-left: 5px;
}

.privacy-icon i.el-icon-unlock {
  color: green;
}
.tag-section {
  position: absolute;
  bottom: 0px;
  left: 30px;
  background-color: #a4c4f0;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  color: #18181c;
}
.circular-image {
  border-radius: 50%;
  width: 100px;
  height: 100px;
}
</style>
