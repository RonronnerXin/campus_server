<template>
  <div class="post-list">
    <div class="post-header">
      <h2>最新动态</h2>
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
    
    <div class="posts">
      <article 
        v-for="post in posts" 
        :key="post.id" 
        class="post-card"
      >
        <div class="post-header-info">
          <img :src="post.author.avatar" :alt="post.author.name" class="author-avatar" />
          <div class="author-info">
            <h4 class="author-name">{{ post.author.name }}</h4>
            <span class="post-time">{{ post.createdAt }}</span>
          </div>
          <button class="follow-btn" v-if="!post.author.isFollowing">关注</button>
        </div>
        
        <div class="post-content">
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-excerpt">{{ post.excerpt }}</p>
          <div class="post-tags">
            <span v-for="tag in post.tags" :key="tag" class="tag"># {{ tag }}</span>
          </div>
          <img v-if="post.image" :src="post.image" :alt="post.title" class="post-image" />
        </div>
        
        <div class="post-actions">
          <button class="action-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M20.84 4.61C20.3292 4.099 19.7228 3.69364 19.0554 3.41708C18.3879 3.14052 17.6725 2.99817 16.95 2.99817C16.2275 2.99817 15.5121 3.14052 14.8446 3.41708C14.1772 3.69364 13.5708 4.099 13.06 4.61L12 5.67L10.94 4.61C9.9083 3.5783 8.50903 2.9987 7.05 2.9987C5.59096 2.9987 4.19169 3.5783 3.16 4.61C2.1283 5.6417 1.5487 7.04097 1.5487 8.5C1.5487 9.95903 2.1283 11.3583 3.16 12.39L12 21.23L20.84 12.39C21.351 11.8792 21.7563 11.2728 22.0329 10.6053C22.3095 9.93789 22.4518 9.22248 22.4518 8.5C22.4518 7.77752 22.3095 7.06211 22.0329 6.39467C21.7563 5.72723 21.351 5.1208 20.84 4.61V4.61Z" stroke="currentColor" stroke-width="2"/>
            </svg>
            <span>{{ post.likes }}</span>
          </button>
          
          <button class="action-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2"/>
            </svg>
            <span>{{ post.comments }}</span>
          </button>
          
          <button class="action-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M4 12V20C4 20.5523 4.44772 21 5 21H9.58579C9.851 21 10.1054 20.8946 10.2929 20.7071L16 15H20C20.5523 15 21 14.5523 21 14V6C21 5.44772 20.5523 5 20 5H4C3.44772 5 3 5.44772 3 6V11C3 11.5523 3.44772 12 4 12Z" stroke="currentColor" stroke-width="2"/>
            </svg>
            <span>分享</span>
          </button>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('latest')

const tabs = ref([
  { id: 'latest', name: '最新' },
  { id: 'hot', name: '热门' },
  { id: 'following', name: '关注' }
])

const posts = ref([
  {
    id: 1,
    title: 'Vue 3 Composition API 最佳实践分享',
    excerpt: '在使用 Vue 3 开发项目的过程中，我总结了一些 Composition API 的最佳实践，希望能帮助到大家提高开发效率...',
    author: {
      name: '前端小王',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face',
      isFollowing: false
    },
    createdAt: '2小时前',
    likes: 128,
    comments: 24,
    tags: ['Vue3', '前端开发', '最佳实践'],
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=300&fit=crop'
  },
  {
    id: 2,
    title: '设计系统构建指南：从零到一',
    excerpt: '设计系统是现代产品开发中不可或缺的一部分。本文将详细介绍如何从零开始构建一个完整的设计系统...',
    author: {
      name: '设计师小李',
      avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=40&h=40&fit=crop&crop=face',
      isFollowing: true
    },
    createdAt: '4小时前',
    likes: 89,
    comments: 16,
    tags: ['设计系统', 'UI设计', '产品设计']
  },
  {
    id: 3,
    title: '微前端架构实践总结',
    excerpt: '在大型项目中，微前端架构能够有效解决团队协作和技术栈选择的问题。本文分享我们团队的实践经验...',
    author: {
      name: '架构师老张',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face',
      isFollowing: false
    },
    createdAt: '6小时前',
    likes: 156,
    comments: 32,
    tags: ['微前端', '架构设计', '工程化'],
    image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600&h=300&fit=crop'
  }
])
</script>

<style scoped>
.post-list {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f3f4;
  overflow: hidden;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #f1f3f4;
}

.post-header h2 {
  font-size: 20px;
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

.posts {
  display: flex;
  flex-direction: column;
}

.post-card {
  padding: 24px;
  border-bottom: 1px solid #f1f3f4;
  transition: background 0.2s ease;
}

.post-card:hover {
  background: #fafbfc;
}

.post-card:last-child {
  border-bottom: none;
}

.post-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.author-info {
  flex: 1;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.post-time {
  font-size: 12px;
  color: #9ca3af;
}

.follow-btn {
  padding: 6px 16px;
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

.post-content {
  margin-bottom: 16px;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
  line-height: 1.4;
}

.post-excerpt {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 12px;
}

.post-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 8px;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 12px;
  border-radius: 6px;
  font-weight: 500;
}

.post-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  margin-top: 12px;
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

.action-btn svg {
  width: 18px;
  height: 18px;
}

@media (max-width: 768px) {
  .post-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .filter-tabs {
    width: 100%;
    justify-content: center;
  }
  
  .post-card {
    padding: 16px;
  }
  
  .post-actions {
    gap: 16px;
  }
}
</style>