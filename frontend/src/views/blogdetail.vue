<template>
  <div class="blog-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 内容区域 -->
    <template v-else-if="article">
      <!-- 返回按钮 -->
      <div class="back-button" @click="goBack">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>返回列表</span>
      </div>
      
      <!-- 文章头部 -->
      <div class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <div class="author-info">
            <img :src="article.author.avatar" :alt="article.author.name" class="author-avatar" />
            <span class="author-name">{{ article.author.name }}</span>
          </div>
          <div class="meta-divider"></div>
          <div class="meta-item">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ formatDate(article.published_at) }}</span>
          </div>
          <div class="meta-divider"></div>
          <div class="meta-item">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ article.views_count }} 阅读</span>
          </div>
        </div>
        
        <!-- 分类和标签 -->
        <div class="article-categories">
          <div class="category-tag">
            <span class="category-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M7 7h.01M7 3h5a1.99 1.99 0 011.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.995 1.995 0 013 12V7a4 4 0 014-4z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            <span class="category-name">{{ article.category }}</span>
          </div>
          <div v-for="tag in article.tags" :key="tag" class="tag">{{ tag }}</div>
        </div>
      </div>
      
      <!-- 封面图 -->
      <div v-if="article.cover_image" class="cover-image-container">
        <img :src="article.cover_image" :alt="article.title" class="cover-image" />
      </div>
      
      <!-- 文章内容 -->
      <div class="article-content" v-html="article.content"></div>
      
      <!-- 文章底部 -->
      <div class="article-footer">
        <div class="article-actions">
          <button class="action-btn like-btn" :class="{ active: article.liked }" @click="toggleLike">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ article.likes_count }} 喜欢</span>
          </button>
          <button class="action-btn" @click="scrollToComments">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ article.comments_count }} 评论</span>
          </button>
          <button class="action-btn" @click="shareArticle">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>分享</span>
          </button>
          <button v-if="isAuthor" class="action-btn edit-btn" @click="editArticle">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>编辑</span>
          </button>
        </div>
        
        <!-- 作者信息卡片 -->
        <div class="author-card">
          <div class="author-card-header">
            <img :src="article.author.avatar" :alt="article.author.name" class="author-card-avatar" />
            <div class="author-card-info">
              <h3 class="author-card-name">{{ article.author.name }}</h3>
              <p class="author-card-bio">{{ article.author.bio || '这个人很懒，什么都没留下' }}</p>
            </div>
          </div>
          <div class="author-card-stats">
            <div class="stat-item">
              <span class="stat-value">{{ article.author.articles_count }}</span>
              <span class="stat-label">文章</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ article.author.followers_count }}</span>
              <span class="stat-label">关注者</span>
            </div>
          </div>
          <button class="follow-btn" :class="{ following: article.author.is_following }" @click="toggleFollow">
            {{ article.author.is_following ? '已关注' : '关注作者' }}
          </button>
        </div>
      </div>
      
      <!-- 评论区 -->
      <div id="comments" class="comments-section">
        <h2 class="section-title">评论 ({{ article.comments_count }})</h2>
        
        <!-- 评论输入框 -->
        <div class="comment-form">
          <div class="comment-avatar">
            <img :src="currentUserAvatar" alt="Your Avatar" />
          </div>
          <div class="comment-input-container">
            <textarea 
              v-model="commentContent" 
              class="comment-input" 
              placeholder="写下你的评论..."
              rows="3"
            ></textarea>
            <button 
              class="comment-submit" 
              :disabled="!commentContent.trim()" 
              @click="submitComment"
            >
              发布评论
            </button>
          </div>
        </div>
        
        <!-- 评论列表 -->
        <div v-if="comments.length > 0" class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-avatar">
              <img :src="comment.user.avatar" :alt="comment.user.name" />
            </div>
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-author">{{ comment.user.name }}</span>
                <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
              <div class="comment-actions">
                <button class="comment-action" @click="toggleCommentLike(comment)">
                  <svg viewBox="0 0 24 24" fill="none" :class="{ 'liked': comment.liked }">
                    <path d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>{{ comment.likes_count }}</span>
                </button>
                <button class="comment-action" @click="replyToComment(comment)">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>回复</span>
                </button>
                <button v-if="isCommentAuthor(comment)" class="comment-action" @click="deleteComment(comment)">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>删除</span>
                </button>
              </div>
              
              <!-- 回复列表 -->
              <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
                <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                  <div class="comment-avatar small">
                    <img :src="reply.user.avatar" :alt="reply.user.name" />
                  </div>
                  <div class="reply-content">
                    <div class="comment-header">
                      <span class="comment-author">{{ reply.user.name }}</span>
                      <span v-if="reply.reply_to" class="reply-to">
                        回复 <span class="reply-to-name">@{{ reply.reply_to.name }}</span>
                      </span>
                      <span class="comment-time">{{ formatDate(reply.created_at) }}</span>
                    </div>
                    <p class="comment-text">{{ reply.content }}</p>
                    <div class="comment-actions">
                      <button class="comment-action" @click="toggleReplyLike(reply)">
                        <svg viewBox="0 0 24 24" fill="none" :class="{ 'liked': reply.liked }">
                          <path d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>{{ reply.likes_count }}</span>
                      </button>
                      <button class="comment-action" @click="replyToComment(comment, reply.user)">
                        <svg viewBox="0 0 24 24" fill="none">
                          <path d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>回复</span>
                      </button>
                      <button v-if="isReplyAuthor(reply)" class="comment-action" @click="deleteReply(comment, reply)">
                        <svg viewBox="0 0 24 24" fill="none">
                          <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>删除</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 回复输入框 -->
              <div v-if="replyingTo && replyingTo.commentId === comment.id" class="reply-form">
                <div class="comment-avatar small">
                  <img :src="currentUserAvatar" alt="Your Avatar" />
                </div>
                <div class="reply-input-container">
                  <textarea 
                    v-model="replyContent" 
                    class="reply-input" 
                    :placeholder="replyingTo.user ? `回复 @${replyingTo.user.name}...` : '写下你的回复...'"
                    rows="2"
                  ></textarea>
                  <div class="reply-actions">
                    <button class="cancel-reply" @click="cancelReply">取消</button>
                    <button 
                      class="submit-reply" 
                      :disabled="!replyContent.trim()" 
                      @click="submitReply(comment)"
                    >
                      回复
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 无评论状态 -->
        <div v-else class="no-comments">
          <svg viewBox="0 0 24 24" fill="none" class="no-comments-icon">
            <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>暂无评论，快来发表第一条评论吧！</p>
        </div>
        
        <!-- 加载更多评论 -->
        <div v-if="hasMoreComments" class="load-more">
          <button class="load-more-btn" @click="loadMoreComments">
            加载更多评论
          </button>
        </div>
      </div>
      
      <!-- 相关文章 -->
      <div class="related-articles">
        <h2 class="section-title">相关文章</h2>
        <div class="related-articles-grid">
          <div 
            v-for="relatedArticle in relatedArticles" 
            :key="relatedArticle.id" 
            class="related-article-card"
            @click="viewArticle(relatedArticle.id)"
          >
            <div class="related-article-image">
              <img :src="relatedArticle.cover_image || getDefaultCoverImage()" :alt="relatedArticle.title" />
            </div>
            <div class="related-article-content">
              <h3 class="related-article-title">{{ relatedArticle.title }}</h3>
              <div class="related-article-meta">
                <span class="related-article-author">{{ relatedArticle.author.name }}</span>
                <span class="meta-divider">·</span>
                <span class="related-article-date">{{ formatDate(relatedArticle.published_at, true) }}</span>
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
      <h2>文章未找到</h2>
      <p>该文章可能已被删除或您没有权限查看</p>
      <button class="primary-btn" @click="goBack">返回列表</button>
    </div>
    
    <!-- 分享对话框 -->
    <div v-if="showShareDialog" class="modal-overlay" @click="showShareDialog = false">
      <div class="modal-container share-dialog" @click.stop>
        <h3>分享文章</h3>
        <div class="share-options">
          <button class="share-option wechat">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M9.5 9.5C9.5 8.12 10.62 7 12 7s2.5 1.12 2.5 2.5S13.38 12 12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 12v3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 21a9 9 0 100-18 9 9 0 000 18z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>微信</span>
          </button>
          <button class="share-option weibo">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M9.5 9.5C9.5 8.12 10.62 7 12 7s2.5 1.12 2.5 2.5S13.38 12 12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 12v3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 21a9 9 0 100-18 9 9 0 000 18z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>微博</span>
          </button>
          <button class="share-option qq">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M9.5 9.5C9.5 8.12 10.62 7 12 7s2.5 1.12 2.5 2.5S13.38 12 12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 12v3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 21a9 9 0 100-18 9 9 0 000 18z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>QQ</span>
          </button>
        </div>
        <div class="share-link">
          <input type="text" :value="articleUrl" readonly class="share-link-input" />
          <button class="copy-link-btn" @click="copyArticleLink">复制链接</button>
        </div>
        <button class="close-dialog" @click="showShareDialog = false">关闭</button>
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
const articleId = computed(() => route.params.id)

