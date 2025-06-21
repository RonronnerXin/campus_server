<template>
  <header class="header">
    <div class="header-content">
      <div class="logo-section">
        <div class="logo">
          <svg viewBox="0 0 24 24" fill="none" class="logo-icon">
            <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2"/>
            <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="2"/>
          </svg>
          <div class="logo-text">
            <h1>大学生失物招领&社区交流平台</h1>
            <span>Campus Lost-Found And Community</span>
          </div>
        </div>
      </div>
      
      <div class="search-section">
        <div class="search-container">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none">
            <path d="M21 21L16.514 16.506M19 10.5C19 15.194 15.194 19 10.5 19S2 15.194 2 10.5 5.806 2 10.5 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <input 
            type="text" 
            placeholder="搜索失物、招领信息..."
            v-model="searchQuery"
            class="search-input"
          />
        </div>
      </div>
      
      <nav class="nav-actions">
        <!-- <button class="nav-btn" title="通知">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M12 22C13.1 22 14 21.1 14 20H10C10 21.1 10.9 22 12 22ZM18 16V11C18 7.93 16.36 5.36 13.5 4.68V4C13.5 3.17 12.83 2.5 12 2.5S10.5 3.17 10.5 4V4.68C7.63 5.36 6 7.92 6 11V16L4 18V19H20V18L18 16Z" fill="currentColor"/>
          </svg>
          <span class="notification-badge">3</span>
        </button> -->
        
        <template v-if="appStore.userInfo.loggedIn">
          <div class="user-menu" @click="toggleMenu">
          <img :src="appStore.userInfo.avatar || defaultAvatar" alt="用户头像" class="avatar" />            
          <div class="user-info">
              <span class="username">{{appStore.userInfo.username}}</span>
              <span class="user-role">软件学院</span>
            </div>
            <ul v-show="showMenu" class="user-dropdown">
              <li><router-link to="/profile">个人中心</router-link></li>
              <li @click="showPasswordDialog">修改密码</li>
              <li @click="appStore.logout">注销</li>
            </ul>
          </div>
        </template>
        <template v-else>
          <div class="auth-buttons">
            <router-link to="/login" class="login-btn">登录</router-link>
            <router-link to="/register" class="register-btn">注册</router-link>
          </div>
        </template>
      </nav>
    </div>
  </header>

  <!-- Add the dialog component at the bottom of the template -->
  <el-dialog
    style="border-radius: 30px;"
    v-model="passwordDialogVisible"
    title="重置密码"
    width="600px"
  >
    <div class="password-form">
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="旧密码">
          <el-input v-model="passwordForm.oldPassword" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="passwordForm.confirmPassword" show-password />
        </el-form-item>
      </el-form>
      <div class="dialog-actions">
        <el-button type="primary" @click="submitPassword">确认重置</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAppStore } from '../stores/app';
import { resetPassword } from '../services/userServ';
import { success, error } from '../tools/messageBox';

const appStore = useAppStore();
const searchQuery = ref('');
const showMenu = ref(false);
const passwordDialogVisible = ref(false);
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

const showPasswordDialog = () => {
  passwordDialogVisible.value = true;
};

const submitPassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    error('新密码和确认密码不一致');
    return;
  }
  const res = await resetPassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
  console.log(res)
  if (res.message == '密码修改成功') {
    success(res.message)
    passwordDialogVisible.value = false
  } else {
    error('密码重置失败，请重试')
  }
}
</script>

<style scoped>
.header {
  background: #ffffff;
  border-bottom: 1px solid #f1f3f4;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #667eea;
}

.logo-text h1 {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1;
}

.logo-text span {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 400;
}

.search-section {
  display: flex;
  justify-content: center;
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
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

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: #f9fafb;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-btn svg {
  width: 20px;
  height: 20px;
}

.notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 18px;
  height: 18px;
  background: #ef4444;
  color: #ffffff;
  font-size: 10px;
  font-weight: 600;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 12px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative; /* 添加这行 */
}

.user-menu:hover {
  background: #f3f4f6;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1;
}

.user-role {
  font-size: 12px;
  color: #9ca3af;
  line-height: 1;
}

.auth-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.login-btn {
  padding: 8px 16px;
  color: #667eea;
  font-weight: 500;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.login-btn:hover {
  background: #f3f4f6;
}

.register-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-weight: 500;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.register-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}
.logout-btn {
  margin-left: 12px;
  padding: 4px 8px;
  font-size: 12px;
  color: #ef4444;
  background: transparent;
  border: none;
  cursor: pointer;
}

.logout-btn:hover {
  text-decoration: underline;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 8px 0;
  min-width: 160px;
  list-style: none;
}

.user-dropdown li {
  padding: 8px 16px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-dropdown li:hover {
  background-color: #f3f4f6;
}

.user-dropdown a {
  color: inherit;
  text-decoration: none;
  display: block;
}

.password-form {
  padding: 20px;
}

.dialog-actions {
  margin-top: 20px;
  text-align: right;
}

.el-dialog__header {
  border-bottom: none;
}

.el-dialog__title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.el-dialog__body {
  padding: 0;
}

.el-form-item {
  margin-bottom: 16px;
}

.el-input {
  border-radius: 8px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}

.el-input--suffix {
  margin-right: 8px;
}

.el-button--primary {
  background: #667eea;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.el-button--primary:hover {
  background: #5a67d8;
}

@media (max-width: 768px) {
  .header-content {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .logo-text span {
    display: none;
  }
  
  .search-container {
    max-width: none;
  }
  
  .nav-actions {
    justify-content: center;
  }
}
</style>