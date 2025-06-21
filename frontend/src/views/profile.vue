<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>个人中心</h1>
      <div class="profile-actions">
        <button class="action-btn primary" @click="createNewItem">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          发布新内容
        </button>
      </div>
    </div>

    <div class="user-info-card">
      <div class="user-avatar-container">
        <img :src="userInfo.avatar || defaultAvatar" alt="用户头像" class="user-avatar" />
        <button class="edit-avatar-btn" @click="updateAvatar">⇧
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
      <div class="user-details">
        <h2 class="user-name">{{ userInfo.username }}</h2>
        <p class="user-email">{{ userInfo.email }}</p>
        <div class="user-stats">
          <div class="stat-item">
            <span class="stat-value">{{ userStats.posts }}</span>
            <span class="stat-label">博客</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ userStats.lostItems }}</span>
            <span class="stat-label">失物招领</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ userStats.comments }}</span>
            <span class="stat-label">评论</span>
          </div>
        </div>
      </div>
      <div class="user-actions">
        <button class="edit-profile-btn" @click="editProfile">
          编辑资料
        </button>
      </div>
    </div>

    <div class="content-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab', { active: activeTab === tab.id }]"
        @click="handleTabChange(tab.id)"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- 筛选器 -->
    <div class="filter-bar" v-if="activeTab === 'posts' || activeTab === 'lostItems'">
      <div class="filter-group">
        <label>状态:</label>
        <select v-model="filters.status" class="filter-select" @change="handleFilterChange">
          <option value="">全部</option>
          <template v-if="activeTab === 'posts'">
            <option value="draft">草稿</option>
            <option value="published">已发布</option>
          </template>
          <template v-else>
            <option value="unclaimed">未认领</option>
            <option value="claimed">已认领</option>
            <option value="expired">已过期</option>
          </template>
        </select>
      </div>
      <div class="filter-group" v-if="activeTab === 'posts'">
        <label>分类:</label>
        <select v-model="filters.category" class="filter-select" @change="handleFilterChange">
          <option value="">全部</option>
          <option value="tech">技术</option>
          <option value="life">生活</option>
          <option value="study">学习</option>
          <option value="travel">旅行</option>
          <option value="other">其他</option>
        </select>
      </div>
      <div class="filter-group" v-if="activeTab === 'lostItems'">
        <label>类型:</label>
        <select v-model="filters.type" class="filter-select" @change="handleFilterChange">
          <option value="">全部</option>
          <option value="lost">寻物启事</option>
          <option value="found">招领启事</option>
        </select>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 无数据状态 -->
    <div v-else-if="!loading && totalCount==0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" class="empty-icon">
        <path d="M9 13h6m-3-3v6M12 21a9 9 0 1 1 0-18 9 9 0 0 1 0 18z" stroke="currentColor" stroke-width="2"/>
      </svg>
      <p>{{ getEmptyStateMessage() }}</p>
      <button class="create-btn" @click="createNewItem">{{ getCreateButtonText() }}</button>
    </div>

    <!-- 博客列表 -->
    <div v-else-if="activeTab === 'posts'" class="items-grid">
      <div v-for="post in items" :key="post.id" class="item-card">
        <div class="item-image-container">
          <img :src="getPostImage(post)" :alt="post.title" class="item-image" />
          <span class="item-status" :class="post.status">{{ getPostStatusName(post.status) }}</span>
          <span v-if="post.featured" class="item-featured">推荐</span>
        </div>
        <div class="item-content">
          <h3 class="item-title">{{ post.title }}</h3>
          <div class="item-details">
            <div class="detail-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ formatDate(post.published_at || post.created_at) }}</span>
            </div>
            <div class="detail-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ post.views_count }}</span>
            </div>
          </div>
          <p class="item-description">{{ post.summary }}</p>
          <div class="item-footer">
            <div class="item-stats">
              <div class="stat-item">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M14 10h3v2h-3v3h-2v-3H9v-2h3V7h2v3z" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span>{{ post.likes_count }}</span>
              </div>
              <div class="stat-item">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0035 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span>{{ post.comments_count }}</span>
              </div>
            </div>
            <div class="item-actions">
              <button class="action-btn" @click.stop="editItem(post)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                编辑
              </button>
              <button class="action-btn delete" @click.stop="deleteItem(post)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 失物招领列表 -->
    <div v-else-if="activeTab === 'lostItems'" class="items-grid">
      <div v-for="item in items" :key="item.id" class="item-card">
        <div class="item-image-container">
          <img :src="getItemImage(item)" :alt="item.title" class="item-image" />
          <span class="item-status" :class="item.type">{{ item.type === 'lost' ? '寻物启事' : '招领启事' }}</span>
          <span class="item-status-tag" :class="item.status">{{ getLostItemStatusName(item.status) }}</span>
        </div>
        <div class="item-content">
          <h3 class="item-title">{{ item.title }}</h3>
          <div class="item-details">
            <div class="detail-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ formatDate(item.time) }}</span>
            </div>
            <div class="detail-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M17.657 16.657L13.414 20.9C13.039 21.2746 12.5303 21.4851 12 21.4851C11.4697 21.4851 10.961 21.2746 10.586 20.9L6.343 16.657C5.22422 15.5381 4.46234 14.1127 4.15369 12.5608C3.84504 11.009 4.00349 9.40047 4.60901 7.93868C5.21452 6.4769 6.2399 5.22749 7.55548 4.34846C8.87107 3.46943 10.4178 3 12 3C13.5822 3 15.1289 3.46943 16.4445 4.34846C17.7601 5.22749 18.7855 6.4769 19.391 7.93868C19.9965 9.40047 20.155 11.009 19.8463 12.5608C19.5377 14.1127 18.7758 15.5381 17.657 16.657V16.657Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ item.location }}</span>
            </div>
          </div>
          <p class="item-description">{{ item.description }}</p>
          <div class="item-footer">
            <div class="item-stats">
              <div class="stat-item">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/>
                  <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span>{{ item.views_count || 0 }}</span>
              </div>
            </div>
            <div class="item-actions">
              <button class="action-btn" @click.stop="updateItemStatus(item)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                更新状态
              </button>
              <button class="action-btn" @click.stop="editItem(item)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                编辑
              </button>
              <button class="action-btn delete" @click.stop="deleteItem(item)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 评论列表 -->
    <div v-else-if="activeTab === 'comments'" class="comments-list">
      <div v-for="comment in items" :key="comment.id" class="comment-card">
        <div class="comment-header">
          <div class="comment-info">
            <span class="comment-type">{{ comment.post_id ? '博客评论' : '失物招领评论' }}</span>
            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
          </div>
          <button class="action-btn delete" @click="deleteComment(comment)">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="comment-content">
          <p>{{ comment.content }}</p>
        </div>
        <div class="comment-footer">
          <button class="view-post-btn" @click="viewRelatedPost(comment)">
            查看原文
          </button>
          <div class="comment-stats">
            <div class="stat-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M14 10h3v2h-3v3h-2v-3H9v-2h3V7h2v3z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ comment.likes_count || 0 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页控件 -->
    <div v-if="totalPages > 1" class="pagination">
      <button class="page-btn prev" :disabled="currentPage === 1" @click="handlePageChange(currentPage - 1)">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M15 19L8 12L15 5" stroke="currentColor" stroke-width="2"/>
        </svg>
      </button>
      <div class="page-numbers">
        <button 
          v-for="page in displayedPages" 
          :key="page" 
          :class="['page-number', { active: currentPage === page }]"
          @click="handlePageChange(page)"
        >
          {{ page }}
        </button>
      </div>
      <button class="page-btn next" :disabled="currentPage === totalPages" @click="handlePageChange(currentPage + 1)">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M9 5L16 12L9 19" stroke="currentColor" stroke-width="2"/>
        </svg>
      </button>
    </div>

    <!-- 状态更新弹窗 -->
    <div v-if="showStatusModal" class="modal-overlay" @click="showStatusModal = false">
      <div class="modal-content" @click.stop>
        <h3>更新状态</h3>
        <div class="modal-body">
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" v-model="selectedStatus" value="unclaimed">
              <span>未认领</span>
            </label>
            <label class="radio-label">
              <input type="radio" v-model="selectedStatus" value="claimed">
              <span>已认领</span>
            </label>
            <label class="radio-label">
              <input type="radio" v-model="selectedStatus" value="expired">
              <span>已过期</span>
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="showStatusModal = false">取消</button>
          <button class="btn primary" @click="confirmStatusUpdate">确认</button>
        </div>
      </div>
    </div>

    <!-- 添加编辑资料对话框 -->
    <el-dialog
      v-model="profileDialogVisible"
      title="编辑个人资料"
      width="600px"
    >
      <div class="profile-form">
        <el-form :model="profileForm" label-width="100px">
          <el-form-item label="用户名">
            <el-input v-model="profileForm.username" />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="profileForm.email" disabled />
          </el-form-item>
        </el-form>
        <div class="dialog-actions">
          <el-button type="primary" @click="submitProfile">保存修改</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { generalRequest } from '../services/genServ' // 根据实际路径调整
