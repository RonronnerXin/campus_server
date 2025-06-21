<template>
  <div class="blog-editor">
    <div class="page-header">
      <h1>{{ isEditMode ? '编辑博客' : '创建博客' }}</h1>
      <div class="header-actions">
        <button class="action-btn secondary" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          返回
        </button>
        <button class="action-btn primary" @click="saveDraft">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M7 11L12 6L17 11M12 18V7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          保存草稿
        </button>
        <button class="action-btn publish" @click="publishPost">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ isEditMode ? '更新' : '发布' }}
        </button>
      </div>
    </div>

    <div class="editor-form">
      <div class="form-row">
        <div class="form-group full-width">
          <label for="title">标题</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title" 
            class="form-control" 
            placeholder="请输入博客标题"
            maxlength="255"
          />
          <div class="character-count">{{ formData.title.length }}/255</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="category">分类</label>
          <select id="category" v-model="formData.category" class="form-control">
            <option value="tech">技术</option>
            <option value="life">生活</option>
            <option value="study">学习</option>
            <option value="travel">旅行</option>
            <option value="other">其他</option>
          </select>
        </div>

        <div class="form-group tags-group">
          <label>标签</label>
          <div class="tags-input-container">
            <div class="tags-list">
              <span 
                v-for="(tag, index) in formData.tags" 
                :key="index" 
                class="tag-item"
              >
                {{ tag }}
                <button class="remove-tag" @click="removeTag(index)">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </span>
            </div>
            <input 
              type="text" 
              v-model="tagInput" 
              @keydown.enter="addTag" 
              placeholder="输入标签后按回车添加" 
              class="tag-input"
            />
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group full-width">
          <label for="summary">摘要</label>
          <textarea 
            id="summary" 
            v-model="formData.summary" 
            class="form-control" 
            placeholder="请输入博客摘要，简要描述文章内容"
            rows="3"
            maxlength="500"
          ></textarea>
          <div class="character-count">{{ formData.summary.length }}/500</div>
        </div>
      </div>

      <div class="form-group">
        <label>封面图片</label>
        <div class="image-upload-container">
          <div 
            v-if="imagePreview" 
            class="image-preview"
          >
            <img :src="imagePreview" alt="封面预览" />
            <button class="remove-image" @click="removeImage">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          <div v-else class="upload-placeholder" @click="triggerImageUpload">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h7m5 5v5M9 8h5m8-1a4 4 0 11-8 0 4 4 0 018 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>点击上传封面图片</span>
          </div>
          <input 
            type="file" 
            ref="imageInput" 
            @change="handleImageUpload" 
            accept="image/*" 
            class="image-input"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="content">正文内容</label>
        <div class="editor-toolbar">
          <button 
            v-for="tool in editorTools" 
            :key="tool.name" 
            class="toolbar-btn" 
            @click="applyFormatting(tool.action)"
            :title="tool.title"
          >
            <span v-html="tool.icon"></span>
          </button>
        </div>
        <textarea 
          id="content" 
          v-model="formData.content" 
          class="form-control content-editor" 
          placeholder="在此输入博客正文内容..."
          rows="15"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group checkbox-group">
          <input type="checkbox" id="allow-comments" v-model="formData.allow_comments">
          <label for="allow-comments">允许评论</label>
        </div>
        <div class="form-group checkbox-group">
          <input type="checkbox" id="featured" v-model="formData.featured">
          <label for="featured">设为推荐</label>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn secondary" @click="goBack">取消</button>
        <button class="btn primary" @click="saveDraft">保存为草稿</button>
        <button class="btn publish" @click="publishPost">{{ isEditMode ? '更新博客' : '发布博客' }}</button>
      </div>
    </div>

    <!-- 确认离开弹窗 -->
    <div v-if="showLeaveConfirm" class="modal-overlay" @click="showLeaveConfirm = false">
      <div class="modal-content" @click.stop>
        <h3>确认离开？</h3>
        <p>您有未保存的更改，确定要离开吗？</p>
        <div class="modal-footer">
          <button class="btn secondary" @click="showLeaveConfirm = false">取消</button>
          <button class="btn primary" @click="confirmLeave">确认离开</button>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>{{ loadingMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { generalRequest } from '../services/genServ' // 根据实际路径调整

const router = useRouter()
const route = useRoute()
const imageInput = ref(null)
const tagInput = ref('')
const imagePreview = ref(null)
const imageFile = ref(null)
const showLeaveConfirm = ref(false)
const hasChanges = ref(false)
const loading = ref(false)
const loadingMessage = ref('保存中...')
const originalFormData = ref({})

// 判断是否为编辑模式
const isEditMode = computed(() => !!route.params.id)

// 表单数据
const formData = reactive({
  title: '',
  category: 'tech',
  summary: '',
  content: '',
  tags: [],
  allow_comments: true,
  featured: false,
  status: 'draft',
  images: []
})

// 编辑器工具栏
const editorTools = [
  { name: 'bold', title: '粗体', icon: '<b>B</b>', action: '**文本**' },
  { name: 'italic', title: '斜体', icon: '<i>I</i>', action: '*文本*' },
  { name: 'heading', title: '标题', icon: 'H', action: '## 标题' },
  { name: 'link', title: '链接', icon: '🔗', action: '[链接文本](URL)' },
  { name: 'list', title: '列表', icon: '•', action: '- 列表项' },
  { name: 'quote', title: '引用', icon: '"', action: '> 引用文本' },
  { name: 'code', title: '代码', icon: '&lt;/&gt;', action: '```\n代码\n```' },
  { name: 'image', title: '图片', icon: '🖼️', action: '![描述](图片URL)' }
]

// 添加标签
const addTag = () => {
  const tag = tagInput.value.trim()
  if (tag && !formData.tags.includes(tag)) {
    formData.tags.push(tag)
    hasChanges.value = true
  }
  tagInput.value = ''
}

// 移除标签
const removeTag = (index) => {
  formData.tags.splice(index, 1)
  hasChanges.value = true
}

// 触发图片上传
const triggerImageUpload = () => {
  imageInput.value.click()
}

// 处理图片上传
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
      hasChanges.value = true
    }
    reader.readAsDataURL(file)
  }
}