const article = ref(null)
const comments = ref([])
const relatedArticles = ref([])
const loading = ref(true)
const commentContent = ref('')
const replyContent = ref('')
const replyingTo = ref(null)
const showShareDialog = ref(false)
const commentsPage = ref(1)
const hasMoreComments = ref(false)

// 当前用户信息 (实际应用中应从用户状态获取)
const currentUserId = ref('user-123') // 示例ID，实际使用时应替换
const currentUserAvatar = ref('https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=40&h=40&fit=crop&crop=face')

// 文章URL
const articleUrl = computed(() => {
  return `${window.location.origin}/blog/${articleId.value}`
})

// 判断当前用户是否为文章作者
const isAuthor = computed(() => {
  return article.value && article.value.author.id === currentUserId.value
})

// 获取文章详情
const fetchArticleDetail = async () => {
  loading.value = true
  try {
    const response = await generalRequest(`/api/articles/${articleId.value}`, {
      method: 'GET'
    })
    
    if (response && response.data) {
      article.value = response.data
      // 获取评论
      fetchComments()
      // 获取相关文章
      fetchRelatedArticles()
    } else {
      console.error('获取文章详情失败:', response)
      article.value = null
    }
  } catch (error) {
    console.error('获取文章详情出错:', error)
    article.value = null
  } finally {
    loading.value = false
  }
}

