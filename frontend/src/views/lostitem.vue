<template>
  <div class="lost-found">
    <div class="page-header">
      <h1>失物招领</h1>
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
        />
      </div>
      <div class="filter-options">
        <select v-model="selectedCategory" class="filter-select">
          <option value="">全部分类</option>
          <option value="card">校园卡</option>
          <option value="electronics">电子设备</option>
          <option value="books">书籍资料</option>
          <option value="clothing">衣物</option>
          <option value="other">其他</option>
        </select>
        <select v-model="selectedLocation" class="filter-select">
          <option value="">全部地点</option>
          <option value="library">图书馆</option>
          <option value="classroom">教室</option>
          <option value="canteen">食堂</option>
          <option value="dorm">宿舍楼</option>
          <option value="other">其他</option>
        </select>
      </div>
    </div>

    <div class="items-grid">
      <div v-for="item in filteredItems" :key="item.id" class="item-card">
        <div class="item-image-container">
          <img :src="item.image" :alt="item.title" class="item-image" />
          <span class="item-status" :class="item.type">{{ item.type === 'lost' ? '寻物启事' : '招领启事' }}</span>
        </div>
        <div class="item-content">
          <h3 class="item-title">{{ item.title }}</h3>
          <div class="item-details">
            <div class="detail-item">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ item.time }}</span>
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
              <img :src="item.user.avatar" :alt="item.user.name" class="user-avatar" />
              <span class="user-name">{{ item.user.name }}</span>
            </div>
            <button class="contact-btn">联系Ta</button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="pagination">
      <button class="page-btn prev" :disabled="currentPage === 1" @click="currentPage--">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M15 19L8 12L15 5" stroke="currentColor" stroke-width="2"/>
        </svg>
      </button>
      <div class="page-numbers">
        <button 
          v-for="page in totalPages" 
          :key="page" 
          :class="['page-number', { active: currentPage === page }]"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
      <button class="page-btn next" :disabled="currentPage === totalPages" @click="currentPage++">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M9 5L16 12L9 19" stroke="currentColor" stroke-width="2"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedLocation = ref('')
const activeTab = ref('all')
const currentPage = ref(1)
const itemsPerPage = 6
const totalPages = 3

const tabs = ref([
  { id: 'all', name: '全部' },
  { id: 'lost', name: '寻物启事' },
  { id: 'found', name: '招领启事' }
])

const items = ref([
  {
    id: 1,
    type: 'lost',
    title: '丢失校园卡',
    description: '昨天下午在图书馆自习时不小心丢失了校园卡，姓名李明，学号2021001234，有拾到的同学请联系我，谢谢！',
    location: '图书馆三楼',
    time: '2023-10-15 14:30',
    image: 'https://images.unsplash.com/photo-1586223287834-f73bd5e6a967?w=300&h=200&fit=crop',
    category: 'card',
    user: {
      name: '李明',
      avatar: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face'
    }
  },
  {
    id: 2,
    type: 'found',
    title: '捡到一个黑色钱包',
    description: '今天早上在教学楼A区一楼捡到一个黑色钱包，内有现金和一些证件，失主请联系我并说出钱包内物品信息认领。',
    location: '教学楼A区',
    time: '2023-10-16 09:15',
    image: 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=200&fit=crop',
    category: 'other',
    user: {
      name: '张华',
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=40&h=40&fit=crop&crop=face'
    }
  },
  {
    id: 3,
    type: 'lost',
    title: '寻找蓝色笔记本电脑',
    description: '今天中午在食堂二楼用餐后发现笔记本电脑不见了，是一台蓝色的联想笔记本，有明显的贴纸标识，内有重要资料，酬谢500元。',
    location: '第二食堂',
    time: '2023-10-16 12:40',
    image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=200&fit=crop',
    category: 'electronics',
    user: {
      name: '王芳',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=40&h=40&fit=crop&crop=face'
    }
  },
  {
    id: 4,
    type: 'found',
    title: '捡到一串钥匙',
    description: '在体育馆门口捡到一串钥匙，有宿舍钥匙和自行车钥匙，还有一个小熊挂件，请失主尽快认领。',
    location: '体育馆',
    time: '2023-10-15 18:20',
    image: 'https://images.unsplash.com/photo-1582550740000-5e53d86ddec9?w=300&h=200&fit=crop',
    category: 'other',
    user: {
      name: '刘强',
      avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=40&h=40&fit=crop&crop=face'
    }
  },
  {
    id: 5,
    type: 'lost',
    title: '丢失《数据结构》教材',
    description: '上周五在计算机教室上课后丢失了一本《数据结构》教材，书内有重要笔记，如有拾到请联系我，必有酬谢。',
    location: '计算机教室',
    time: '2023-10-13 16:00',
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=200&fit=crop',
    category: 'books',
    user: {
      name: '赵雪',
      avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=40&h=40&fit=crop&crop=face'
    }
  },
  {
    id: 6,
    type: 'found',
    title: '捡到一件黑色外套',
    description: '昨晚在学生活动中心捡到一件黑色外套，是优衣库的，口袋里有一张电影票，请失主联系认领。',
    location: '学生活动中心',
    time: '2023-10-15 21:30',
    image: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=300&h=200&fit=crop',
    category: 'clothing',
    user: {
      name: '陈明',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face'
    }
  }
])

const filteredItems = computed(() => {
  let result = items.value

  // 按标签筛选
  if (activeTab.value !== 'all') {
    result = result.filter(item => item.type === activeTab.value)
  }

  // 按搜索关键词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item => 
      item.title.toLowerCase().includes(query) || 
      item.description.toLowerCase().includes(query) || 
      item.location.toLowerCase().includes(query)
    )
  }

  // 按分类筛选
  if (selectedCategory.value) {
    result = result.filter(item => item.category === selectedCategory.value)
  }

  // 按地点筛选
  if (selectedLocation.value) {
    const location = selectedLocation.value.toLowerCase()
    result = result.filter(item => item.location.toLowerCase().includes(location))
  }

  return result
})
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
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  min-width: 200px;
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

.filter-options {
  display: flex;
  gap: 12px;
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