// 移除图片
const removeImage = () => {
  imagePreview.value = null
  imageFile.value = null
  imageInput.value.value = ''
  hasChanges.value = true
}

// 应用文本格式化
const applyFormatting = (formatPattern) => {
  const textarea = document.getElementById('content')
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = formData.content.substring(start, end)
  let replacement = ''

  if (selectedText) {
    // 如果有选中文本，将格式应用到选中文本
    if (formatPattern.includes('文本')) {
      replacement = formatPattern.replace('文本', selectedText)
    } else if (formatPattern.includes('标题')) {
      replacement = formatPattern.replace('标题', selectedText)
    } else if (formatPattern.includes('链接文本')) {
      replacement = formatPattern.replace('链接文本', selectedText).replace('URL', 'https://')
    } else if (formatPattern.includes('列表项')) {
      replacement = formatPattern.replace('列表项', selectedText)
    } else if (formatPattern.includes('引用文本')) {
      replacement = formatPattern.replace('引用文本', selectedText)
    } else if (formatPattern.includes('代码')) {
      replacement = formatPattern.replace('代码', selectedText)
    } else if (formatPattern.includes('描述')) {
      replacement = formatPattern.replace('描述', selectedText).replace('图片URL', 'https://')
    }
  } else {
    // 如果没有选中文本，使用默认模板
    replacement = formatPattern
  }

  // 更新文本区域内容
  formData.content = formData.content.substring(0, start) + replacement + formData.content.substring(end)
  
  // 重新聚焦文本区域并移动光标到插入内容之后
  setTimeout(() => {
    textarea.focus()
    const newPosition = start + replacement.length
    textarea.setSelectionRange(newPosition, newPosition)
  }, 0)
  
  hasChanges.value = true
}

