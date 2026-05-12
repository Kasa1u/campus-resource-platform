<template>
  <div class="login-page">
    <!-- 左侧：品牌区 -->
    <div class="login-left">
      <div class="brand-content">
        <div class="brand-logo">
          <div class="logo-icon">
            <IconBook />
          </div>
        </div>
        <h1 class="brand-title">校园课程资源平台</h1>
        <p class="brand-slogan">让教学资源真正流动起来</p>
        <p class="brand-subtitle">Campus Resource Sharing</p>
      </div>
      
      <div class="brand-footer">
        <p class="brand-copyright">© 2026 All rights reserved</p>
      </div>
    </div>

    <!-- 右侧：登录区 -->
    <div class="login-right">
      <div class="login-card">
        <div class="card-header">
          <h2 class="card-title">LOGIN</h2>
          <p class="card-subtitle">继续使用校园课程资源平台</p>
        </div>

        <!-- 角色选择 -->
        <div class="role-selector">
          <button
            v-for="(r, i) in roles"
            :key="r.value"
            :class="['role-btn', role === r.value ? 'active' : '']"
            @click="role = r.value; roleIndex = i"
          >
            <component :is="r.icon" class="role-icon" />
            <span>{{ r.label }}</span>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-field">
            <label class="field-label">用户名</label>
            <div class="input-wrapper" :class="{ 'has-error': usernameError }">
              <input
                v-model="username"
                placeholder="请输入用户名"
                required
                autocomplete="username"
                @focus="activeInput = 'username'"
                @blur="activeInput = ''"
                @input="validateUsernameInput"
              />
            </div>
            <transition name="fade">
              <div v-if="usernameError" class="field-error">
                <IconAlertCircle class="error-icon" />
                {{ usernameError }}
              </div>
            </transition>
          </div>

          <div class="form-field">
            <label class="field-label">密码</label>
            <div class="input-wrapper" :class="{ 'has-error': passwordError }">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                placeholder="请输入密码"
                required
                autocomplete="current-password"
                @focus="activeInput = 'password'"
                @blur="activeInput = ''"
              />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                <component :is="showPassword ? IconEye : IconEyeOff" class="toggle-icon" />
              </button>
            </div>
            <transition name="fade">
              <div v-if="passwordError" class="field-error">
                <IconAlertCircle class="error-icon" />
                {{ passwordError }}
              </div>
            </transition>
          </div>

          <div class="form-options">
            <label class="remember-checkbox">
              <input type="checkbox" v-model="rememberMe" />
              <span class="checkmark">
                <IconCheck v-if="rememberMe" class="check-icon" />
              </span>
              <span class="remember-text">记住我</span>
            </label>
            <button type="button" class="forgot-btn" @click="showForgotDialog = true">
              忘记密码？
            </button>
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">登录</span>
            <span v-else>
              <span class="loading-spinner"></span>
              登录中...
            </span>
          </button>
        </form>

        <!-- 快速体验 -->
        <div class="quick-access">
          <div class="quick-access-label">快速体验不同角色</div>
          <div class="quick-access-buttons">
            <button
              v-for="acc in testAccounts"
              :key="acc.role"
              class="quick-btn"
              @click="fillAccount(acc)"
            >
              {{ acc.roleLabel }}体验
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <transition name="fade">
      <div v-if="showForgotDialog" class="dialog-overlay" @click="showForgotDialog = false">
        <div class="dialog-content" @click.stop>
          <div class="dialog-header">
            <h3>修改密码</h3>
            <button class="dialog-close" @click="showForgotDialog = false">
              <IconClose class="close-icon" />
            </button>
          </div>
          <div class="dialog-body">
            <div class="form-field">
              <label class="field-label">用户名</label>
              <div class="input-wrapper" :class="{ 'has-error': forgotForm.usernameError }">
                <input
                  v-model="forgotForm.username"
                  placeholder="请输入用户名"
                  required
                  @input="validateForgotUsername"
                />
              </div>
              <transition name="fade">
                <div v-if="forgotForm.usernameError" class="field-error">
                  <IconAlertCircle class="error-icon" />
                  {{ forgotForm.usernameError }}
                </div>
              </transition>
            </div>
            <div class="form-field">
              <label class="field-label">旧密码</label>
              <div class="input-wrapper">
                <input type="password" v-model="forgotForm.oldPassword" placeholder="请输入旧密码" required />
              </div>
            </div>
            <div class="form-field">
              <label class="field-label">新密码</label>
              <div class="input-wrapper" :class="{ 'has-error': forgotForm.newPasswordError }">
                <input
                  type="password"
                  v-model="forgotForm.newPassword"
                  placeholder="至少 6 位"
                  required
                  @input="validateForgotNewPassword"
                />
              </div>
              <transition name="fade">
                <div v-if="forgotForm.newPasswordError" class="field-error">
                  <IconAlertCircle class="error-icon" />
                  {{ forgotForm.newPasswordError }}
                </div>
              </transition>
              <PasswordStrength v-if="forgotForm.newPassword" :password="forgotForm.newPassword" />
            </div>
            <div class="form-field">
              <label class="field-label">确认新密码</label>
              <div class="input-wrapper" :class="{ 'has-error': forgotForm.confirmPasswordError }">
                <input
                  type="password"
                  v-model="forgotForm.confirmPassword"
                  placeholder="请再次输入新密码"
                  required
                  @input="validateForgotConfirmPassword"
                />
              </div>
              <transition name="fade">
                <div v-if="forgotForm.confirmPasswordError" class="field-error">
                  <IconAlertCircle class="error-icon" />
                  {{ forgotForm.confirmPasswordError }}
                </div>
              </transition>
            </div>
            <button class="submit-btn" @click="handleChangePassword" :disabled="changingPassword">
              <span v-if="!changingPassword">确认修改</span>
              <span v-else>修改中...</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

