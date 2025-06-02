<template>
  <div class="item-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 内容区域 -->
    <template v-else-if="item">
      <!-- 返回按钮 -->
      <div class="back-button" @click="goBack">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>返回列表</span>
      </div>
      
      <!-- 主要内容 -->
      <div class="detail-container">
        <!-- 左侧图片区域 -->
        <div class="image-section">
          <div class="main-image-container">
            <img :src="currentImage" :alt="item.title" class="main-image" />
            <span class="item-status" :class="item.type">
              {{ item.type === 'lost' ? '寻物启事' : '招领启事' }}
            </span>
            <span class="item-status status-badge" :class="getStatusClass(item.status)">
              {{ getStatusText(item.status) }}
            </span>
          </div>
          
          <!-- 缩略图列表 -->
          <div v-if="item.images && item.images.length > 1" class="thumbnail-list">
            <div 
              v-for="(image, index) in item.images" 
              :key="index"
              :class="['thumbnail-item', { active: currentImageIndex === index }]"
              @click="currentImageIndex = index"
            >
              <img :src="image" :alt="`缩略图 ${index + 1}`" />
            </div>
          </div>
        </div>
        
        <!-- 右侧信息区域 -->
        <div class="info-section">
          <h1 class="item-title">{{ item.title }}</h1>
          
          <div class="item-meta">
            <div class="meta-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>发布时间: {{ formatDate(item.created_at) }}</span>
            </div>
            <div class="meta-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>浏览次数: {{ item.views_count }}</span>
            </div>
          </div>
          
          <div class="info-card">
            <h3 class="info-title">物品信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">物品类型</span>
                <span class="info-value">{{ getCategoryText(item.category) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">丢失/拾取地点</span>
                <span class="info-value">{{ item.location }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">丢失/拾取时间</span>
                <span class="info-value">{{ formatDate(item.time) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">当前状态</span>
                <span class="info-value" :class="getStatusClass(item.status)">
                  {{ getStatusText(item.status) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="description-card">
            <h3 class="info-title">详细描述</h3>
            <p class="description-text">{{ item.description }}</p>
          </div>
          
          <div class="contact-card">
            <h3 class="info-title">联系方式</h3>
            <div v-if="item.hide_contact" class="hidden-contact">
              <p>发布者已隐藏联系方式，请通过站内消息联系</p>
              <button class="primary-btn" @click="sendMessage">发送站内消息</button>
            </div>
            <div v-else class="contact-info">
              <div class="contact-type">
                <span class="contact-label">联系方式:</span>
                <span class="contact-value">{{ getContactTypeText(item.contact_type) }}</span>
              </div>
              <div class="contact-value-container">
                <span class="contact-label">联系信息:</span>
                <span class="contact-value">{{ item.contact_value }}</span>
                <button class="copy-btn" @click="copyContactInfo(item.contact_value)">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  复制
                </button>
              </div>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div v-if="isOwner" class="action-buttons">
            <button class="secondary-btn" @click="editItem">编辑信息</button>
            <button class="secondary-btn" :class="getStatusActionClass(item.status)" @click="updateStatus">
              {{ getStatusActionText(item.status) }}
            </button>
            <button class="danger-btn" @click="confirmDelete">删除信息</button>
          </div>
        </div>
      </div>
      
      <!-- 相关推荐 -->
      <div class="related-section">
        <h2 class="section-title">相关物品</h2>
        <div class="related-items">
          <div v-if="loading" class="loading-container small">
            <div class="loading-spinner"></div>
          </div>
          <div v-else-if="relatedItems.length === 0" class="empty-related">
            暂无相关物品
          </div>
          <div v-else class="related-items-grid">
            <div 
              v-for="relatedItem in relatedItems" 
              :key="relatedItem.id" 
              class="related-item-card"
              @click="viewItemDetail(relatedItem.id)"
            >
              <div class="related-item-image">
                <img :src="getItemImage(relatedItem)" :alt="relatedItem.title" />
                <span class="item-status small" :class="relatedItem.type">
                  {{ relatedItem.type === 'lost' ? '寻物' : '招领' }}
                </span>
              </div>
              <div class="related-item-info">
                <h4 class="related-item-title">{{ relatedItem.title }}</h4>
                <p class="related-item-location">{{ relatedItem.location }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <!-- 错误状态 -->
    <div v-else class="error-container">
      <svg viewBox="0 0 24 24" fill="none" class="error-icon">
        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <h2>物品信息未找到</h2>
      <p>该物品可能已被删除或您没有权限查看</p>
      <button class="primary-btn" @click="goBack">返回列表</button>
    </div>
    
    <!-- 确认删除对话框 -->
    <div v-if="showDeleteConfirm" class="modal-overlay">
      <div class="modal-container">
        <h3>确认删除</h3>
        <p>您确定要删除这条物品信息吗？此操作不可撤销。</p>
        <div class="modal-actions">
          <button class="secondary-btn" @click="showDeleteConfirm = false">取消</button>
          <button class="danger-btn" @click="deleteItem">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { generalRequest } from '../services/genServ' // 根据实际路径调整

const router = useRouter()
const route = useRoute()
const itemId = computed(() => route.params.id)

const item = ref(null)
const loading = ref(true)
const currentImageIndex = ref(0)
const relatedItems = ref([])
const showDeleteConfirm = ref(false)

// 当前用户ID (实际应用中应从用户状态获取)
const currentUserId = ref('user-123') // 示例ID，实际使用时应替换

// 计算当前显示的图片
const currentImage = computed(() => {
  if (!item.value || !item.value.images || item.value.images.length === 0) {
    return getDefaultImage(item.value?.category)
  }
  return item.value.images[currentImageIndex.value]
})

// 判断当前用户是否为物品所有者
const isOwner = computed(() => {
  return item.value && item.value.owner_id === currentUserId.value
})

// 获取物品详情
const fetchItemDetail = async () => {
  loading.value = true
  try {
    const response = await generalRequest(`/api/lost-items/${itemId.value}`, {
      method: 'GET'
    })
    
    if (response) {
      item.value = response
      // 重置当前图片索引
      currentImageIndex.value = 0
      // 获取相关物品
      fetchRelatedItems()
    } else {
      console.error('获取物品详情失败:', response)
      item.value = null
    }
  } catch (error) {
    console.error('获取物品详情出错:', error)
    item.value = null
    if (error.response && error.response.status === 403) {
      if (confirm('您的登录状态已过期，请先登录')) {
        router.push('/login')
      }
    }
  } finally {
    loading.value = false
  }
}

// 获取相关物品
const fetchRelatedItems = async () => {
  if (!item.value) return
  
  try {
    // 根据当前物品的类型和分类获取相关物品
    const params = {
      skip: 0,
      limit: 4,
      type: item.value.type,
      category: item.value.category,
      // 排除当前物品
      exclude: itemId.value
    }
    
    const response = await generalRequest('/api/lost-items/', {
      method: 'GET',
      params
    })
    
    if (response && response.data) {
      // 过滤掉当前物品
      relatedItems.value = response.data
        .filter(i => i.id !== itemId.value)
        .slice(0, 4) // 最多显示4个
    }
  } catch (error) {
    console.error('获取相关物品失败:', error)
    relatedItems.value = []
  }
}

// 更新物品状态
const updateStatus = async () => {
  if (!item.value) return
  
  const newStatus = item.value.status === 'unclaimed' ? 'claimed' : 'unclaimed'
  
  try {
    const response = await generalRequest(`/api/lost-items/${itemId.value}/status`, {
      method: 'PATCH',
      data: { status: newStatus }
    })
    
    if (response && response.data) {
      item.value = response.data
      alert(newStatus === 'claimed' ? '物品已标记为已认领/找到' : '物品已标记为未认领/未找到')
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    alert('更新状态失败，请稍后再试')
  }
}

// 删除物品
const deleteItem = async () => {
  try {
    const response = await generalRequest(`/api/lost-items/${itemId.value}`, {
      method: 'DELETE'
    })
    
    if (response && response.message) {
      alert('删除成功')
      router.push('/lost-found')
    }
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败，请稍后再试')
  } finally {
    showDeleteConfirm.value = false
  }
}

// 确认删除
const confirmDelete = () => {
  showDeleteConfirm.value = true
}

// 编辑物品
const editItem = () => {
  router.push(`/lost-found/edit/${itemId.value}`)
}

// 发送站内消息
const sendMessage = () => {
  if (!item.value) return
  router.push(`/messages/new?recipient=${item.value.owner_id}&itemId=${itemId.value}`)
}

// 复制联系信息
const copyContactInfo = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => alert('联系方式已复制到剪贴板'))
    .catch(err => console.error('复制失败:', err))
}

// 返回列表页
const goBack = () => {
  router.push('/lost-found')
}

// 查看其他物品详情
const viewItemDetail = (id) => {
  router.push(`/lost-found/${id}`)
}

// 获取物品图片
const getItemImage = (item) => {
  if (!item) return ''
  
  if (item.images && item.images.length > 0) {
    return item.images[0]
  }
  return getDefaultImage(item.category)
}

// 获取默认图片
const getDefaultImage = (category) => {
  const defaultImages = {
    'card': 'https://images.unsplash.com/photo-1586223287834-f73bd5e6a967?w=300&h=200&fit=crop',
    'electronics': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=200&fit=crop',
    'books': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=200&fit=crop',
    'clothing': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=300&h=200&fit=crop',
    'other': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=200&fit=crop'
  }
  return defaultImages[category] || defaultImages.other
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

// 获取分类文本
const getCategoryText = (category) => {
  const categoryMap = {
    'card': '校园卡',
    'electronics': '电子设备',
    'books': '书籍资料',
    'clothing': '衣物',
    'other': '其他'
  }
  return categoryMap[category] || '未知'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'unclaimed': '未认领/未找到',
    'claimed': '已认领/已找到',
    'expired': '已过期'
  }
  return statusMap[status] || '未知'
}

// 获取状态CSS类
const getStatusClass = (status) => {
  const statusClassMap = {
    'unclaimed': 'status-unclaimed',
    'claimed': 'status-claimed',
    'expired': 'status-expired'
  }
  return statusClassMap[status] || ''
}

// 获取状态操作文本
const getStatusActionText = (status) => {
  return status === 'unclaimed' ? '标记为已认领/找到' : '标记为未认领/未找到'
}

// 获取状态操作CSS类
const getStatusActionClass = (status) => {
  return status === 'unclaimed' ? 'action-claim' : 'action-unclaim'
}

// 获取联系方式文本
const getContactTypeText = (contactType) => {
  const contactTypeMap = {
    'phone': '电话',
    'wechat': '微信',
    'qq': 'QQ'
  }
  return contactTypeMap[contactType] || '其他'
}

// 监听路由参数变化
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchItemDetail()
  }
}, { immediate: true })
</script>

<style scoped>
.item-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  position: relative;
}

.back-button {
  display: inline-flex;
  align-self: left;
  gap: 8px;
  padding: 8px 16px;
  background: #f9fafb;
  border-radius: 8px;
  color: #4b5563;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 24px;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.back-button svg {
  width: 20px;
  height: 20px;
}

.detail-container {
  display: grid;
  grid-template-columns: minmax(300px, 2fr) 3fr;
  gap: 32px;
  margin-bottom: 48px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.image-section {
  padding: 24px;
}

.main-image-container {
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 16px;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-status {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 16px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  z-index: 1;
}

.item-status.lost {
  background: #ef4444;
}

.item-status.found {
  background: #10b981;
}

.item-status.small {
  font-size: 12px;
  padding: 4px 12px;
}

.status-badge {
  top: 16px;
  left: auto;
  right: 16px;
}

.status-unclaimed {
  background: #f59e0b;
}

.status-claimed {
  background: #10b981;
}

.status-expired {
  background: #6b7280;
}

.thumbnail-list {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.thumbnail-item {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.thumbnail-item:hover {
  transform: translateY(-2px);
}

.thumbnail-item.active {
  border-color: #667eea;
}

.thumbnail-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-section {
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.item-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.item-meta {
  display: flex;
  gap: 24px;
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
}

.meta-item svg {
  width: 18px;
  height: 18px;
}

.info-card, .description-card, .contact-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
}

.info-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 14px;
  color: #6b7280;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: #1f2937;
}

.description-text {
  font-size: 16px;
  line-height: 1.6;
  color: #4b5563;
  white-space: pre-line;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-type, .contact-value-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.contact-label {
  font-size: 14px;
  color: #6b7280;
  min-width: 80px;
}

.contact-value {
  font-size: 16px;
  font-weight: 500;
  color: #1f2937;
}

.hidden-contact {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

.hidden-contact p {
  font-size: 14px;
  color: #6b7280;
}

.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #f3f4f6;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.copy-btn svg {
  width: 16px;
  height: 16px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.primary-btn, .secondary-btn, .danger-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn {
  background: #667eea;
  color: #ffffff;
}

.primary-btn:hover {
  background: #5a67d8;
}

.secondary-btn {
  background: #f3f4f6;
  color: #4b5563;
}

.secondary-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.danger-btn {
  background: #fee2e2;
  color: #ef4444;
}

.danger-btn:hover {
  background: #fecaca;
}

.action-claim {
  background: #d1fae5;
  color: #10b981;
}

.action-claim:hover {
  background: #a7f3d0;
}

.action-unclaim {
  background: #fef3c7;
  color: #f59e0b;
}

.action-unclaim:hover {
  background: #fde68a;
}

.related-section {
  margin-top: 48px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.related-items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.related-item-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.related-item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.related-item-image {
  position: relative;
  height: 150px;
}

.related-item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-item-info {
  padding: 12px;
}

.related-item-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.related-item-location {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
}

.loading-container.small {
  padding: 24px 0;
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

.loading-container.small .loading-spinner {
  width: 24px;
  height: 24px;
  margin-bottom: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  text-align: center;
}

.error-icon {
  width: 64px;
  height: 64px;
  color: #ef4444;
  margin-bottom: 24px;
}

.empty-related {
  text-align: center;
  padding: 24px;
  color: #6b7280;
  font-size: 14px;
}

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

.modal-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.modal-container h3 {
  font-size: 18px;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 16px;
}

.modal-container p {
  margin-bottom: 24px;
  color: #4b5563;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 768px) {
  .detail-container {
    grid-template-columns: 1fr;
  }
  
  .main-image-container {
    height: 300px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .related-items-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}
</style>