// 保存为草稿
const saveDraft = async () => {
  formData.status = 'draft'
  await savePost()
}

// 发布博客
const publishPost = async () => {
  formData.status = 'published'
  await savePost()
}

// 保存文章
const savePost = async () => {
  // 表单验证
  if (!formData.title.trim()) {
    alert('请输入标题')
    return
  }
  
  if (!formData.summary.trim()) {
    alert('请输入摘要')
    return
  }
  
  if (!formData.content.trim()) {
    alert('请输入正文内容')
    return
  }

  loading.value = true
  loadingMessage.value = isEditMode.value ? '更新中...' : '保存中...'
  
  try {
    // 创建FormData对象
    const postData = new FormData()
    postData.append('title', formData.title)
    postData.append('category', formData.category)
    postData.append('summary', formData.summary)
    postData.append('content', formData.content)
    postData.append('allow_comments', formData.allow_comments)
    postData.append('featured', formData.featured)
    postData.append('status', formData.status)
    
    // 添加标签
    if (formData.tags.length > 0) {
      formData.tags.forEach(tag => {
        postData.append('tags', tag)
      })
    } else {
      postData.append('tags', [])
    }
    
    // 添加图片
    if (imageFile.value) {
      postData.append('images', imageFile.value)
    }
    
    if (isEditMode.value) {
      // 编辑模式 - 使用PUT请求更新
      if (formData.images.length === 0 && !imageFile.value) {
        postData.append('remove_cover', true)
      }
      
      const response = await generalRequest(`/api/blog-posts/${route.params.id}`, {
        method: 'PUT',
        data: postData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response) {
        hasChanges.value = false
        alert('博客更新成功！')
        router.push(`/blogdetail/${route.params.id}`)
      }
    } else {
      // 创建模式 - 使用POST请求创建
      const response = await generalRequest('/api/blog-posts/', {
        method: 'POST',
        data: postData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response && response.data) {
        hasChanges.value = false
        alert('博客创建成功！')
        router.push(`/blog/${response.data.id}`)
      }
    }
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 获取博客详情
const fetchBlogPost = async () => {
  if (!isEditMode.value) return
  
  loading.value = true
  loadingMessage.value = '加载中...'
  
  try {
    const response = await generalRequest(`/api/blog-posts/${route.params.id}`, {
      method: 'GET'
    })
    
    if (response) {
      const postData = response
      
      // 更新表单数据
      formData.title = postData.title
      formData.category = postData.category
      formData.summary = postData.summary
      formData.content = postData.content
      formData.tags = postData.tags || []
      formData.allow_comments = postData.allow_comments
      formData.featured = postData.featured
      formData.status = postData.status
      
      // 如果有封面图片
      if (postData.images && postData.images.length > 0) {
        formData.images = postData.images
        // 设置预览图
        if (postData.images[0]) {
          if (postData.images[0].startsWith('http')) {
            imagePreview.value = postData.images[0]
          } else {
            imagePreview.value = `http://localhost:8000${postData.images[0]}`
          }
        }
      }
      
      // 保存初始数据，用于检测变更
      originalFormData.value = JSON.parse(JSON.stringify(formData))
      hasChanges.value = false
    }
  } catch (error) {
    console.error('获取博客详情失败:', error)
    alert('获取博客详情失败，请稍后重试')
    router.push('/profile')
  } finally {
    loading.value = false
  }
}

// 返回
const goBack = () => {
  if (hasChanges.value) {
    showLeaveConfirm.value = true
  } else {
    router.push('/profile')
  }
}

// 确认离开
const confirmLeave = () => {
  showLeaveConfirm.value = false
  router.push('/profile')
}

// 检测表单变更
const checkFormChanges = () => {
  if (isEditMode.value && Object.keys(originalFormData.value).length > 0) {
    // 编辑模式，比较与原始数据
    if (
      formData.title !== originalFormData.value.title ||
      formData.category !== originalFormData.value.category ||
      formData.summary !== originalFormData.value.summary ||
      formData.content !== originalFormData.value.content ||
      formData.allow_comments !== originalFormData.value.allow_comments ||
      formData.featured !== originalFormData.value.featured ||
      JSON.stringify(formData.tags) !== JSON.stringify(originalFormData.value.tags) ||
      imageFile.value !== null
    ) {
      hasChanges.value = true
    } else {
      hasChanges.value = false
    }
  } else if (!isEditMode.value) {
    // 创建模式，检查是否有任何内容
    if (
      formData.title.trim() !== '' ||
      formData.summary.trim() !== '' ||
      formData.content.trim() !== '' ||
      formData.tags.length > 0 ||
      imageFile.value !== null
    ) {
      hasChanges.value = true
    } else {
      hasChanges.value = false
    }
  }
}

// 离开前确认
const beforeUnload = (e) => {
  if (hasChanges.value) {
    e.preventDefault()
    e.returnValue = ''
    return ''
  }
}

// 监听路由变化
const beforeRouteLeave = (to, from, next) => {
  if (hasChanges.value) {
    showLeaveConfirm.value = true
    next(false)
  } else {
    next()
  }
}

// 生命周期钩子
onMounted(() => {
  // 获取博客详情（如果是编辑模式）
  fetchBlogPost()
  
  // 监听表单变更
  window.addEventListener('beforeunload', beforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', beforeUnload)
})
</script>

<style scoped>
.blog-editor {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f3f4;
  padding: 24px;
  position: relative;
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

.header-actions {
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
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #4b5563;
}

.action-btn.secondary:hover {
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

.action-btn.publish {
  background: #10b981;
  color: #ffffff;
}

.action-btn.publish:hover {
  background: #059669;
}

.editor-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  flex: 1 1 100%;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
}

.form-control {
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #f9fafb;
  color: #1f2937;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control.content-editor {
  min-height: 300px;
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

.character-count {
  text-align: right;
  font-size: 12px;
  color: #9ca3af;
}

.tags-input-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px;
  background: #f9fafb;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: #eef2ff;
  color: #667eea;
  border-radius: 4px;
  font-size: 12px;
}

.remove-tag {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: #667eea;
  cursor: pointer;
  padding: 0;
}

.remove-tag:hover {
  background: rgba(102, 126, 234, 0.1);
}

.remove-tag svg {
  width: 12px;
  height: 12px;
}

.tag-input {
  border: none;
  background: transparent;
  padding: 8px;
  font-size: 14px;
  color: #1f2937;
  width: 100%;
}

.tag-input:focus {
  outline: none;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.checkbox-group input[type="checkbox"] {
  width: 16px;
  height: 16px;
}

.image-upload-container {
  width: 100%;
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-placeholder:hover {
  background: #f3f4f6;
}

.upload-placeholder svg {
  width: 48px;
  height: 48px;
  color: #9ca3af;
  margin-bottom: 12px;
}

.upload-placeholder span {
  color: #6b7280;
  font-size: 14px;
}

.image-input {
  display: none;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 200px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-image:hover {
  background: #ffffff;
}

.remove-image svg {
  width: 16px;
  height: 16px;
  color: #ef4444;
}

.editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px;
  background: #f3f4f6;
  border-radius: 8px 8px 0 0;
  border: 1px solid #e5e7eb;
  border-bottom: none;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.toolbar-btn:hover {
  background: #eef2ff;
  border-color: #667eea;
  color: #667eea;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 12px;
}

.btn {
  padding: 10px 16px;
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

.btn.publish {
  background: #10b981;
  color: #ffffff;
}

.btn.publish:hover {
  background: #059669;
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
  margin-bottom: 8px;
}

.modal-content p {
  color: #4b5563;
  margin-bottom: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
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

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .action-btn {
    flex: 1;
    justify-content: center;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>