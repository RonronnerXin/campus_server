<template>
  <div class="publish-container">
    <div class="page-header">
      <h1>发布信息</h1>
    </div>
    
    <div class="publish-form">
      <div class="form-section">
        <h2 class="section-title">基本信息</h2>
        
        <div class="form-group">
          <label for="type">信息类型</label>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" name="type" value="lost" v-model="formData.type" />
              <span class="radio-text">寻物启事</span>
            </label>
            <label class="radio-label">
              <input type="radio" name="type" value="found" v-model="formData.type" />
              <span class="radio-text">招领启事</span>
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="title">标题</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title" 
            placeholder="请输入简短的标题描述"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="category">物品分类</label>
          <select id="category" v-model="formData.category" class="form-select">
            <option value="">请选择分类</option>
            <option value="card">校园卡</option>
            <option value="electronics">电子设备</option>
            <option value="books">书籍资料</option>
            <option value="clothing">衣物</option>
            <option value="other">其他</option>
          </select>
        </div>
      </div>
      
      <div class="form-section">
        <h2 class="section-title">详细信息</h2>
        
        <div class="form-group">
          <label for="description">详细描述</label>
          <textarea 
            id="description" 
            v-model="formData.description" 
            placeholder="请详细描述物品特征、丢失/拾获经过等信息"
            class="form-textarea"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="location">地点</label>
          <input 
            type="text" 
            id="location" 
            v-model="formData.location" 
            placeholder="请输入丢失/拾获地点"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="time">时间</label>
          <input 
            type="datetime-local" 
            id="time" 
            v-model="formData.time" 
            class="form-input"
          />
        </div>
      </div>
      
      <div class="form-section">
        <h2 class="section-title">联系方式</h2>
        
        <div class="form-group">
          <label for="contact">联系方式</label>
          <div class="contact-inputs">
            <div class="contact-input-group">
              <select v-model="formData.contactType" class="contact-type-select">
                <option value="phone">手机号</option>
                <option value="wechat">微信</option>
                <option value="qq">QQ</option>
              </select>
              <input 
                type="text" 
                v-model="formData.contactValue" 
                placeholder="请输入联系方式"
                class="contact-value-input"
              />
            </div>
            <div class="contact-privacy">
              <label class="checkbox-label">
                <input type="checkbox" v-model="formData.hideContact" />
                <span>仅通过站内消息联系我</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <div class="form-section">
        <h2 class="section-title">上传图片</h2>
        
        <div class="image-upload">
          <div 
            class="upload-box"
            @click="triggerFileInput"
            @dragover.prevent="dragover = true"
            @dragleave.prevent="dragover = false"
            @drop.prevent="onDrop"
            :class="{ 'dragover': dragover }"
          >
            <input 
              type="file" 
              ref="fileInput" 
              @change="onFileChange" 
              accept="image/*" 
              multiple 
              class="file-input"
            />
            <svg viewBox="0 0 24 24" fill="none" class="upload-icon">
              <path d="M7 16.5V17.5C7 19.9853 9.01472 22 11.5 22H12.5C14.9853 22 17 19.9853 17 17.5V16.5M12 2V14M12 2L7 7M12 2L17 7" stroke="currentColor" stroke-width="2"/>
            </svg>
            <p class="upload-text">点击或拖拽上传图片</p>
            <p class="upload-hint">最多上传3张，每张不超过2MB</p>
          </div>
          
          <div class="image-preview" v-if="formData.images.length > 0">
            <div v-for="(image, index) in formData.images" :key="index" class="preview-item">
              <img :src="image.url" :alt="`预览图${index + 1}`" class="preview-image" />
              <button class="remove-image" @click="removeImage(index)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M6 18L18 6M6 6L18 18" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="form-actions">
        <button class="cancel-btn" @click="goBack">取消</button>
        <button class="submit-btn" @click="submitForm">发布信息</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInput = ref(null)
const dragover = ref(false)

const formData = reactive({
  type: 'lost',
  title: '',
  category: '',
  description: '',
  location: '',
  time: '',
  contactType: 'phone',
  contactValue: '',
  hideContact: false,
  images: []
})

const triggerFileInput = () => {
  fileInput.value.click()
}

const onFileChange = (event) => {
  const files = event.target.files
  if (!files.length) return
  
  processFiles(files)
}

const onDrop = (event) => {
  dragover.value = false
  const files = event.dataTransfer.files
  if (!files.length) return
  
  processFiles(files)
}

const processFiles = (files) => {
  // 限制最多上传3张图片
  const remainingSlots = 3 - formData.images.length
  if (remainingSlots <= 0) {
    alert('最多只能上传3张图片')
    return
  }
  
  const filesToProcess = Array.from(files).slice(0, remainingSlots)
  
  filesToProcess.forEach(file => {
    // 检查文件类型
    if (!file.type.startsWith('image/')) {
      alert('请上传图片文件')
      return
    }
    
    // 检查文件大小
    if (file.size > 2 * 1024 * 1024) {
      alert('图片大小不能超过2MB')
      return
    }
    
    const reader = new FileReader()
    reader.onload = (e) => {
      formData.images.push({
        file: file,
        url: e.target.result
      })
    }
    reader.readAsDataURL(file)
  })
}

const removeImage = (index) => {
  formData.images.splice(index, 1)
}

const submitForm = () => {
  // 表单验证
  if (!formData.title) {
    alert('请输入标题')
    return
  }
  
  if (!formData.category) {
    alert('请选择物品分类')
    return
  }
  
  if (!formData.description) {
    alert('请输入详细描述')
    return
  }
  
  if (!formData.location) {
    alert('请输入地点')
    return
  }
  
  if (!formData.time) {
    alert('请选择时间')
    return
  }
  
  if (!formData.hideContact && !formData.contactValue) {
    alert('请输入联系方式或选择仅通过站内消息联系')
    return
  }
  
  // 提交表单
  console.log('提交表单数据:', formData)
  
  // 模拟提交成功
  alert('发布成功！')
  router.push('/lost-found')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.publish-container {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f3f4;
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
}

.form-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f1f3f4;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  background: #f9fafb;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.radio-group {
  display: flex;
  gap: 16px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-label input {
  accent-color: #667eea;
  width: 16px;
  height: 16px;
}

.radio-text {
  font-size: 14px;
  color: #4b5563;
}

.contact-inputs {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.contact-input-group {
  display: flex;
  gap: 12px;
}

.contact-type-select {
  width: 100px;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  background: #f9fafb;
}

.contact-value-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  background: #f9fafb;
}

.contact-privacy {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #4b5563;
}

.checkbox-label input {
  accent-color: #667eea;
  width: 16px;
  height: 16px;
}

.image-upload {
  margin-bottom: 20px;
}

.upload-box {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 160px;
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  background: #f9fafb;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-box:hover,
.upload-box.dragover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-icon {
  width: 40px;
  height: 40px;
  color: #9ca3af;
  margin-bottom: 12px;
}

.upload-text {
  font-size: 16px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 4px;
}

.upload-hint {
  font-size: 12px;
  color: #9ca3af;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}

.preview-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  cursor: pointer;
}

.remove-image svg {
  width: 16px;
  height: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
}

.cancel-btn {
  padding: 12px 24px;
  background: #f9fafb;
  color: #4b5563;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: #f3f4f6;
}

.submit-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .contact-input-group {
    flex-direction: column;
    gap: 8px;
  }
  
  .contact-type-select {
    width: 100%;
  }
  
  .form-actions {
    flex-direction: column-reverse;
    gap: 12px;
  }
  
  .cancel-btn,
  .submit-btn {
    width: 100%;
  }
}
</style>