<template>
  <div class="lost-item-editor">
    <div class="page-header">
      <h1>{{ isEditMode ? '编辑失物招领' : '发布失物招领' }}</h1>
      <div class="header-actions">
        <button class="action-btn secondary" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          返回
        </button>
        <button class="action-btn primary" @click="submitForm">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ isEditMode ? '更新' : '发布' }}
        </button>
      </div>
    </div>

    <div class="editor-form">
      <div class="form-row">
        <div class="form-group">
          <label for="type">信息类型</label>
          <div class="radio-buttons">
            <label class="radio-label">
              <input type="radio" id="type-lost" name="type" value="lost" v-model="formData.type">
              <span class="radio-text">寻物启事</span>
            </label>
            <label class="radio-label">
              <input type="radio" id="type-found" name="type" value="found" v-model="formData.type">
              <span class="radio-text">招领启事</span>
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="category">物品分类</label>
          <select id="category" v-model="formData.category" class="form-control">
            <option value="card">校园卡</option>
            <option value="electronics">电子设备</option>
            <option value="books">书籍资料</option>
            <option value="clothing">衣物</option>
            <option value="other">其他</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group full-width">
          <label for="title">标题</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title" 
            class="form-control" 
            placeholder="请简要描述物品特征，如：黑色钱包，内有学生证"
            maxlength="50"
          />
          <div class="character-count">{{ formData.title.length }}/50</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="location">地点</label>
          <input 
            type="text" 
            id="location" 
            v-model="formData.location" 
            class="form-control" 
            placeholder="丢失/拾获地点，如：图书馆三楼"
          />
        </div>
        
        <div class="form-group">
          <label for="time">时间</label>
          <input 
            type="datetime-local" 
            id="time" 
            v-model="formData.time" 
            class="form-control"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="description">详细描述</label>
        <textarea 
          id="description" 
          v-model="formData.description" 
          class="form-control" 
          placeholder="请详细描述物品特征、丢失/拾获经过等信息，有助于失主/拾主确认"
          rows="6"
        ></textarea>
      </div>

      <div class="form-group">
        <label>图片上传</label>
        <div class="images-container">
          <div 
            v-for="(image, index) in imageList" 
            :key="index" 
            class="image-preview-item"
          >
            <img :src="image.preview" alt="物品图片" />
            <button class="remove-image" @click="removeImage(index)">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          
          <div 
            v-if="imageList.length < 3" 
            class="image-upload-box" 
            @click="triggerImageUpload"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 5v14m-7-7h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>添加图片</span>
          </div>
        </div>
        <div class="form-hint">最多上传3张图片，每张不超过2MB</div>
        <input 
          type="file" 
          ref="imageInput" 
          @change="handleImageUpload" 
          accept="image/*" 
          class="image-input"
        />
      </div>

      <div class="form-section">
        <h3>联系方式</h3>
        <div class="form-row">
          <div class="form-group">
            <label for="contact-type">联系方式类型</label>
            <select id="contact-type" v-model="formData.contact_type" class="form-control">
              <option value="phone">手机号码</option>
              <option value="wechat">微信号</option>
              <option value="qq">QQ号</option>
              <option value="email">邮箱</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="contact-value">联系方式</label>
            <input 
              type="text" 
              id="contact-value" 
              v-model="formData.contact_value" 
              class="form-control" 
              placeholder="填写对应的联系方式"
            />
          </div>
        </div>
        
        <div class="form-group checkbox-group">
          <input type="checkbox" id="hide-contact" v-model="formData.hide_contact">
          <label for="hide-contact">隐藏联系方式（他人需通过站内消息与您联系）</label>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn secondary" @click="goBack">取消</button>
        <button class="btn primary" @click="submitForm">{{ isEditMode ? '更新信息' : '发布信息' }}</button>
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
const imageList = ref([])
const showLeaveConfirm = ref(false)
const hasChanges = ref(false)
const loading = ref(false)
const loadingMessage = ref('保存中...')
const originalFormData = ref({})

// 判断是否为编辑模式
const isEditMode = computed(() => !!route.params.id)

// 获取当前时间（格式化为datetime-local输入框支持的格式）
const getCurrentDateTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

// 表单数据
const formData = reactive({
  type: 'lost',  // 默认为寻物启事
  title: '',
  category: 'other',
  description: '',
  location: '',
  time: getCurrentDateTime(),
  contact_type: 'phone',
  contact_value: '',
  hide_contact: false,
  status: 'unclaimed'  // 默认为未认领
})

// 触发图片上传
const triggerImageUpload = () => {
  imageInput.value.click()
}

// 处理图片上传
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件大小（最大2MB）
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过2MB')
    return
  }
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    alert('请上传图片文件')
    return
  }
  
  // 限制最多3张图片
  if (imageList.value.length >= 3) {
    alert('最多上传3张图片')
    return
  }
  
  // 创建预览
  const reader = new FileReader()
  reader.onload = (e) => {
    imageList.value.push({
      file: file,
      preview: e.target.result
    })
    hasChanges.value = true
  }
  reader.readAsDataURL(file)
  
  // 清空input，使得可以上传相同的图片
  event.target.value = ''
}

// 移除图片
const removeImage = (index) => {
  imageList.value.splice(index, 1)
  hasChanges.value = true
}

