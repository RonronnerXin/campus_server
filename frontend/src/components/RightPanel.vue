<template>
  <aside class="right-panel">
    <!-- 推荐用户 -->
    <div class="panel-section">
      <h3 class="section-title">推荐关注</h3>
      <div class="user-list">
        <div v-for="user in recommendedUsers" :key="user.id" class="user-item">
          <img :src="user.avatar" :alt="user.name" class="user-avatar" />
          <div class="user-info">
            <h4 class="user-name">{{ user.name }}</h4>
            <p class="user-desc">{{ user.description }}</p>
          </div>
          <button class="follow-btn">关注</button>
        </div>
      </div>
    </div>

    <!-- 热门话题 -->
    <div class="panel-section">
      <h3 class="section-title">热门话题</h3>
      <div class="trending-topics">
        <div v-for="topic in trendingTopics" :key="topic.id" class="topic-item">
          <div class="topic-info">
            <h4 class="topic-name"># {{ topic.name }}</h4>
            <p class="topic-stats">{{ topic.posts }} 条讨论</p>
          </div>
          <div class="topic-trend">
            <span class="trend-indicator" :class="topic.trend">
              {{ topic.trend === 'up' ? '↗' : '↘' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 活动公告 -->
    <div class="panel-section">
      <h3 class="section-title">社区活动</h3>
      <div class="activity-card">
        <div class="activity-header">
          <h4>前端技术分享会</h4>
          <span class="activity-status">进行中</span>
        </div>
        <p class="activity-desc">
          本周六下午2点，我们将举办前端技术分享会，欢迎大家参与讨论。
        </p>
        <button class="join-btn">立即参与</button>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="panel-section">
      <h3 class="section-title">社区数据</h3>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-number">12.5k</span>
          <span class="stat-label">活跃用户</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">3.2k</span>
          <span class="stat-label">今日发帖</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">856</span>
          <span class="stat-label">在线用户</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">45.6k</span>
          <span class="stat-label">总帖子数</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'

const recommendedUsers = ref([
  {
    id: 1,
    name: '技术大牛',
    description: '全栈开发工程师',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face'
  },
  {
    id: 2,
    name: '设计师小美',
    description: 'UI/UX 设计师',
    avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=40&h=40&fit=crop&crop=face'
  },
  {
    id: 3,
    name: '产品经理',
    description: '互联网产品经理',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'
  }
])

const trendingTopics = ref([
  { id: 1, name: 'Vue3新特性', posts: '1.2k', trend: 'up' },
  { id: 2, name: 'React18', posts: '856', trend: 'up' },
  { id: 3, name: '前端工程化', posts: '642', trend: 'down' },
  { id: 4, name: 'TypeScript', posts: '423', trend: 'up' }
])
</script>

<style scoped>
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: sticky;
  top: 88px;
  height: fit-content;
}

.panel-section {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #f1f3f4;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-item {
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

.user-info {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.user-desc {
  font-size: 12px;
  color: #9ca3af;
}

.follow-btn {
  padding: 6px 12px;
  border: 1px solid #667eea;
  border-radius: 6px;
  background: transparent;
  color: #667eea;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.follow-btn:hover {
  background: #667eea;
  color: #ffffff;
}

.trending-topics {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.topic-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  transition: background 0.2s ease;
  cursor: pointer;
}

.topic-item:hover {
  background: #f9fafb;
}

.topic-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.topic-stats {
  font-size: 12px;
  color: #9ca3af;
}

.trend-indicator {
  font-size: 16px;
  font-weight: bold;
}

.trend-indicator.up {
  color: #10b981;
}

.trend-indicator.down {
  color: #ef4444;
}

.activity-card {
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #ffffff;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.activity-header h4 {
  font-size: 16px;
  font-weight: 600;
}

.activity-status {
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.activity-desc {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
  opacity: 0.9;
}

.join-btn {
  width: 100%;
  padding: 10px;
  background: #ffffff;
  color: #667eea;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.join-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px 8px;
  border-radius: 8px;
  background: #f9fafb;
}

.stat-number {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 500;
}

@media (max-width: 1024px) {
  .right-panel {
    display: none;
  }
}
</style>