// 获取文章评论
const fetchComments = async () => {
  try {
    const response = await generalRequest(`/api/articles/${articleId.value}/comments`, {
      method: 'GET',
      params: {
        page: commentsPage.value,
        per_page: 10
      }
    })
    
    if (response && response.data) {
      if (commentsPage.value === 1) {
        comments.value = response.data.data
      } else {
        comments.value = [...comments.value, ...response.data.data]
      }
      
      hasMoreComments.value = response.data.current_page < response.data.total_pages
    }
  } catch (error) {
    console.error('获取评论失败:', error)
  }
}

// 加载更多评论
const loadMoreComments = () => {
  commentsPage.value++
  fetchComments()
}

// 获取相关文章
const fetchRelatedArticles = async () => {
  if (!article.value) return
  
  try {
    const response = await generalRequest('/api/articles', {
      method: 'GET',
      params: {
        category: article.value.category,
        exclude: articleId.value,
        limit: 3
      }
    })
    
    if (response && response.data && response.data.data) {
      relatedArticles.value = response.data.data.slice(0, 3)
    }
  } catch (error) {
    console.error('获取相关文章失败:', error)
    relatedArticles.value = []
  }
}

// 提交评论
const submitComment = async () => {
  if (!commentContent.value.trim()) return
  
  try {
    const response = await generalRequest(`/api/articles/${articleId.value}/comments`, {
      method: 'POST',
      data: {
        content: commentContent.value
      }
    })
    
    if (response && response.data) {
      // 添加新评论到列表顶部
      comments.value.unshift(response.data)
      // 更新文章评论数
      if (article.value) {
        article.value.comments_count++
      }
      // 清空输入框
      commentContent.value = ''
    }
  } catch (error) {
    console.error('提交评论失败:', error)
    alert('评论发布失败，请稍后再试')
  }
}

