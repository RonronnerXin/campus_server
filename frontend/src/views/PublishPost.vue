<template>
  <div class="publish-container">
    <div class="page-header">
      <h1>发布博客</h1>
    </div>
    <form class="publish-form" @submit.prevent="submitForm">
      <!-- 基本信息 -->
      <div class="form-section">
        <h2 class="section-title">基本信息</h2>
        <div class="form-group">
          <label for="title">标题</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title" 
            placeholder="请输入博客标题" 
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="category">博客分类</label>
          <select id="category" v-model="formData.category" class="form-select">
            <option value="">请选择分类</option>
            <option value="tech">技术</option>
            <option value="life">生活</option>
            <option value="study">学习</option>
            <option value="travel">旅行</option>
            <option value="other">其他</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="tags">标签</label>
          <div class="tags-input-container">
            <div class="tags-list" v-if="formData.tags.length > 0">
              <div v-for="(tag, index) in formData.tags" :key="index" class="tag-item">
                {{ tag }}
                <button type="button" class="remove-tag" @click="removeTag(index)">×</button>
              </div>
            </div>
            <input 
              type="text" 
              id="tags" 
              v-model="tagInput" 
              @keydown.enter.prevent="addTag"
              placeholder="输入标签后按回车添加" 
              class="tags-input"
            />
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
      
      <!-- 博客内容 -->
      <div class="form-section">
        <h2 class="section-title">博客内容</h2>
        <div class="form-group">
          <label for="summary">摘要</label>
          <textarea 
            id="summary" 
            v-model="formData.summary" 
            placeholder="请输入博客摘要，将显示在博客列表中"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="content">正文内容</label>
          <div class="editor-toolbar">
            <button type="button" class="toolbar-btn" @click="formatText('bold')">B</button>
            <button type="button" class="toolbar-btn" @click="formatText('italic')"><i>I</i></button>
            <button type="button" class="toolbar-btn" @click="formatText('heading')">H</button>
            <button type="button" class="toolbar-btn" @click="formatText('list')">•</button>
            <button type="button" class="toolbar-btn" @click="formatText('link')">🔗</button>
            <button type="button" class="toolbar-btn" @click="formatText('image')">🖼️</button>
          </div>
          <textarea 
            id="content" 
            v-model="formData.content" 
            placeholder="请输入博客正文内容"
            class="content-textarea"
            rows="15"
          ></textarea>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="form-actions">
        <button type="button" class="cancel-btn" @click="goBack">取消</button>
        <button type="submit" class="submit-btn">{{ formData.draft ? '保存草稿' : '发布博客' }}</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createBlogPost } from '../services/blogPostServ' 

const router = useRouter()
const coverInput = ref(null)
const coverDragover = ref(false)
const tagInput = ref('')
const submitting = ref(false);

const formData = reactive({
  title: '',
  category: '',
  tags: [],
  images: [],
  summary: '',
  content: '',
  allowComments: true,
  featured: false,
  draft: false
})

// 标签相关
const addTag = () => {
  const tag = tagInput.value.trim()
  if (tag && !formData.tags.includes(tag)) {
    if (formData.tags.length >= 5) {
      alert('最多添加5个标签')
      return
    }
    formData.tags.push(tag)
    tagInput.value = ''
  }
}

const removeTag = (index) => {
  formData.tags.splice(index, 1)
}

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click();
};

// 处理文件变化
const onFileChange = (event) => {
  const files = Array.from(event.target.files);
  handleFiles(files);
};

// 处理拖拽
const onDrop = (event) => {
  dragover.value = false;
  const files = Array.from(event.dataTransfer.files);
  handleFiles(files);
};

// 处理文件
const handleFiles = (files) => {
  // 检查文件数量
  if (formData.images.length + files.length > 3) {
    alert('最多只能上传3张图片');
    return;
  }

  files.forEach(file => {
    // 检查文件类型
    if (!file.type.startsWith('image/')) {
      alert('只能上传图片文件');
      return;
    }

    // 检查文件大小（2MB = 2 * 1024 * 1024 bytes）
    if (file.size > 2 * 1024 * 1024) {
      alert('图片大小不能超过2MB');
      return;
    }

    // 创建预览URL
    const url = URL.createObjectURL(file);
    formData.images.push({
      file,
      url
    });
  });
};

// 移除图片
const removeImage = (index) => {
  URL.revokeObjectURL(formData.images[index].url); // 释放URL
  formData.images.splice(index, 1);
};

// 编辑器工具栏
const formatText = (format) => {
  // 简单实现，实际项目中可能需要更复杂的富文本编辑器
  const textarea = document.getElementById('content')
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = formData.content.substring(start, end)
  
  let formattedText = ''
  
  switch (format) {
    case 'bold':
      formattedText = `**${selectedText}**`
      break
    case 'italic':
      formattedText = `*${selectedText}*`
      break
    case 'heading':
      formattedText = `## ${selectedText}`
      break
    case 'list':
      formattedText = `- ${selectedText}`
      break
    case 'link':
      formattedText = `[${selectedText}](链接地址)`
      break
    case 'image':
      formattedText = `![${selectedText || '图片描述'}](图片链接)`
      break
  }
  
  formData.content = formData.content.substring(0, start) + formattedText + formData.content.substring(end)
}

