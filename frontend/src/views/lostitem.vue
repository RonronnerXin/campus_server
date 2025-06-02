<template>
  <div class="lost-found">
    <div class="page-header">
      <h1>失物招领</h1>
      <div class="filter-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab', { active: activeTab === tab.id }]"
          @click="handleTabChange(tab.id)"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>

    <div class="search-filter">
      <div class="search-input-wrapper">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none">
          <path d="M21 21L16.514 16.506M19 10.5C19 15.194 15.194 19 10.5 19S2 15.194 2 10.5 5.806 2 10.5 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2"/>
        </svg>
        <input 
          type="text" 
          placeholder="搜索物品描述、地点、时间..."
          v-model="searchQuery"
          class="search-input"
          @input="handleSearchDebounce"
          width="200px"
        />
      </div>
      <div class="filter-options">
        <select v-model="selectedCategory" class="filter-select" @change="handleFilterChange">
          <option value="">全部分类</option>
          <option value="card">校园卡</option>
          <option value="electronics">电子设备</option>
          <option value="books">书籍资料</option>
          <option value="clothing">衣物</option>
          <option value="other">其他</option>
        </select>
        <select v-model="selectedLocation" class="filter-select" @change="handleFilterChange">
          <option value="">全部地点</option>
          <option value="library">图书馆</option>
          <option value="classroom">教室</option>
          <option value="canteen">食堂</option>
          <option value="dorm">宿舍楼</option>
          <option value="other">其他</option>
        </select>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 无数据状态 -->
  <div v-else-if="!loading && items.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" class="empty-icon">
        <path d="M9 13h6m-3-3v6M12 21a9 9 0 1 1 0-18 9 9 0 0 1 0 18z" stroke="currentColor" stroke-width="2"/>
      </svg>
      <p>暂无相关物品信息</p>
    </div>

    <!-- 物品列表 -->
    <div v-else class="items-grid">
      <div v-for="item in items" :key="item.id" class="item-card" @click="viewItemDetail(item.id)">
        <div class="item-image-container">
          <img :src="getItemImage(item)" :alt="item.title" class="item-image" />
          <span class="item-status" :class="item.type">{{ item.type === 'lost' ? '寻物启事' : '招领启事' }}</span>
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
            <div class="user-info">
              <img :src="getUserAvatar(item.owner_id)" :alt="item.owner_username || '用户'" class="user-avatar" />
              <span class="user-name">{{ item.owner_username || '匿名用户' }}</span>
            </div>
            <button class="contact-btn" @click.stop="contactOwner(item)">联系Ta</button>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { generalRequest } from '../services/genServ' // 根据实际路径调整

const router = useRouter()
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedLocation = ref('')
const activeTab = ref('all')
const currentPage = ref(1)
const itemsPerPage = 20
const totalPages = ref(1)
const totalCount = ref(0)
const items = ref([])
const loading = ref(false)
const searchTimeout = ref(null)

// 默认用户头像
const DEFAULT_AVATAR = 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face'

// 标签页配置
const tabs = ref([
  { id: 'all', name: '全部' },
  { id: 'lost', name: '寻物启事' },
  { id: 'found', name: '招领启事' }
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

// 获取失物招领列表
const fetchItems = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * itemsPerPage,
      limit: itemsPerPage,
      type: activeTab.value === 'all' ? undefined : activeTab.value,
      category: selectedCategory.value || undefined,
      q: searchQuery.value || undefined
    }

    // 如果是按地点筛选，将其添加到搜索查询中
    if (selectedLocation.value) {
      params.q = params.q ? `${params.q} ${selectedLocation.value}` : selectedLocation.value
    }

    const response = await generalRequest('/api/lost-items/', {
      method: 'GET',
      params
    })

    if (response && response.data) {
      items.value = response.data
      totalCount.value = response.count
      totalPages.value = response.totalPages
    } else {
      console.error('获取数据失败: 响应格式不正确', response)
      items.value = []
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    items.value = []
    if (error.response && error.response.status === 403) {
      if (confirm('您的登录状态已过期，请先登录')) {
        router.push('/login')
      }
    }
  } finally {
    loading.value = false
  }
}

