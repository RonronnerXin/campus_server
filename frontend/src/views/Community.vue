<template>
  <div class="community">
    <div class="page-header">
      <h1>社区分享</h1>
      <div class="filter-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>

    <div class="posts-container">
      <div v-for="post in filteredPosts" :key="post.id" class="post-card">
        <div class="post-header">
          <div class="user-info">
            <img :src="post.user.avatar" :alt="post.user.name" class="user-avatar" />
            <div class="user-details">
              <div class="user-name">{{ post.user.name }}</div>
              <div class="post-time">{{ post.time }}</div>
            </div>
          </div>
          <div class="post-tag" :class="post.category">{{ getCategoryName(post.category) }}</div>
        </div>
        
        <div class="post-content">
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-text">{{ post.content }}</p>
          
          <div v-if="post.images && post.images.length > 0" class="post-images" :class="'images-' + post.images.length">
            <div v-for="(image, index) in post.images" :key="index" class="image-wrapper">
              <img :src="image" :alt="`图片${index + 1}`" class="post-image" />
            </div>
          </div>
        </div>
        
        <div class="post-footer">
          <div class="post-actions">
            <button class="action-btn" :class="{ active: post.liked }" @click="toggleLike(post)">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M7 22H4C3.46957 22 2.96086 21.7893 2.58579 21.4142C2.21071 21.0391 2 20.5304 2 20V13C2 12.4696 2.21071 11.9609 2.58579 11.5858C2.96086 11.2107 3.46957 11 4 11H7M14 9V5C14 4.20435 13.6839 3.44129 13.1213 2.87868C12.5587 2.31607 11.7956 2 11 2L7 11V22H18.28C18.7623 22.0055 19.2304 21.8364 19.5979 21.524C19.9654 21.2116 20.2077 20.7769 20.28 20.3L21.66 11.3C21.7035 11.0134 21.6842 10.7207 21.6033 10.4423C21.5225 10.1638 21.3821 9.90629 21.1919 9.68751C21.0016 9.46873 20.7661 9.29393 20.5016 9.17522C20.2371 9.0565 19.9499 8.99672 19.66 9H14Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ post.likes }}</span>
            </button>
            
            <button class="action-btn" @click="toggleComments(post.id)">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0035 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ post.comments.length }}</span>
            </button>
            
            <button class="action-btn">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M8.68387 20.378C8.88616 20.5291 9.14288 20.6052 9.40232 20.5941C9.66177 20.5829 9.90968 20.4852 10.0982 20.3178L16 15L10 9L8.68387 20.378Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>分享</span>
            </button>
          </div>
        </div>
        
        <!-- 评论区域 -->
        <div v-if="showComments[post.id]" class="comments-section">
          <div class="comment-input">
            <img src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face" alt="我的头像" class="comment-avatar" />
            <div class="comment-input-wrapper">
              <input 
                type="text" 
                v-model="commentInputs[post.id]" 
                placeholder="写下你的评论..."
                class="comment-text-input"
                @keyup.enter="addComment(post.id)"
              />
              <button class="comment-submit" @click="addComment(post.id)">发送</button>
            </div>
          </div>
          
          <div class="comments-list">
            <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
              <img :src="comment.user.avatar" :alt="comment.user.name" class="comment-avatar" />
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-user">{{ comment.user.name }}</span>
                  <span class="comment-time">{{ comment.time }}</span>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const activeTab = ref('all')
const showComments = reactive({})
const commentInputs = reactive({})

const tabs = ref([
  { id: 'all', name: '全部' },
  { id: 'study', name: '技术' },
  { id: 'life', name: '生活' },
  { id: 'food', name: '学习' },
  { id: 'activity', name: '旅行' }
])

const posts = ref([
  {
    id: 1,
    title: '图书馆自习位推荐',
    content: '分享几个图书馆的绝佳自习位置，安静且光线充足，特别适合考研党！三楼靠窗的位置视野很好，四楼的讨论区适合小组学习。记得早点去占位哦～',
    category: 'study',
    time: '2小时前',
    likes: 24,
    liked: false,
    user: {
      name: '学霸小王',
      avatar: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face'
    },
    images: [
      'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop',
      'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop'
    ],
    comments: [
      {
        id: 1,
        content: '谢谢分享！明天就去试试',
        time: '1小时前',
        user: {
          name: '努力学习中',
          avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=40&h=40&fit=crop&crop=face'
        }
      }
    ]
  },
  {
    id: 2,
    title: '食堂新品尝鲜报告',
    content: '今天试了食堂新推出的麻辣香锅，味道真的不错！料很足，价格也合理，15元一份。推荐大家去试试，就在二楼新开的窗口。',
    category: 'food',
    time: '4小时前',
    likes: 18,
    liked: true,
    user: {
      name: '美食探索者',
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=40&h=40&fit=crop&crop=face'
    },
    images: [
      'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop'
    ],
    comments: [
      {
        id: 1,
        content: '看起来就很香！',
        time: '3小时前',
        user: {
          name: '吃货小李',
          avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=40&h=40&fit=crop&crop=face'
        }
      },
      {
        id: 2,
        content: '明天中午就去试试',
        time: '2小时前',
        user: {
          name: '张同学',
          avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=40&h=40&fit=crop&crop=face'
        }
      }
    ]
  },
  {
    id: 3,
    title: '宿舍生活小贴士',
    content: '分享一些宿舍生活的实用小技巧：1. 用收纳盒整理桌面 2. 定期清洁空调滤网 3. 合理安排作息时间 4. 与室友保持良好沟通。希望对大家有帮助！',
    category: 'life',
    time: '1天前',
    likes: 32,
    liked: false,
    user: {
      name: '生活达人',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'
    },
    images: [],
    comments: [
      {
        id: 1,
        content: '很实用的建议！',
        time: '20小时前',
        user: {
          name: '室友A',
          avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face'
        }
      }
    ]
  },
  {
    id: 4,
    title: '周末音乐节活动预告',
    content: '本周六晚上7点，学生活动中心将举办校园音乐节，有多个社团表演，还有抽奖环节！免费入场，欢迎大家来参加～',
    category: 'activity',
    time: '2天前',
    likes: 45,
    liked: true,
    user: {
      name: '活动组织者',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=40&h=40&fit=crop&crop=face'
    },
    images: [
      'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop'
    ],
    comments: [
      {
        id: 1,
        content: '期待！一定会去的',
        time: '1天前',
        user: {
          name: '音乐爱好者',
          avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=40&h=40&fit=crop&crop=face'
        }
      }
    ]
  }
])