// 回复评论
const replyToComment = (comment, replyToUser = null) => {
  replyingTo.value = {
    commentId: comment.id,
    user: replyToUser
  }
  replyContent.value = ''
  
  // 滚动到回复框
  setTimeout(() => {
    const replyForm = document.querySelector('.reply-form')
    if (replyForm) {
      replyForm.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }, 100)
}

// 取消回复
const cancelReply = () => {
  replyingTo.value = null
  replyContent.value = ''
}

// 提交回复
const submitReply = async (comment) => {
  if (!replyContent.value.trim() || !replyingTo.value) return
  
  try {    const response = await generalRequest(`/api/articles/${articleId.value}/comments/${comment.id}/replies`, {
      method: 'POST',
      data: {
        content: replyContent.value,
        reply_to_id: replyingTo.value.user ? replyingTo.value.user.id : null
      }
    })
    
    if (response && response.data) {
      // 确保评论有replies数组
      if (!comment.replies) {
        comment.replies = []
      }
      
      // 添加新回复到列表
      comment.replies.push(response.data)
      
      // 更新文章评论数
      if (article.value) {
        article.value.comments_count++
      }
      
      // 清空输入框并关闭回复框
      replyContent.value = ''
      replyingTo.value = null
    }
  } catch (error) {
    console.error('提交回复失败:', error)
    alert('回复发布失败，请稍后再试')
  }
}

// 点赞文章
const toggleLike = async () => {
  if (!article.value) return
  
  try {
    const method = article.value.liked ? 'DELETE' : 'POST'
    const response = await generalRequest(`/api/articles/${articleId.value}/like`, {
      method
    })
    
    if (response) {
      // 更新点赞状态
      article.value.liked = !article.value.liked
      // 更新点赞数
      article.value.likes_count += article.value.liked ? 1 : -1
    }
  } catch (error) {
    console.error('点赞操作失败:', error)
  }
}

// 点赞评论
const toggleCommentLike = async (comment) => {
  try {
    const method = comment.liked ? 'DELETE' : 'POST'
    const response = await generalRequest(`/api/comments/${comment.id}/like`, {
      method
    })
    
    if (response) {
      // 更新点赞状态
      comment.liked = !comment.liked
      // 更新点赞数
      comment.likes_count += comment.liked ? 1 : -1
    }
  } catch (error) {
    console.error('评论点赞操作失败:', error)
  }
}

// 点赞回复
const toggleReplyLike = async (reply) => {
  try {
    const method = reply.liked ? 'DELETE' : 'POST'
    const response = await generalRequest(`/api/replies/${reply.id}/like`, {
      method
    })
    
    if (response) {
      // 更新点赞状态
      reply.liked = !reply.liked
      // 更新点赞数
      reply.likes_count += reply.liked ? 1 : -1
    }
  } catch (error) {
    console.error('回复点赞操作失败:', error)
  }
}

// 删除评论
const deleteComment = async (comment) => {
  if (!confirm('确定要删除这条评论吗？')) return
  
  try {
    const response = await generalRequest(`/api/comments/${comment.id}`, {
      method: 'DELETE'
    })
    
    if (response) {
      // 从列表中移除评论
      comments.value = comments.value.filter(c => c.id !== comment.id)
      // 更新文章评论数
      if (article.value) {
        article.value.comments_count -= 1 + (comment.replies ? comment.replies.length : 0)
      }
    }
  } catch (error) {
    console.error('删除评论失败:', error)
    alert('删除失败，请稍后再试')
  }
}

// 删除回复
const deleteReply = async (comment, reply) => {
  if (!confirm('确定要删除这条回复吗？')) return
  
  try {
    const response = await generalRequest(`/api/replies/${reply.id}`, {
      method: 'DELETE'
    })
    
    if (response) {
      // 从列表中移除回复
      comment.replies = comment.replies.filter(r => r.id !== reply.id)
      // 更新文章评论数
      if (article.value) {
        article.value.comments_count--
      }
    }
  } catch (error) {
    console.error('删除回复失败:', error)
    alert('删除失败，请稍后再试')
  }
}

// 关注/取消关注作者
const toggleFollow = async () => {
  if (!article.value || !article.value.author) return
  
  try {
    const method = article.value.author.is_following ? 'DELETE' : 'POST'
    const response = await generalRequest(`/api/users/${article.value.author.id}/follow`, {
      method
    })
    
    if (response) {
      // 更新关注状态
      article.value.author.is_following = !article.value.author.is_following
      // 更新关注者数量
      article.value.author.followers_count += article.value.author.is_following ? 1 : -1
    }
  } catch (error) {
    console.error('关注操作失败:', error)
  }
}

// 分享文章
const shareArticle = () => {
  showShareDialog.value = true
}

// 复制文章链接
const copyArticleLink = () => {
  navigator.clipboard.writeText(articleUrl.value)
    .then(() => alert('链接已复制到剪贴板'))
    .catch(err => console.error('复制失败:', err))
}

// 编辑文章
const editArticle = () => {
  router.push(`/blog/edit/${articleId.value}`)
}

// 查看其他文章
const viewArticle = (id) => {
  router.push(`/blog/${id}`)
}

// 滚动到评论区
const scrollToComments = () => {
  document.getElementById('comments').scrollIntoView({ behavior: 'smooth' })
}

// 返回列表页
const goBack = () => {
  router.push('/blog')
}

// 格式化日期
const formatDate = (dateString, short = false) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  
  if (short) {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  }
  
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取默认封面图
const getDefaultCoverImage = () => {
  return 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&h=400&fit=crop'
}

// 判断当前用户是否为评论作者
const isCommentAuthor = (comment) => {
  return comment.user.id === currentUserId.value
}

// 判断当前用户是否为回复作者
const isReplyAuthor = (reply) => {
  return reply.user.id === currentUserId.value
}

// 监听路由参数变化
watch(() => route.params.id, (newId) => {
  if (newId) {
    commentsPage.value = 1
    fetchArticleDetail()
  }
}, { immediate: true })
</script>

<style scoped>
.blog-detail-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

.back-button {
  display: inline-flex;
  align-items: center;
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

.article-header {
  margin-bottom: 32px;
}

.article-title {
  font-size: 36px;
  font-weight: 800;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  line-height: 1.2;
}

.article-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.meta-divider {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #d1d5db;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6b7280;
}

.meta-item svg {
  width: 18px;
  height: 18px;
}

.article-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}

.category-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #eef2ff;
  border-radius: 20px;
  color: #4f46e5;
  font-size: 14px;
  font-weight: 500;
}