import { ElDialog, ElForm, ElFormItem, ElInput, ElButton, ElMessage } from 'element-plus'
import { success } from '../tools/messageBox'
const router = useRouter()
const activeTab = ref('posts')
const currentPage = ref(1)
const itemsPerPage = 12
const totalPages = ref(1)
const totalCount = ref(0)
const items = ref([])
const loading = ref(false)
const showStatusModal = ref(false)
const selectedStatus = ref('')
const currentItem = ref(null)
const defaultAvatar = 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=80&h=80&fit=crop'

// 用户信息
const userInfo = ref({
  id: '',
  username: '',
  email: '',
  avatar: null
})

// 用户统计数据
const userStats = ref({
  posts: 0,
  lostItems: 0,
  comments: 0
})

// 标签页配置
const tabs = [
  { id: 'posts', name: '我的博客' },
  { id: 'lostItems', name: '我的失物招领' },
]

// 筛选条件
const filters = ref({
  status: '',
  category: '',
  type: ''
})

// 个人资料对话框
const profileDialogVisible = ref(false)
const profileForm = ref({
  username: '',
  email: ''
})

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

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const response = await generalRequest('/api/users/me', {
      method: 'GET'
    })
    
    if (response) {
      userInfo.value = response
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    if (error.response && error.response.status === 401) {
      router.push('/login')
    }
  }
}