import { useToast } from '../composables/useToast'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  IconBook,
  IconSettings,
  IconCheck,
  IconUser,
  IconEye,
  IconEyeOff,
  IconAlertCircle,
  IconClose
} from './icons'
import PasswordStrength from './common/PasswordStrength.vue'
import { validateUsername, validatePassword, validatePasswordMatch } from '@/utils/validation'

const toast = useToast()
const router = useRouter()

type RoleType = 'admin' | 'student' | 'teacher'

const role = ref<RoleType>('student')
const roleIndex = ref(0)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const rememberMe = ref(false)
const activeInput = ref('')
const usernameError = ref('')
const passwordError = ref('')

const showForgotDialog = ref(false)
const changingPassword = ref(false)
const forgotForm = ref({
  username: '',
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
  usernameError: '',
  oldPasswordError: '',
  newPasswordError: '',
  confirmPasswordError: ''
})

const validateUsernameInput = () => {
  const result = validateUsername(username.value)
  usernameError.value = result.valid ? '' : (result.message || '')
}

const validateForgotUsername = () => {
  const result = validateUsername(forgotForm.value.username)
  forgotForm.value.usernameError = result.valid ? '' : (result.message || '')
}

const validateForgotNewPassword = () => {
  const result = validatePassword(forgotForm.value.newPassword)
  forgotForm.value.newPasswordError = result.valid ? '' : (result.message || '')
}

const validateForgotConfirmPassword = () => {
  const result = validatePasswordMatch(forgotForm.value.newPassword, forgotForm.value.confirmPassword)
  forgotForm.value.confirmPasswordError = result.valid ? '' : (result.message || '')
}

onMounted(() => {
  const savedUsername = localStorage.getItem('remember_username')
  const savedRole = localStorage.getItem('remember_role') as RoleType
  if (savedUsername) {
    username.value = savedUsername
    rememberMe.value = true
    if (savedRole) {
      role.value = savedRole
      roleIndex.value = roles.findIndex(r => r.value === savedRole)
    }
  }
})

const roles = [
  { value: 'student' as RoleType, label: '学生', icon: IconUser },
  { value: 'teacher' as RoleType, label: '教师', icon: IconBook },
  { value: 'admin' as RoleType, label: '管理员', icon: IconSettings }
]

const testAccounts = [
  { role: 'admin' as RoleType, roleLabel: '管理员', username: 'admin', password: 'admin123' },
  { role: 'student' as RoleType, roleLabel: '学生', username: 's1', password: 's123' },
  { role: 'teacher' as RoleType, roleLabel: '教师', username: 't1', password: 't123' }
]

