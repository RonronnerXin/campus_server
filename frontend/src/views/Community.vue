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
      <div 
        v-for="post in posts" 
        :key="post.id" 
        class="post-card"
        @click="viewPostDetail(post.id)"
      >
        <div class="post-header">
          <div class="user-info">
            <img 
              :src="post.author_avatar || defaultAvatar" 
              :alt="post.author_name" 
              class="user-avatar" 
              @error="handleAvatarError"
            />
            <div class="user-details">
              <div class="user-name">{{ post.author_name }}</div>
              <div class="post-time">{{ formatDate(post.created_at) }}</div>
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
              <span>{{ post.likes_count }}</span>
            </button>
            
            <button class="action-btn" @click="toggleComments(post.id)">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0035 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ post.comments_count }}</span>
            </button>
            
            <button class="action-btn">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M8.68387 20.378C8.88616 20.5291 9.14288 20.6052 9.40232 20.5941C9.66177 20.5829 9.90968 20.4852 10.0982 20.3178L16 15L10 9L8.68387 20.378Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>分享</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { generalRequest } from '../services/genServ' // 根据实际路径调整

const router = useRouter()
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedTag = ref('')
const activeTab = ref('all')
const currentPage = ref(1)
const postsPerPage = 20
const totalPages = ref(1)
const totalCount = ref(0)
const posts = ref([])
const loading = ref(false)
const searchTimeout = ref(null)
const popularTags = ref(['技术分享', '学习笔记', '生活感悟', '旅行日记', '编程', '前端', '后端', '数据库'])

// 默认用户头像
const DEFAULT_AVATAR = 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face'
// 默认头像
const defaultAvatar = 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'

// 标签页配置
const tabs = ref([
  { id: 'all', name: '全部' },

])

// 计算要显示的页码（最多显示5个页码）
const displayedPages = computed(() => {
  if (totalPages.value <= 5) {
    return Array.from({ length: totalPages.value }, (_, i) => i + 1)
  }
  
  let start = Math.max(1, currentPage.value - 2)
  let end = Math.min(totalPages.value, start + 4)
  
  if (end - start < 4) {
    start = Math.max(1, end - 4)
  }
  
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

// 获取博客文章列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * postsPerPage,
      limit: postsPerPage,
      category: selectedCategory.value || undefined,
      tag: selectedTag.value || undefined,
      q: searchQuery.value || undefined
    }

    // 根据标签页类型添加参数
    if (activeTab.value === 'featured') {
      params.featured = true
    }

    const response = await generalRequest('/api/blog-posts/', {
      method: 'GET',
      params
    })

    if (response && response.data) {
      posts.value = response.data
      totalCount.value = response.count
      totalPages.value = response.total_pages
    } else {
      console.error('获取数据失败: 响应格式不正确', response)
      posts.value = []
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    posts.value = []
    if (error.response && error.response.status === 403) {
      if (confirm('您的登录状态已过期，请先登录')) {
        router.push('/login')
      }
    }
  } finally {
    loading.value = false
  }
}

// 获取博客封面图片
const getPostImage = (post) => {
  if (post.images && post.images.length > 0) {
    // 检查是否已经是完整URL
    if (post.images[0].startsWith('http')) {
      return post.images[0]
    }
    // 拼接完整的API地址
    return `http://localhost:8000${post.images[0]}`
  }

  // 默认图片逻辑
  const defaultImages = {
    'tech': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=300&h=200&fit=crop',
    'life': 'https://images.unsplash.com/photo-1483794344563-d27a8d18014e?w=300&h=200&fit=crop',
    'study': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=300&h=200&fit=crop',
    'travel': 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=300&h=200&fit=crop',
    'other': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=300&h=200&fit=crop'
  }
  return defaultImages[post.category] || defaultImages.other
}

// 获取用户头像
const getUserAvatar = (userId) => {
  // 这里可以根据用户ID获取用户头像，现在使用默认头像
  return DEFAULT_AVATAR
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取分类名称
const getCategoryName = (category) => {
  const categoryMap = {
    'tech': '技术',
    'life': '生活',
    'study': '学习',
    'travel': '旅行',
    'other': '其他'
  }
  return categoryMap[category] || '其他'
}

// 处理标签切换
const handleTabChange = (tabId) => {
  activeTab.value = tabId
  currentPage.value = 1
  fetchPosts()
}

// 处理筛选条件变化
const handleFilterChange = () => {
  currentPage.value = 1
  fetchPosts()
}

// 处理搜索（带防抖）
const handleSearchDebounce = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1
    fetchPosts()
  }, 500) // 500ms防抖
}

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchPosts()
  // 滚动到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 查看博客详情
const viewPostDetail = (postId) => {
  router.push(`/blogdetail/${postId}`)
}

// 点赞/取消点赞
const toggleLike = async (post) => {
  event.stopPropagation() // 阻止冒泡，避免触发卡片点击
  
  try {
    if (post.liked) {
      // 取消点赞
      await generalRequest(`/api/blog-posts/${post.id}/like`, {
        method: 'DELETE'
      })
      post.likes_count = Math.max(0, post.likes_count - 1)
    } else {
      // 点赞
      await generalRequest(`/api/blog-posts/${post.id}/like`, {
        method: 'POST'
      })
      post.likes_count += 1
    }
    post.liked = !post.liked
  } catch (error) {
    console.error('点赞操作失败:', error)
    if (error.response && error.response.status === 401) {
      if (confirm('请先登录后再进行操作')) {
        router.push('/login')
      }
    }
  }
}

// 默认头像加载失败时的处理函数
const handleAvatarError = (e) => {
  e.target.src = defaultAvatar
}

// 初始化加载数据
onMounted(() => {
  fetchPosts()
})

// 监听路由参数变化（如果有）
watch(() => router.currentRoute.value.query, (newQuery) => {
  if (newQuery.category) {
    selectedCategory.value = newQuery.category
  }
  if (newQuery.tag) {
    selectedTag.value = newQuery.tag
  }
  if (newQuery.q) {
    searchQuery.value = newQuery.q
  }
  if (newQuery.featured === 'true') {
    activeTab.value = 'featured'
  }
  
  // 如果有查询参数变化，重新获取数据
  fetchPosts()
}, { immediate: true })
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
  cursor: pointer;
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
  max-height: 200px; /* 添加最大高度限制 */
}

.post-images.images-1 .image-wrapper {
  max-height: 300px; /* 单张图片可以稍大一些 */
}

.post-images.images-2 .image-wrapper,
.post-images.images-3 .image-wrapper {
  max-height: 180px; /* 多张图片时设置更小的高度 */
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
  
  .image-wrapper {
    max-height: 160px; /* 移动端更小 */
  }
  
  .post-images.images-1 .image-wrapper {
    max-height: 200px; /* 移动端单张图片高度 */
  }
}
</style>