.category-icon {
  display: flex;
  align-items: center;
}

.category-icon svg {
  width: 16px;
  height: 16px;
}

.tag {
  padding: 6px 12px;
  background: #f3f4f6;
  border-radius: 20px;
  color: #4b5563;
  font-size: 14px;
}

.cover-image-container {
  width: 100%;
  height: 400px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 32px;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  font-size: 18px;
  line-height: 1.8;
  color: #1f2937;
  margin-bottom: 48px;
}

.article-content p {
  margin-bottom: 24px;
}

.article-content h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 40px 0 16px;
}

.article-content h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 32px 0 16px;
}

.article-content img {
  max-width: 100%;
  border-radius: 8px;
  margin: 24px 0;
}

.article-content a {
  color: #4f46e5;
  text-decoration: none;
}

.article-content a:hover {
  text-decoration: underline;
}

.article-content blockquote {
  border-left: 4px solid #e5e7eb;
  padding-left: 16px;
  margin-left: 0;
  color: #6b7280;
  font-style: italic;
}

.article-content code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9em;
}

.article-content pre {
  background: #1f2937;
  color: #f9fafb;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: monospace;
  font-size: 0.9em;
}

.article-footer {
  border-top: 1px solid #e5e7eb;
  padding-top: 32px;
  margin-bottom: 48px;
}

.article-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 32px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #f3f4f6;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.action-btn svg {
  width: 20px;
  height: 20px;
}

.like-btn.active {
  background: #fee2e2;
  color: #ef4444;
}

.like-btn.active svg {
  fill: #ef4444;
  stroke: #ef4444;
}

.edit-btn {
  margin-left: auto;
}

.author-card {
  background: #f9fafb;
  border-radius: 16px;
  padding: 24px;
  margin-top: 32px;
}

.author-card-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.author-card-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
}

.author-card-info {
  flex: 1;
}