// 表单提交与预览
const submitForm = async () => {
  // 表单验证
  if (!formData.title) {
    alert('请输入博客标题')
    return
  }
  
  if (!formData.category) {
    alert('请选择博客分类')
    return
  }
  
  if (!formData.content) {
    alert('请输入博客内容')
    return
  }
  // 构建提交数据
  const submitData = {
    title: formData.title,
    category: formData.category,
    tags: formData.tags,
    summary: formData.summary,
    content: formData.content,
    allowComments: formData.allowComments,
    featured: formData.featured,
    draft: formData.draft
  }

  // 准备图片文件
  const imageFiles = formData.images.map(img => img.file);
  
  
  submitting.value = true;
  // 提交表单
  console.log('提交博客数据:', formData)
  try {
    console.log(submitData, imageFiles);
    const result = await createBlogPost(submitData, imageFiles);
    console.log('提交结果:', result);
    if (result) {
      alert('发布成功！');
      router.push('/');
    }
  } catch (error) {
    console.error('提交表单出错:', error);
    alert('发布失败，请稍后再试');
  } finally {
    submitting.value = false;
  }
}


const goBack = () => {
  router.back()
}
</script>

<style scoped>
.publish-container {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #f1f3f4;
  padding: 40px 0 40px 0;
  max-width: 900px;
  width: 100%;
  margin: 40px auto;
  box-shadow: 0 8px 32px rgba(60,100,180,0.04);
}

.page-header { 
  margin-bottom: 32px; 
  text-align: left;
  padding: 0 40px;
}

.page-header h1 { 
  font-size: 28px; 
  font-weight: 700; 
  color: #1a1a1a;
}

.publish-form {
  width: 95%;
  margin: 0 auto;
}

.form-section { 
  margin-bottom: 36px; 
}

.section-title {
  font-size: 18px; 
  font-weight: 600; 
  color: #333; 
  margin-bottom: 16px; 
  padding-bottom: 8px; 
  border-bottom: 1px solid #f1f3f4;
}

.form-group { 
  margin-bottom: 24px; 
}

.form-group label { 
  display: block; 
  margin-bottom: 8px; 
  font-size: 15px; 
  font-weight: 500; 
  color: #444;
}

.form-input, .form-select, .form-textarea, .tags-input {
  width: 100%; 
  padding: 14px 18px; 
  border: 1px solid #e5e7eb; 
  border-radius: 10px; 
  font-size: 16px; 
  background: #f9fafb;
  transition: all .18s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus, .tags-input:focus {
  border-color: #667eea; 
  background: #fff; 
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.07);
  outline: none;
}

.form-textarea {
  resize: vertical; 
  min-height: 100px;
}

.content-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 0 0 10px 10px;
  font-size: 16px;
  min-height: 300px;
  background: #f9fafb;
  transition: all .18s;
  resize: vertical;
  line-height: 1.6;
}

.content-textarea:focus {
  border-color: #667eea;
  background: #fff;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.07);
  outline: none;
}

/* 标签相关样式 */
.tags-input-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f3f4f6;
  border-radius: 16px;
  font-size: 14px;
  color: #4b5563;
}

.remove-tag {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0;
  margin-left: 4px;
}

.remove-tag:hover {
  color: #ef4444;
}

/* 封面图片上传样式 */
.upload-box {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  background: #f9fafb;
  cursor: pointer;
  padding: 24px;
  transition: all 0.2s;
  user-select: none;
}

.upload-box:hover, .upload-box.dragover {
  border-color: #667eea;
  background: rgba(102,126,234,0.06);
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  width: 48px;
  height: 48px;
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

.cover-preview {
  position: relative;
  width: 100%;
  height: 100%;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.remove-cover {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(0,0,0,0.5);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
}

.remove-cover svg {
  width: 18px;
  height: 18px;
}

/* 编辑器工具栏 */
.editor-toolbar {
  display: flex;
  gap: 8px;
  padding: 10px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 10px 10px 0 0;
  border-bottom: none;
}

.toolbar-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

/* 发布设置 */
.publish-options {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 15px;
  color: #4b5563;
}

.checkbox-label input {
  accent-color: #667eea;
  width: 16px;
  height: 16px;
}

/* 操作按钮 */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 40px;
}

.cancel-btn {
  padding: 12px 24px;
  background: #f9fafb;
  color: #4b5563;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #f3f4f6;
}

.preview-btn {
  padding: 12px 24px;
  background: #fff;
  color: #667eea;
  border: 1px solid #667eea;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.preview-btn:hover {
  background: rgba(102, 126, 234, 0.05);
}

.submit-btn {
  padding: 12px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* 响应式样式 */
@media (max-width: 900px) {
  .publish-container {
    max-width: 95vw;
    margin: 20px auto;
  }
  
  .page-header {
    padding: 0 20px;
  }
}

@media (max-width: 600px) {
  .publish-container {
    padding: 20px 0;
    border-radius: 0;
    border: none;
    box-shadow: none;
    max-width: 100%;
    margin: 0;
  }
  
  .page-header {
    padding: 0 16px;
  }
  
  .publish-form {
    width: 92%;
  }
  
  .publish-options {
    flex-direction: column;
    gap: 16px;
  }
  
  .form-actions {
    flex-direction: column-reverse;
    gap: 12px;
  }
  
  .cancel-btn,
  .preview-btn,
  .submit-btn {
    width: 100%;
  }
}
</style>