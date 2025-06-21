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
          <div>
          <div class="form-group">
              <label for="location">定位选择</label>
            <input placeholder="请在地图中选择地点" class="form-input" id="suggestId" type="text" size="30" style="width:300px" />
          </div>
          <!-- <div class="lng-lat">
            <div class="item">
              当前经度:
              <input v-model="lng" />
            </div>
            <div class="item">
              当前纬度:
              <input v-model="lat" />
            </div>
          </div> -->
          <!-- <div id="searchResultPanel"></div> -->
          <div id="container" style="width: 600px; height: 400px;"></div>
        </div>
        
        <div class="form-group">
          <label for="time">时间</label>
          <input 
            type="datetime-local" 
            id="time" 
            v-model="formData.time" 
            placeholder="请选择丢失/拾获时间"
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
import { ref, reactive, onBeforeUnmount, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createLostItem } from '../services/lostItemServ';

const router = useRouter();
const fileInput = ref(null);
const dragover = ref(false);
const submitting = ref(false);
const map = ref(null)
const myValue = ref('')
const lng = ref('')
const lat = ref('')

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
  images: [],
  lng: '',
  lat: ''
});

// 处理表单提交
const submitForm = async () => {
  // 表单验证
  if (!formData.title) {
    alert('请输入标题');
    return;
  }
  
  if (!formData.category) {
    alert('请选择物品分类');
    return;
  }
  
  if (!formData.description) {
    alert('请输入详细描述');
    return;
  }
  
  if (!formData.location) {
    alert('请输入地点');
    return;
  }
  
  if (!formData.time) {
    alert('请选择时间');
    return;
  }
  
  if (!formData.hideContact && !formData.contactValue) {
    alert('请输入联系方式或选择仅通过站内消息联系');
    return;
  }
  
  // 准备提交数据
  const submitData = {
    type: formData.type,
    title: formData.title,
    category: formData.category,
    description: formData.description,
    location: formData.location,
    time: formData.time,
    contact_type: formData.contactType,
    contact_value: formData.contactValue,
    hide_contact: formData.hideContact,
    lat:lat.value,
    lng:lng.value
  };
  
  // 准备图片文件
  const imageFiles = formData.images.map(img => img.file);
  
  submitting.value = true;
  
  try {
    const result = await createLostItem(submitData, imageFiles);
    
    if (result) {
      alert('发布成功！');
      router.push('/lost-found');
    }
  } catch (error) {
    console.error('提交表单出错:', error);
    alert('发布失败，请稍后再试');
  } finally {
    submitting.value = false;
  }
};

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

// 组件卸载时清理
onBeforeUnmount(() => {
  formData.images.forEach(image => {
    URL.revokeObjectURL(image.url);
  });
});

const loadBaiduMap = (callback) => {
  if (typeof BMap !== "undefined") {
    callback()
    return
  }

  const script = document.createElement("script")
  script.type = "text/javascript"
  script.src = "http://api.map.baidu.com/api?v=2.0&ak=mK5CDIAi1mk8Le8z3RCTto1KLzGCG0hQ&callback=initBMap&address=济南"
  document.head.appendChild(script)

  window.initBMap = () => {
    callback()
  }
}

const initMap = () => {
  map.value = new BMap.Map("container")
  const centerPoint = new BMap.Point(116.3964, 39.9093)
  map.value.centerAndZoom(centerPoint, 13)
  map.value.enableScrollWheelZoom()

  const ac = new BMap.Autocomplete({
    input: "suggestId",
    location: map.value,
  })

  ac.addEventListener("onconfirm", (e) => {
    const _value = e.item.value
    myValue.value = _value.province + _value.city + _value.district + _value.street + _value.business
    setPlace()
  })
  map.value.addEventListener("click", (e) => {
    lng.value = e.point.lng.toFixed(6)
    lat.value = e.point.lat.toFixed(6)
    addMarker(new BMap.Point(e.point.lng, e.point.lat))
  })
}

const setPlace = () => {
  const myGeo = new BMap.Geocoder()
  myGeo.getPoint(myValue.value, (point) => {
    if (point) {
      map.value.centerAndZoom(point, 16)
      addMarker(point)
    }
  }, "北京")
}

const addMarker = (point) => {
  clearMarkers()
  const marker = new BMap.Marker(point)
  map.value.addOverlay(marker)
}

const clearMarkers = () => {
  const allOverlay = map.value.getOverlays()
  for (let i = 0; i < allOverlay.length - 1; i++) {
    map.value.removeOverlay(allOverlay[i])
  }
}

onMounted(() => {
  loadBaiduMap(() => {
    initMap()
  })
})

</script>

<style scoped>
.publish-container {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f3f4;
  padding: 24px;
  max-width: 800px;  /* 与PostList同宽 */
  margin: 0 auto;
}

.publish-form {
  width: 100%;
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

.lng-lat {
  margin: 0 0 30px 0px;
}
.lng-lat .item {
  margin: 10px;
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