// 提交表单
const submitForm = async () => {
  // 表单验证
  if (!formData.title.trim()) {
    alert('请输入标题')
    return
  }
  
  if (!formData.location.trim()) {
    alert('请输入地点')
    return
  }
  
  if (!formData.description.trim()) {
    alert('请输入详细描述')
    return
  }
  
  if (!formData.contact_value.trim() && !formData.hide_contact) {
    alert('请输入联系方式或选择隐藏联系方式')
    return
  }

  loading.value = true
  loadingMessage.value = isEditMode.value ? '更新中...' : '发布中...'
  
  try {
    // 创建FormData对象
    const postData = new FormData()
    postData.append('type', formData.type)
    postData.append('title', formData.title)
    postData.append('category', formData.category)
    postData.append('description', formData.description)
    postData.append('location', formData.location)
    postData.append('time', new Date(formData.time).toISOString())
    postData.append('contact_type', formData.contact_type)
    postData.append('contact_value', formData.contact_value)
    postData.append('hide_contact', formData.hide_contact)
    postData.append('status', formData.status)
    
    // 添加图片
    imageList.value.forEach(image => {
      if (image.file) {
        postData.append('images', image.file)
      }
    })
    
    if (isEditMode.value) {
      // 编辑模式 - 使用PUT请求更新
      const response = await generalRequest(`/api/lost-items/${route.params.id}`, {
        method: 'PUT',
        data: postData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response) {
        hasChanges.value = false
        alert('信息更新成功！')
        router.push(`/lostitemdetail/${route.params.id}`)
      }
    } else {
      // 创建模式 - 使用POST请求创建
      const response = await generalRequest('/api/lost-items/', {
        method: 'POST',
        data: postData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response && response.data) {
        hasChanges.value = false
        alert('信息发布成功！')
        router.push(`/lost-found/${response.data.id}`)
      }
    }
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 获取失物招领详情
const fetchLostItem = async () => {
  if (!isEditMode.value) return
  
  loading.value = true
  loadingMessage.value = '加载中...'
  
  try {
    const response = await generalRequest(`/api/lost-items/${route.params.id}`, {
      method: 'GET'
    })
    
    if (response) {
      const itemData = response
      
      // 更新表单数据
      formData.type = itemData.type
      formData.title = itemData.title
      formData.category = itemData.category
      formData.description = itemData.description
      formData.location = itemData.location
      
      // 格式化时间为datetime-local输入框支持的格式
      if (itemData.time) {
        const date = new Date(itemData.time)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        const hours = String(date.getHours()).padStart(2, '0')
        const minutes = String(date.getMinutes()).padStart(2, '0')
        
        formData.time = `${year}-${month}-${day}T${hours}:${minutes}`
      }
      
      formData.contact_type = itemData.contact_type
      formData.contact_value = itemData.contact_value
      formData.hide_contact = itemData.hide_contact
      formData.status = itemData.status
      
      // 如果有图片
      if (itemData.images && itemData.images.length > 0) {
        itemData.images.forEach(imageUrl => {
          // 判断是否为完整URL
          const fullUrl = imageUrl.startsWith('http') 
            ? imageUrl 
            : `http://localhost:8000${imageUrl}`
          
          imageList.value.push({
            preview: fullUrl,
            isExisting: true,  // 标记为现有图片
            url: imageUrl
          })
        })
      }
      
      // 保存初始数据，用于检测变更
      originalFormData.value = JSON.parse(JSON.stringify(formData))
      hasChanges.value = false
    }
  } catch (error) {
    console.error('获取详情失败:', error)
    alert('获取详情失败，请稍后重试')
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
      formData.type !== originalFormData.value.type ||
      formData.title !== originalFormData.value.title ||
      formData.category !== originalFormData.value.category ||
      formData.description !== originalFormData.value.description ||
      formData.location !== originalFormData.value.location ||
      formData.time !== originalFormData.value.time ||
      formData.contact_type !== originalFormData.value.contact_type ||
      formData.contact_value !== originalFormData.value.contact_value ||
      formData.hide_contact !== originalFormData.value.hide_contact ||
      imageList.value.some(img => !img.isExisting)
    ) {
      hasChanges.value = true
    } else {
      hasChanges.value = false
    }
  } else if (!isEditMode.value) {
    // 创建模式，检查是否有任何内容
    if (
      formData.title.trim() !== '' ||
      formData.description.trim() !== '' ||
      formData.location.trim() !== '' ||
      formData.contact_value.trim() !== '' ||
      imageList.value.length > 0
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

// 生命周期钩子
onMounted(() => {
  // 获取详情（如果是编辑模式）
  fetchLostItem()
  
  // 监听表单变更
  window.addEventListener('beforeunload', beforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', beforeUnload)
})
</script>

<style scoped>
.lost-item-editor {
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

.radio-buttons {
  display: flex;
  gap: 16px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-text {
  font-size: 14px;
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

.character-count {
  text-align: right;
  font-size: 12px;
  color: #9ca3af;
}

.form-hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.form-section {
  border-top: 1px solid #f1f3f4;
  padding-top: 16px;
  margin-top: 8px;
}

.form-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
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

.images-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.image-preview-item {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
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
  width: 12px;
  height: 12px;
  color: #ef4444;
}

.image-upload-box {
  width: 120px;
  height: 120px;
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.image-upload-box:hover {
  border-color: #667eea;
  background: #f9fafb;
}

.image-upload-box svg {
  width: 24px;
  height: 24px;
  color: #9ca3af;
  margin-bottom: 8px;
}

.image-upload-box span {
  font-size: 12px;
  color: #6b7280;
}

.image-input {
  display: none;
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