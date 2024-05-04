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

<el-container>
  <el-header>通讯记录</el-header>
  <el-container>
    <el-aside width="150px">
      <div v-for="(contact, index) in contacts" :key="index" class="contact-item" >
      <div :class="['contact-card', { 'highlighted': highlightedIndex === index}]" @click="selectContact(index)">
        <span class="contact-username">{{ contact }}</span>
        <div v-if="unreadContacts.includes(index) && highlightedIndex !== index" class="red-dot"></div>
        <el-button class="remove-button" @click="removeContact(index)">X</el-button>
      </div>
      </div>
    </el-aside>

      <el-container direction="vertical">
        <el-main class="main1">
          <div class="chat-container">
          <div class="chat-message">
            <div v-for="(message, index) in filteredMessages" :key="index" class="message-item">
              {{ message.content }}
            </div>
          </div>
        </div>
        </el-main>
              <div class="divider"></div>
        <el-main class="main2">
          <div class="main2-content">
         <el-input
          type="textarea"
          :rows="2"
          placeholder="请输入内容"
          v-model="textarea"
          maxlength="200"
          >
         </el-input>
         <el-button type="primary" @click="sendMessage">发送</el-button>
         </div>
        </el-main>
      </el-container>
  </el-container>
</el-container>

</div>
</template>

<script>