const fillAccount = (acc: any) => {
  username.value = acc.username
  password.value = acc.password
  role.value = acc.role
  roleIndex.value = roles.findIndex(r => r.value === acc.role)
  // 清除验证错误
  usernameError.value = ''
  passwordError.value = ''
}

const handleSubmit = async () => {
  loading.value = true
  console.log('登录参数:', {
    username: username.value,
    password: password.value,
    role: role.value
  })
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: username.value,
      password: password.value,
      role: role.value
    })
    console.log('登录响应:', res.data)
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('user', JSON.stringify(res.data.user))

    if (rememberMe.value) {
      localStorage.setItem('remember_username', username.value)
      localStorage.setItem('remember_role', role.value)
    } else {
      localStorage.removeItem('remember_username')
      localStorage.removeItem('remember_role')
    }

    const r = res.data.user.role
    console.log('跳转到:', r)
    if (r === 'admin') router.push('/admin')
    else if (r === 'teacher') router.push('/teacher/courses')
    else router.push('/student')
  } catch (error: any) {
    console.error('登录错误:', error)
    const data = error.response?.data
    const msg = data?.non_field_errors?.[0] || data?.detail || data?.username?.[0] || data?.password?.[0] || '登录失败，请检查用户名和密码'
    alert(msg)
  } finally {
    loading.value = false
  }
}

const handleChangePassword = async () => {
  if (!forgotForm.value.username || !forgotForm.value.oldPassword || !forgotForm.value.newPassword) {
    toast.warning('请填写所有必填项')
    return
  }
  if (forgotForm.value.newPassword.length < 6) {
    toast.info('新密码至少需要6位')
    return
  }
  if (forgotForm.value.newPassword !== forgotForm.value.confirmPassword) {
    toast.info('两次输入的新密码不一致')
    return
  }

  changingPassword.value = true
  try {
    const loginRes = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: forgotForm.value.username,
      password: forgotForm.value.oldPassword
    })
    const token = loginRes.data.access
    await axios.post('http://127.0.0.1:8000/api/auth/change-password/', {
      old_password: forgotForm.value.oldPassword,
      new_password: forgotForm.value.newPassword
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('密码修改成功！请使用新密码登录')
    showForgotDialog.value = false
    forgotForm.value = { username: '', oldPassword: '', newPassword: '', confirmPassword: '', usernameError: '', oldPasswordError: '', newPasswordError: '', confirmPasswordError: '' }
  } catch (error: any) {
    const msg = error.response?.data?.error || error.response?.data?.detail || '修改失败，请检查用户名和密码是否正确'
    alert(msg)
  } finally {
    changingPassword.value = false
  }
}
</script>

<style scoped>
/* 基础布局 */
.login-page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #fafbfc 0%, #ffffff 100%);
}

/* 左侧品牌区 */
.login-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 64px;
  position: relative;
  background: 
    radial-gradient(circle at 20% 20%, rgba(13, 148, 136, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(13, 148, 136, 0.02) 0%, transparent 50%),
    linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-right: 1px solid rgba(15, 23, 42, 0.04);
}

/* 超弱网格纹理 */
.login-left::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(to right, rgba(15, 23, 42, 0.02) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(15, 23, 42, 0.02) 1px, transparent 1px);
  background-size: 48px 48px;
  opacity: 0.8;
  pointer-events: none;
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.brand-logo {
  margin-bottom: 32px;
}

.logo-icon {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 8px 24px rgba(13, 148, 136, 0.15);
}

.logo-icon svg {
  width: 36px;
  height: 36px;
  color: white;
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 16px 0;
  letter-spacing: -0.03em;
}

.brand-slogan {
  font-size: 16px;
  color: #475569;
  margin: 0 0 8px 0;
  font-weight: 400;
  letter-spacing: -0.01em;
}

.brand-subtitle {
  font-size: 13px;
  color: #94a3b8;
  margin: 0;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.brand-footer {
  position: relative;
  z-index: 1;
  text-align: center;
}

.brand-copyright {
  font-size: 12px;
  color: #cbd5e1;
  margin: 0;
}

/* 右侧登录区 */
.login-right {
  width: 540px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 64px 48px;
  background: #ffffff;
}

/* 登录卡片 - 高级细节 */
.login-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 
    0 1px 1px rgba(15, 23, 42, 0.02),
    0 8px 24px rgba(15, 23, 42, 0.04),
    0 24px 60px rgba(15, 23, 42, 0.04);
  padding: 48px;
  position: relative;
}