// 获取博客文章列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * itemsPerPage,
      limit: itemsPerPage,
      status: filters.value.status || undefined,
      category: filters.value.category || undefined
    }

    const response = await generalRequest('/api/blog-posts/my', {
      method: 'GET',
      params
    })
    console.log('获取博客列表响应:', response)

    if (response && response.data) {
      items.value = response.data
      totalCount.value = response.count
      userStats.value.posts = response.count
      totalPages.value = response.total_pages
    } else {
      items.value = []
    }
  } catch (error) {
    console.error('获取博客列表失败:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

// 获取失物招领列表
const fetchLostItems = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * itemsPerPage,
      limit: itemsPerPage,
      status: filters.value.status || undefined,
      type: filters.value.type || undefined
    }

    const response = await generalRequest('/api/lost-items/my', {
      method: 'GET',
      params
    })

    if (response && response.data) {
      items.value = response.data
      totalCount.value = response.count
      userStats.value.lostItems = response.count
      totalPages.value = response.total_pages
    } else {
      items.value = []
    }
  } catch (error) {
    console.error('获取失物招领列表失败:', error)
    items.value = []
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

// 获取失物招领图片
const getItemImage = (item) => {
  if (item.images && item.images.length > 0) {
    // 检查是否已经是完整URL
    if (item.images[0].startsWith('http')) {
      return item.images[0]
    }
    // 拼接完整的API地址
    return `http://localhost:8000${item.images[0]}`
  }

  // 默认图片逻辑
  const defaultImages = {
    'card': 'https://images.unsplash.com/photo-1586223287834-f73bd5e6a967?w=300&h=200&fit=crop',
    'electronics': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=200&fit=crop',
    'books': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=200&fit=crop',
    'clothing': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=300&h=200&fit=crop',
    'other': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=200&fit=crop'
  }
  return defaultImages[item.category] || defaultImages.other
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

// 获取博客状态名称
const getPostStatusName = (status) => {
  const statusMap = {
    'draft': '草稿',
    'published': '已发布'
  }
  return statusMap[status] || '未知'
}

// 获取失物招领状态名称
const getLostItemStatusName = (status) => {
  const statusMap = {
    'unclaimed': '未认领',
    'claimed': '已认领',
    'expired': '已过期'
  }
  return statusMap[status] || '未知'
}

// 获取空状态提示信息
const getEmptyStateMessage = () => {
  if (activeTab.value === 'posts') {
    return '您还没有发布任何博客文章'
  } else if (activeTab.value === 'lostItems') {
    return '您还没有发布任何失物招领信息'
  } else {
    return '您还没有发表任何评论'
  }
}

// 获取创建按钮文本
const getCreateButtonText = () => {
  if (activeTab.value === 'posts') {
    return '创建博客文章'
  } else if (activeTab.value === 'lostItems') {
    return '发布失物招领'
  } else {
    return '浏览内容'
  }
}

// 处理标签切换
const handleTabChange = (tabId) => {
  activeTab.value = tabId
  currentPage.value = 1
  filters.value = { status: '', category: '', type: '' }
  fetchItems()
}

// 处理筛选条件变化
const handleFilterChange = () => {
  currentPage.value = 1
  fetchItems()
}

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchItems()
  // 滚动到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 根据当前标签页获取对应数据
const fetchItems = () => {
  if (activeTab.value === 'posts') {
    fetchPosts()
  } else if (activeTab.value === 'lostItems') {
    fetchLostItems()
  } 
}

// 创建新内容
const createNewItem = () => {
  if (activeTab.value === 'posts') {
    router.push('/publishPost')
  } else if (activeTab.value === 'lostItems') {
    router.push('/publishItem')
  }
}

// 编辑内容
const editItem = (item) => {
  if (activeTab.value === 'posts') {
    router.push(`/blog/edit/${item.id}`)
  } else if (activeTab.value === 'lostItems') {
    router.push(`/lost-found/edit/${item.id}`)
  }
}

// 删除内容
const deleteItem = async (item) => {
  if (!confirm('确定要删除这条信息吗？此操作不可撤销。')) {
    return
  }

  try {
    if (activeTab.value === 'posts') {
      await generalRequest(`/api/blog-posts/${item.id}`, {
        method: 'DELETE'
      })
    } else if (activeTab.value === 'lostItems') {
      await generalRequest(`/api/lost-items/${item.id}`, {
        method: 'DELETE'
      })
    }
    success('删除成功!')
    // 重新加载数据
    fetchItems()
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败，请稍后再试')
  }
}

// 删除评论
const deleteComment = async (comment) => {
  if (!confirm('确定要删除这条评论吗？此操作不可撤销。')) {
    return
  }

  try {
    if (comment.post_id) {
      await generalRequest(`/api/blog-posts/comments/${comment.id}`, {
        method: 'DELETE'
      })
    } else {
      await generalRequest(`/api/lost-items/comments/${comment.id}`, {
        method: 'DELETE'
      })
    }
    
    // 重新加载数据
    fetchComments()
  } catch (error) {
    console.error('删除评论失败:', error)
    alert('删除评论失败，请稍后再试')
  }
}

// 查看相关文章
const viewRelatedPost = (comment) => {
  if (comment.post_id) {
    router.push(`/blog/${comment.post_id}`)
  } else if (comment.item_id) {
    router.push(`/lost-found/${comment.item_id}`)
  }
}

// 更新失物招领状态
const updateItemStatus = (item) => {
  currentItem.value = item
  selectedStatus.value = item.status
  showStatusModal.value = true
}

// 确认更新状态
const confirmStatusUpdate = async () => {
  if (!currentItem.value) return
  console.log('当前选中的状态:', selectedStatus.value)
  try {
    await generalRequest(`/api/lost-items/${currentItem.value.id}/status`, {
      method: 'PUT',
      data: {
        status: selectedStatus.value
      }
    })
    
    // 更新本地数据
    const index = items.value.findIndex(item => item.id === currentItem.value.id)
    if (index !== -1) {
      items.value[index].status = selectedStatus.value
    }
    
    showStatusModal.value = false
    currentItem.value = null
  } catch (error) {
    console.error('更新状态失败:', error)
    alert('更新状态失败，请稍后再试')
  }
}

// 更新用户头像
const updateAvatar = async () => {
  // 这里可以实现文件上传逻辑，比如使用input[type="file"]
  const fileInput = document.createElement('input')
  fileInput.type = 'file'
  fileInput.accept = 'image/*'
  fileInput.onchange = async (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      
      // 创建FormData对象
      const formData = new FormData()
      formData.append('avatar', file)
      
      try {
        const response = await generalRequest('/api/users/avatar', {
          method: 'POST',
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (response) {
          userInfo.value.avatar = response.avatar_url
        }
      } catch (error) {
        console.error('上传头像失败:', error)
        alert('上传头像失败，请稍后再试')
      }
    }
  }
  fileInput.click()
}

// 编辑个人资料
const editProfile = () => {
  profileForm.value = {
    username: userInfo.value.username,
    email: userInfo.value.email
  }
    profileDialogVisible.value = true

}

// 提交个人资料
const submitProfile = async () => {
  if (!profileForm.value.username.trim()) {
    ElMessage.warning('用户名不能为空')
    return
  }

  try {
    const response = await generalRequest('/api/users', {
      method: 'PUT',
      data: {
        username: profileForm.value.username.trim()
      }
    })

    if (response) {
      ElMessage.success('资料更新成功')
      // 更新本地用户信息
      userInfo.value.username = profileForm.value.username
      profileDialogVisible.value = false
    }
  } catch (error) {
    console.error('更新资料失败:', error)
    ElMessage.error(error.response?.data?.detail || '更新失败，请稍后再试')
  }
}

// 初始化
onMounted(() => {
  fetchUserInfo()
  fetchItems()
})

// 监听标签页变化
watch(activeTab, () => {
  currentPage.value = 1
  fetchItems()
})
</script>

<style scoped>
.profile-page {
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

.profile-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.action-btn.primary {
  background: #667eea;
  color: #ffffff;
}

.action-btn.primary:hover {
  background: #5a67d8;
}

.action-btn.delete:hover {
  background: #fee2e2;
  color: #ef4444;
}

/* 用户信息卡片 */
.user-info-card {
  display: flex;
  gap: 24px;
  padding: 24px;
  margin-bottom: 24px;
  background: #f9fafb;
  border-radius: 12px;
  align-items: center;
}

.user-avatar-container {
  position: relative;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.edit-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 32px;
  height: 32px;
  border-radius: 100%;
  background: #667eea;
  color: #ffffff;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-avatar-btn:hover {
  background: #5a67d8;
  transform: scale(1.1);
}

.edit-avatar-btn svg {
  width: 16px;
  height: 16px;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.user-email {
  color: #6b7280;
  margin-bottom: 16px;
}

.user-stats {
  display: flex;
  gap: 24px;
}

.user-stats .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.user-actions {
  display: flex;
  justify-content: flex-end;
}

.edit-profile-btn {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-profile-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

/* 标签页 */
.content-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 1px solid #f1f3f4;
  padding-bottom: 12px;
}

.content-tabs .tab {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #6b7280;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.content-tabs .tab:hover {
  background: #f3f4f6;
  color: #374151;
}

.content-tabs .tab.active {
  background: #667eea;
  color: #ffffff;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #6b7280;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #f9fafb;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  color: #6b7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f4f6;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  color: #6b7280;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.create-btn {
  margin-top: 16px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background: #667eea;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn:hover {
  background: #5a67d8;
}

/* 物品网格 */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.item-card {
  border: 1px solid #f1f3f4;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background: #ffffff;
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
}

.item-image-container {
  position: relative;
  height: 160px;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-status {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
}

.item-status.lost {
  background: #ef4444;
}

.item-status.found {
  background: #10b981;
}

.item-status.draft {
  background: #9ca3af;
}

.item-status.published {
  background: #10b981;
}

.item-status-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
}

.item-status-tag.unclaimed {
  background: #3b82f6;
}

.item-status-tag.claimed {
  background: #10b981;
}

.item-status-tag.expired {
  background: #9ca3af;
}

.item-featured {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
  background: #f59e0b;
}

.item-content {
  padding: 16px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-details {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b7280;
}

.detail-item svg {
  width: 16px;
  height: 16px;
}

.item-description {
  font-size: 14px;
  color: #4b5563;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 42px;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f1f3f4;
  padding-top: 12px;
}

.item-stats {
  display: flex;
  gap: 12px;
}

.item-stats .stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b7280;
}

.item-stats .stat-item svg {
  width: 16px;
  height: 16px;
}

.item-actions {
  display: flex;
  gap: 8px;
}

/* 评论列表 */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.comment-card {
  border: 1px solid #f1f3f4;
  border-radius: 12px;
  overflow: hidden;
  padding: 16px;
  background: #ffffff;
  transition: box-shadow 0.2s ease;
}

.comment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-type {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: #eef2ff;
  color: #667eea;
}

.comment-time {
  font-size: 12px;
  color: #9ca3af;
}

.comment-content {
  font-size: 14px;
  color: #4b5563;
  margin-bottom: 16px;
}

.comment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f1f3f4;
  padding-top: 12px;
}

.view-post-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-post-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.comment-stats {
  display: flex;
  gap: 12px;
}

.comment-stats .stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b7280;
}

.comment-stats .stat-item svg {
  width: 16px;
  height: 16px;
}

/* 分页控件 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: #667eea;
  color: #667eea;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.page-numbers {
  display: flex;
  gap: 8px;
}

.page-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  color: #4b5563;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-number:hover:not(.active) {
  border-color: #667eea;
  color: #667eea;
}

.page-number.active {
  background: #667eea;
  color: #ffffff;
  border-color: #667eea;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 100%;
  max-width: 400px;
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
}

.modal-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.modal-body {
  margin-bottom: 24px;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn.secondary {
  background: #f3f4f6;
  color: #4b5563;
}

.btn.secondary:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.btn.primary {
  background: #667eea;
  color: #ffffff;
}

.btn.primary:hover {
  background: #5a67d8;
}

:deep(.el-dialog) {
  border-radius: 16px;
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-dialog__body) {
  padding: 0;
}

:deep(.el-input.is-disabled .el-input__wrapper) {
  background-color: #f5f7fa;
}

:deep(.el-input.is-disabled .el-input__inner) {
  color: #606266;
}

.profile-form {
  padding: 20px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}
</style>