export default{
  data () {
    return {
      user: null,
      contacted_users: null,
      activeIndex: '3',
      activeIndex2: '3',
      textarea: '',
      websocket: null,
      contacts: [],
      highlightedIndex: -1,
      contactUser: null,
      messages: [], // 消息列表
      unreadContacts: [] // 未读消息的联系人索引列表
    }
  },
  computed: {
    filteredMessages () {
      return this.messages.filter(message => message.contactIndex === this.highlightedIndex)
    }
  },
  mounted () {
    this.user = sessionStorage.getItem('user').replace(/"/g, '')
    this.connectWebSocket()
    this.get_contacts()
  },
  methods: {
    connectWebSocket () {
      const socket = new WebSocket('ws://localhost:8000/chat/')

      socket.onopen = () => {
        console.log('WebSocket 连接已打开')
      }
      function scrollToBottom (element) {
        element.scrollTop = element.scrollHeight
      }
      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          const senderId = message.sender_id
          const messageContent = message.content
          const existingContactIndex = this.contacts.findIndex(contact => contact.id === senderId)

          if (existingContactIndex !== -1) {
            // 如果发送者已存在于联系人中，则将其置顶并更新消息内容
            const existingContact = this.contacts[existingContactIndex]
            existingContactIndex.message = messageContent
            this.contacts.splice(existingContactIndex, 1)
            this.contacts.unshift(existingContact)
            if (existingContactIndex !== this.highlightedIndex) {
              this.unreadContacts.push(existingContactIndex)
            }
            // 将该联系人从原位置删除，并将其添加到数组的开头，以实现置顶效果
          } else {
            // 如果发送者不存在于联系人中，则创建一个新的联系人对象并将其置顶
            const newContact = {
              id: senderId,
              message: messageContent
            }
            this.$axios.post('save_contact/', {
              contacted_users: senderId
            }).then(() => {
              this.get_contacts()
              this.contacts.unshift(newContact.id)
              this.unreadContacts.push(0)
            }).catch(error => {
              console.error('保存联系人出错:', error)
            })
          }
          // 创建聊天消息的容器元素
          const chatMessageElement = document.createElement('div')
          chatMessageElement.classList.add('chat-message')

          // 创建头像元素
          const avatarElement = document.createElement('el-avatar')
          avatarElement.classList.add('chat-avatar')
          avatarElement.setAttribute('size', 'small')
          avatarElement.setAttribute('round', 'true')
          avatarElement.innerText = message.sender_id

          // 创建气泡消息元素

          const cardElement = document.createElement('el-card')
          cardElement.classList.add('chat-card')
          cardElement.setAttribute('body-style', 'padding: 10px;')
          cardElement.setAttribute('shadow', 'never')
          cardElement.appendChild(document.createTextNode(message.content))
          chatMessageElement.appendChild(cardElement)
          const chatContainer = document.querySelector('.chat-container')
          if (message.sender_id === this.contactUser) {
            chatMessageElement.appendChild(avatarElement)
            chatMessageElement.appendChild(cardElement) // 添加样式，标识当前用户
            chatContainer.appendChild(chatMessageElement)
          }
          // 将头像和气泡消息元素添加到聊天消息容器中
          // 将聊天消息容器添加到聊天容器中
          // 接收到消息后滚动到底部
          scrollToBottom(chatContainer)
        } catch (error) {
          console.error('无效的 JSON 格式:', event.data)
        }
      }

      socket.onclose = () => {
        console.log('WebSocket 连接已关闭')
      }

      this.websocket = socket
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    },
    redirectToUserPage () {
      this.$router.push({
        path: '/usermessage'
      })
    },
    redirectTofirstPage () {
      this.$router.push({
        path: '/HelloWorld'
      })
    },
    selectContact (index) {
      this.highlightedIndex = index
      this.unreadContacts = this.unreadContacts.filter(item => item !== index)
      const chatContainer = document.querySelector('.chat-container')
      chatContainer.innerHTML = ''
      this.getMessagesForContact(index) // 获取选中联系人的消息
      this.contactUser = this.contacts[index]
      this.messages.forEach(message => {
        const chatMessageElement = document.createElement('div')
        chatMessageElement.classList.add('chat-message')

        // 创建头像元素
        const avatarElement = document.createElement('el-avatar')
        avatarElement.classList.add('chat-avatar')
        avatarElement.setAttribute('size', 'small')
        avatarElement.setAttribute('round', 'true')
        avatarElement.innerText = message.sender_id

        // 创建气泡消息元素
        const cardElement = document.createElement('el-card')
        cardElement.classList.add('chat-card')
        cardElement.setAttribute('body-style', 'padding: 10px;')
        cardElement.setAttribute('shadow', 'never')
        cardElement.appendChild(document.createTextNode(message.content))

        // 根据发送者的不同设置消息在左边或右边
        if (message.sender_id === this.user) {
          chatMessageElement.classList.add('self')
          chatMessageElement.appendChild(cardElement)
          chatMessageElement.appendChild(avatarElement)
        } else {
          chatMessageElement.classList.add('other')
          chatMessageElement.appendChild(avatarElement)
          chatMessageElement.appendChild(cardElement)
        }

        chatContainer.appendChild(chatMessageElement)
        function scrollToBottom () {
          chatContainer.scrollTop = chatContainer.scrollHeight
        }// 滚动到最底部

        scrollToBottom()
      })
    },
    async getMessagesForContact (index) {
      try {
        const receiver = this.contacts[index]
        const response = await this.$axios.post('get_chat_messages/', {
          receiver: receiver
        })
        console.log(this.contacts[index])
        if (response.status === 200) {
          const messages = response.data
          this.messages = messages
        } else {
          console.error('Failed to fetch chat messages')
        }
      } catch (error) {
        console.error('Error occurred while fetching chat messages:', error)
      }
    },
    sendMessage () {
      let message = {
        sender_id: this.user,
        receiver_id: this.contactUser,
        content: this.textarea
      }

      const chatContainerElement = document.querySelector('.chat-container')

      // 创建聊天消息容器
      const chatMessageElement = document.createElement('div')
      chatMessageElement.classList.add('chat-message')
      if (message.sender_id === this.user) {
        chatMessageElement.classList.add('sender') // 添加发送者类名
      } else {
        chatMessageElement.classList.add('receiver') // 添加接收者类名
      }

      // 创建头像元素
      const avatarElement = document.createElement('el-avatar')
      avatarElement.classList.add('chat-avatar')
      avatarElement.setAttribute('size', 'small')
      avatarElement.setAttribute('round', 'true')
      avatarElement.innerText = message.sender_id
      chatMessageElement.appendChild(avatarElement)

      // 创建文本消息元素
      const cardElement = document.createElement('el-card')
      cardElement.classList.add('chat-card')
      cardElement.setAttribute('body-style', 'padding: 10px;')
      cardElement.setAttribute('shadow', 'never')
      cardElement.classList.add('sender')
      cardElement.appendChild(document.createTextNode(message.content))
      chatMessageElement.appendChild(cardElement)

      chatContainerElement.appendChild(chatMessageElement)

      function scrollToBottom () {
        chatContainerElement.scrollTop = chatContainerElement.scrollHeight
      }// 滚动到最底部

      scrollToBottom() // 发送消息后滚动到底部
      this.websocket.send(JSON.stringify(message)) // 发送消息
      this.textarea = ' ' // 清空输入框
    },
    get_contacts () {
      this.$axios.get('/get_contacts')
        .then(response => {
          this.contacts = response.data.contacts // 将从后端获取的联系人列表存储在 data 中的 contacts 变量中
          console.log(this.contacts)
        })
        .catch(error => {
          console.error(error)
        })
    },
    removeContact (index) {
      this.contacts.splice(index, 1) // 从联系人列表中移除指定索引的联系人
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
 .el-header {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .main1 {
  position: relative;
  height: 300px;
}
.chat-container {
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}
 .el-container {
  display: flex;
}
.chat-avatar {
  width: 50px;
  height: 50px;
  background-color: lightgray;
  margin-right: 10px;
}
.chat-text {
  flex: 1;
}
.divider {
  border-top: 1px solid lightgray;
  margin: 10px 0;
}
.main2 {
  position: relative;
  height: 150px;
}
.main2-content {
    height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.main2-content .el-input {
  flex: 1;
  margin-bottom: 10px;
}

.main2-content .el-button {
  /* align-self: flex-end; */
  position: absolute;
  bottom: 10px;
  right: 10px;
}
.contact-item {
  margin-bottom: 10px;
}

.contact-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  height: 40px;
}

.contact-username {
  margin-right: 10px;
}

.remove-button {
  background-color: #ff0000;
  color: #ffffff;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}
.contact-card.highlighted {
  background-color: #799beb; /* 设置高亮时的背景颜色 */
}
.chat-message {
  display: flex;
  align-items: center;
}
.chat-message.sender {
  flex-direction: row-reverse;
}
.chat-avatar {
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.chat-card {
  max-width: 400px;
  background-color: #f2f2f2;
  border-radius: 10px;
  padding: 10px;
  display: inline-block;
  text-align: left
}
.chat-card.sender {
  max-width: 400px;
  background-color: #9ab3ee;
  border-radius: 10px;
  padding: 10px;
  display: inline-block;
  text-align: left;
  color: #ffffff;
}
.chat-card.self {
  max-width: 400px;
  background-color: #9ab3ee;
  border-radius: 10px;
  padding: 10px;
  display: inline-block;
  text-align: left;
  color: #ffffff;
}
.red-dot {
  width: 10px;
  height: 10px;
  background-color: red;
  border-radius: 50%;
}
.self {
  flex-direction: row;
  justify-content: flex-end;
}

.other {
  display: flex;
  align-items: center;
}
</style>