.card-header {
  margin-bottom: 36px;
}

.card-title {
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  letter-spacing: -0.03em;
}

.card-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  font-weight: 400;
}

/* 角色选择 */
.role-selector {
  display: flex;
  gap: 8px;
  margin-bottom: 36px;
  padding: 6px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}

.role-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px 14px;
  border: none;
  background: transparent;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.role-btn:hover {
  color: #475569;
  background: rgba(15, 23, 42, 0.02);
}

.role-btn.active {
  background: #ffffff;
  color: #0d9488;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 0 0 1px rgba(15, 23, 42, 0.03);
}

.role-icon {
  width: 14px;
  height: 14px;
}

/* 表单 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 13px;
  font-weight: 500;
  color: #334155;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 16px;
  font-size: 14px;
  color: #0f172a;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  outline: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-wrapper input::placeholder {
  color: #94a3b8;
}

.input-wrapper input:focus {
  background: #ffffff;
  border-color: #0d9488;
  box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.08);
}

.input-wrapper.has-error input {
  border-color: #ef4444;
  background: #fef2f2;
}

.input-wrapper.has-error input:focus {
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.08);
}

.password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  transition: all 0.15s ease;
  border-radius: 8px;
}

.password-toggle:hover {
  color: #64748b;
  background: rgba(15, 23, 42, 0.03);
}

.toggle-icon {
  width: 16px;
  height: 16px;
}

.field-error {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #ef4444;
}

.error-icon {
  width: 13px;
  height: 13px;
  flex-shrink: 0;
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -4px;
}

.remember-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #64748b;
}

.remember-checkbox input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 1.5px solid #cbd5e1;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.remember-checkbox input:checked + .checkmark {
  background: #0d9488;
  border-color: #0d9488;
}

.check-icon {
  width: 11px;
  height: 11px;
  color: white;
}

.remember-text {
  user-select: none;
}

.forgot-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13px;
  color: #0d9488;
  transition: color 0.15s ease;
}

.forgot-btn:hover {
  color: #0f766e;
}

/* 提交按钮 - 高级渐变和交互 */
.submit-btn {
  width: 100%;
  padding: 14px 20px;
  background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 1px 1px rgba(15, 23, 42, 0.03), 0 4px 12px rgba(13, 148, 136, 0.15);
  position: relative;
  overflow: hidden;
}

/* 微高光效果 */
.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.12), transparent);
  pointer-events: none;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #0f766e 0%, #0b5f59 100%);
  transform: translateY(-1px);
  box-shadow: 0 1px 1px rgba(15, 23, 42, 0.03), 0 6px 20px rgba(13, 148, 136, 0.2);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 1px 1px rgba(15, 23, 42, 0.03), 0 2px 8px rgba(13, 148, 136, 0.15);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 1px 1px rgba(15, 23, 42, 0.03);
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 快速体验 */
.quick-access {
  margin-top: 36px;
  padding-top: 28px;
  border-top: 1px solid #f1f5f9;
}

.quick-access-label {
  font-size: 12px;
  color: #94a3b8;
  text-align: center;
  margin-bottom: 14px;
  font-weight: 400;
}

.quick-access-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.quick-btn {
  padding: 10px 18px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  transition: all 0.15s ease;
}

.quick-btn:hover {
  background: #f1f5f9;
  color: #475569;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

/* 弹窗 */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: #ffffff;
  border-radius: 20px;
  width: 90%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 
    0 1px 1px rgba(15, 23, 42, 0.02),
    0 24px 60px rgba(15, 23, 42, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-bottom: 1px solid #f1f5f9;
}

.dialog-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
}

.dialog-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  transition: all 0.15s ease;
  border-radius: 8px;
}

.dialog-close:hover {
  color: #64748b;
  background: rgba(15, 23, 42, 0.03);
}

.close-icon {
  width: 18px;
  height: 18px;
}

.dialog-body {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式 */
@media (max-width: 1024px) {
  .login-left {
    display: none;
  }
  .login-right {
    width: 100%;
    padding: 40px 24px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
    border-radius: 20px;
  }
  .quick-access-buttons {
    flex-direction: column;
  }
  .quick-btn {
    width: 100%;
  }
}
</style>
