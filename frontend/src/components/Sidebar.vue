<template>
  <aside class="sidebar">
    <nav class="nav-menu">
      <div class="nav-section">
        
        <div class="nav-item" :class="{ active: currentRoute === '/' }" @click="navigateTo('/lost-found')">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>失物招领</span>
        </div>
        
        <div class="nav-item" :class="{ active: currentRoute === '/community' }" @click="navigateTo('/community')">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M17 20H22V18C22 16.3431 20.6569 15 19 15C18.0444 15 17.1931 15.4468 16.6438 16.1429M17 20H7M17 20V18C17 15.3431 14.6569 13 12 13C9.34315 13 7 15.3431 7 18V20M7 20H2V18C2 16.3431 3.34315 15 5 15C5.95561 15 6.80686 15.4468 7.35625 16.1429M15 7C15 9.20914 13.2091 11 11 11C8.79086 11 7 9.20914 7 7C7 4.79086 8.79086 3 11 3C13.2091 3 15 4.79086 15 7Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>社区分享</span>
        </div>
        
      </div>
      <div class="create-post">
      <button class="create-btn" @click="navigateTo('/publishItem')">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M12 4V20M20 12H4" stroke="currentColor" stroke-width="2"/>
        </svg>
        发布失物招领
      </button>
            <button class="create-btn" @click="navigateTo('/publishPost')">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M12 4V20M20 12H4" stroke="currentColor" stroke-width="2"/>
        </svg>
        发布博客
      </button>
    </div>
      <div class="nav-section">
        <h3 class="section-title">热门话题</h3>
        <div class="topic-list">
          <div class="topic-item" v-for="topic in topics" :key="topic.id">
            <span class="topic-name"># {{ topic.name }}</span>
            <span class="topic-count">{{ topic.count }}</span>
          </div>
        </div>
      </div>
    </nav>
    

  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const currentRoute = computed(() => route.path)

const navigateTo = (path) => {
  router.push(path)
}

const topics = ref([
  { id: 1, name: '校园卡丢失', count: '56' },
  { id: 2, name: '考研资料', count: '42' },
  { id: 3, name: '宿舍生活', count: '38' },
  { id: 4, name: '校园美食', count: '31' },
  { id: 5, name: '实习信息', count: '28' }
])
</script>

<style scoped>
.sidebar {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  height: fit-content;
  position: sticky;
  top: 88px;
  border: 1px solid #f1f3f4;
}

.nav-menu {
  margin-bottom: 24px;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 4px;
  color: #6b7280;
  font-weight: 500;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.nav-item svg {
  width: 20px;
  height: 20px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #9ca3af;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.topic-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.topic-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.topic-item:hover {
  background: #f9fafb;
}

.topic-name {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.topic-count {
  font-size: 12px;
  color: #9ca3af;
}

.create-post {
  border-top: 1px solid #f1f3f4;
  padding-top: 24px;
}

.create-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #e834bb 100%);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 20px;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.create-btn svg {
  width: 18px;
  height: 18px;
}

@media (max-width: 1024px) {
  .sidebar {
    display: none;
  }
}
</style>