const filteredPosts = computed(() => {
  if (activeTab.value === 'all') {
    return posts.value
  }
  return posts.value.filter(post => post.category === activeTab.value)
})

const getCategoryName = (category) => {
  const categoryMap = {
    study: '学习交流',
    life: '校园生活',
    food: '美食分享',
    activity: '活动推荐'
  }
  return categoryMap[category] || '其他'
}

const toggleLike = (post) => {
  post.liked = !post.liked
  post.likes += post.liked ? 1 : -1
}

const toggleComments = (postId) => {
  showComments[postId] = !showComments[postId]
  if (!commentInputs[postId]) {
    commentInputs[postId] = ''
  }
}

const addComment = (postId) => {
  const content = commentInputs[postId]?.trim()
  if (!content) return
  
  const post = posts.value.find(p => p.id === postId)
  if (post) {
    post.comments.push({
      id: Date.now(),
      content: content,
      time: '刚刚',
      user: {
        name: '我',
        avatar: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face'
      }
    })
    commentInputs[postId] = ''
  }
}
</script>

<style scoped>
.community {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f3f4;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
}

.filter-tabs {
  display: flex;
  gap: 8px;
}

.tab {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #6b7280;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab:hover {
  background: #f3f4f6;
  color: #374151;
}

.tab.active {
  background: #667eea;
  color: #ffffff;
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  border: 1px solid #f1f3f4;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
}

.post-time {
  font-size: 12px;
  color: #9ca3af;
}

.post-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: #ffffff;
}

.post-tag.study {
  background: #3b82f6;
}

.post-tag.life {
  background: #10b981;
}

.post-tag.food {
  background: #f59e0b;
}

.post-tag.activity {
  background: #ef4444;
}

.post-content {
  margin-bottom: 16px;
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.post-text {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 12px;
}

.post-images {
  display: grid;
  gap: 8px;
  border-radius: 8px;
  overflow: hidden;
}

.post-images.images-1 {
  grid-template-columns: 1fr;
}

.post-images.images-2 {
  grid-template-columns: 1fr 1fr;
}

.post-images.images-3 {
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.post-images.images-3 .image-wrapper:first-child {
  grid-row: 1 / 3;
}

.image-wrapper {
  aspect-ratio: 16/9;
  overflow: hidden;
  border-radius: 8px;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.post-image:hover {
  transform: scale(1.05);
}

.post-footer {
  border-top: 1px solid #f1f3f4;
  padding-top: 16px;
}

.post-actions {
  display: flex;
  gap: 24px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #6b7280;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.action-btn.active {
  color: #667eea;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.comments-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f1f3f4;
}

.comment-input {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-input-wrapper {
  flex: 1;
  display: flex;
  gap: 8px;
}

.comment-text-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  font-size: 14px;
  background: #f9fafb;
  transition: all 0.2s ease;
}

.comment-text-input:focus {
  outline: none;
  border-color: #667eea;
  background: #ffffff;
}

.comment-submit {
  padding: 8px 16px;
  background: #667eea;
  color: #ffffff;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.comment-submit:hover {
  background: #5a67d8;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-user {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.comment-time {
  font-size: 12px;
  color: #9ca3af;
}

.comment-text {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .filter-tabs {
    width: 100%;
    overflow-x: auto;
  }
  
  .tab {
    white-space: nowrap;
  }
  
  .post-images.images-2,
  .post-images.images-3 {
    grid-template-columns: 1fr;
  }
  
  .post-images.images-3 .image-wrapper:first-child {
    grid-row: auto;
  }
  
  .post-actions {
    gap: 16px;
  }
  
  .comment-input-wrapper {
    flex-direction: column;
    gap: 8px;
  }
}
</style>