.author-card-name {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.author-card-bio {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.author-card-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.follow-btn {
  width: 100%;
  padding: 12px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.follow-btn:hover {
  background: #4338ca;
}

.follow-btn.following {
  background: #f3f4f6;
  color: #4b5563;
}

.follow-btn.following:hover {
  background: #e5e7eb;
}

.comments-section {
  margin-bottom: 48px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.comment-form {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.comment-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.comment-avatar.small {
  width: 32px;
  height: 32px;
}

.comment-input-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.comment-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  resize: vertical;
  min-height: 100px;
  margin-bottom: 16px;
  transition: all 0.2s ease;
}

.comment-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.comment-submit {
  align-self: flex-end;
  padding: 10px 20px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.comment-submit:hover {
  background: #4338ca;
}

.comment-submit:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.comment-item {
  display: flex;
  gap: 16px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.comment-time {
  font-size: 14px;
  color: #6b7280;
}

.comment-text {
  font-size: 16px;
  line-height: 1.6;
  color: #4b5563;
  margin-bottom: 12px;
}

.comment-actions {
  display: flex;
  gap: 16px;
}

.comment-action {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
}

.comment-action:hover {
  color: #4b5563;
}

.comment-action svg {
  width: 16px;
  height: 16px;
}

.comment-action svg.liked {
  fill: #ef4444;
  stroke: #ef4444;
}

.replies-list {
  margin-top: 16px;
  margin-left: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reply-item {
  display: flex;
  gap: 12px;
}

.reply-content {
  flex: 1;
}

.reply-to {
  font-size: 14px;
  color: #6b7280;
}

.reply-to-name {
  color: #4f46e5;
}

.reply-form {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  margin-left: 24px;
}

.reply-input-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.reply-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  min-height: 80px;
  margin-bottom: 12px;
  transition: all 0.2s ease;
}

.reply-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.reply-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-reply {
  padding: 8px 16px;
  background: #f3f4f6;
  color: #4b5563;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-reply:hover {
  background: #e5e7eb;
}

.submit-reply {
  padding: 8px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-reply:hover {
  background: #4338ca;
}

.submit-reply:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.no-comments {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 0;
  color: #6b7280;
}

.no-comments-icon {
  width: 48px;
  height: 48px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.load-more {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.load-more-btn {
  padding: 10px 20px;
  background: #f3f4f6;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s ease;
}

.load-more-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.related-articles {
  margin-bottom: 48px;
}

.related-articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.related-article-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.related-article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.related-article-image {
  height: 160px;
}

.related-article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-article-content {
  padding: 16px;
}

.related-article-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
}

.related-article-author {
  font-weight: 500;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f4f6;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
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

.primary-btn {
  padding: 12px 24px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  background: #4338ca;
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

.share-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.share-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.share-option svg {
  width: 24px;
  height: 24px;
}

.share-option.wechat {
  background: #f6ffed;
  color: #52c41a;
}

.share-option.wechat:hover {
  background: #d9f7be;
}

.share-option.weibo {
  background: #fff2e8;
  color: #fa8c16;
}

.share-option.weibo:hover {
  background: #ffe7ba;
}

.share-option.qq {
  background: #e6f7ff;
  color: #1890ff;
}

.share-option.qq:hover {
  background: #bae7ff;
}

.share-link {
  display: flex;
  margin-bottom: 24px;
}

.share-link-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px 0 0 8px;
  font-size: 14px;
}

.copy-link-btn {
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-link-btn:hover {
  background: #4338ca;
}

.close-dialog {
  width: 100%;
  padding: 10px;
  background: #f3f4f6;
  color: #4b5563;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-dialog:hover {
  background: #e5e7eb;
}

@media (max-width: 768px) {
  .article-title {
    font-size: 28px;
  }
  
  .cover-image-container {
    height: 250px;
  }
  
  .article-content {
    font-size: 16px;
  }
  
  .article-actions {
    justify-content: space-between;
  }
  
  .action-btn {
    padding: 8px 12px;
    font-size: 14px;
  }
  
  .edit-btn {
    margin-left: 0;
  }
  
  .related-articles-grid {
    grid-template-columns: 1fr;
  }
}
</style>