// 获取物品图片
const getItemImage = (item) => {
  if (item.images && item.images.length > 0) {
    // 检查是否已经是完整URL
    if (item.images[0].startsWith('http')) {
      return item.images[0]
    }
    // 拼接完整的API地址
    return `http://localhost:8000${item.images[0]}`
  }

  // 默认图片逻辑保持不变
  const defaultImages = {
    'card': 'https://images.unsplash.com/photo-1586223287834-f73bd5e6a967?w=300&h=200&fit=crop',
    'electronics': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=200&fit=crop',
    'books': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=200&fit=crop',
    'clothing': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=300&h=200&fit=crop',
    'other': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=200&fit=crop'
  }
  return defaultImages[item.category] || defaultImages.other
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

// 处理标签切换
const handleTabChange = (tabId) => {
  activeTab.value = tabId
  currentPage.value = 1
  fetchItems()
}

// 处理筛选条件变化
const handleFilterChange = () => {
  currentPage.value = 1
  fetchItems()
}

// 处理搜索（带防抖）
const handleSearchDebounce = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1
    fetchItems()
  }, 500) // 500ms防抖
}

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchItems()
  // 滚动到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 查看物品详情
const viewItemDetail = (itemId) => {
  router.push(`/lostitemdetail/${itemId}`)
}

// 联系物品所有者
const contactOwner = (item) => {
  // 阻止冒泡，避免触发卡片点击
  event.stopPropagation()
  
  if (item.hide_contact) {
    // 如果隐藏联系方式，跳转到消息页面
    router.push(`/messages/new?recipient=${item.owner_id}&itemId=${item.id}`)
  } else {
    // 显示联系方式
    let contactInfo = ''
    switch (item.contact_type) {
      case 'phone':
        contactInfo = `电话: ${item.contact_value}`
        break
      case 'wechat':
        contactInfo = `微信: ${item.contact_value}`
        break
      case 'qq':
        contactInfo = `QQ: ${item.contact_value}`
        break
      default:
        contactInfo = item.contact_value
    }
    alert(`联系方式: ${contactInfo}`)
  }
}

// 初始化加载数据
onMounted(() => {
  fetchItems()
})

// 监听路由参数变化（如果有）
watch(() => router.currentRoute.value.query, (newQuery) => {
  if (newQuery.type) {
    activeTab.value = newQuery.type
  }
  if (newQuery.category) {
    selectedCategory.value = newQuery.category
  }
  if (newQuery.q) {
    searchQuery.value = newQuery.q
  }
  
  // 如果有查询参数变化，重新获取数据
  fetchItems()
}, { immediate: true })
</script>

<style scoped>
.lost-found {
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

.search-filter {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  align-items: center; /* 垂直居中 */
}

.search-input-wrapper {
  flex: 1 1 220px; /* 不用width, 自动分配剩余宽度，最小220px */
  min-width: 180px;
}

.filter-options {
  flex-shrink: 0;
  min-width: 200px;
  max-width: 350px;
  gap: 12px;
  display: flex;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  background: #f9fafb;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-select {
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
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
  cursor: pointer;
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

.item-content {
  padding: 16px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 12px;
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
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 12px;
  color: #4b5563;
  font-weight: 500;
}

.contact-btn {
  padding: 6px 12px;
  background: #667eea;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.contact-btn:hover {
  background: #5a67d8;
}

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

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .filter-tabs {
    width: 100%;
  }
  
  .tab {
    flex: 1;
    text-align: center;
  }
  
  .search-filter {
    flex-direction: column;
  }
  
  .filter-options {
    width: 100%;
  }
  
  .filter-select {
    flex: 1;
  }
}
</style>