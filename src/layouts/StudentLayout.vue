<template>
  <div class="dashboard">
    <div class="sidebar">
      <div class="sidebar-brand">
        <div class="brand-icon">🎓</div>
        <span class="brand-name">学习中心</span>
      </div>

      <div class="user-card">
        <div class="user-avatar">{{ userInitial }}</div>
        <div class="user-meta">
          <div class="user-name">{{ userName }}</div>
          <div class="user-points">💎 {{ userPoints }} 积分</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <!-- 学习资源模块 -->
        <div class="nav-group">
          <div class="nav-group-title">学习资源</div>
          <router-link to="/student/courses">
            <span class="nav-icon">📚</span>资源浏览
          </router-link>
          <router-link to="/student/collections">
            <span class="nav-icon">⭐</span>收藏管理
          </router-link>
        </div>
        
        <!-- 交流互动模块 -->
        <div class="nav-group">
          <div class="nav-group-title">交流互动</div>
          <router-link to="/student/forum">
            <span class="nav-icon">💬</span>论坛
          </router-link>
          <router-link to="/student/announcements">
            <span class="nav-icon">📢</span>公告
          </router-link>
        </div>
        
        <!-- 个人管理模块 -->
        <div class="nav-group">
          <div class="nav-group-title">个人管理</div>
          <router-link to="/student/points">
            <span class="nav-icon">🎁</span>我的积分
          </router-link>
          <router-link to="/student/personal">
            <span class="nav-icon">👤</span>个人中心
          </router-link>
        </div>
      </nav>

      <button @click="handleLogout" class="logout-btn">
        <span>🚪</span> 退出登录
      </button>
    </div>
    <div class="content">
      <router-view />
    </div>
    <AIAssistantFloating />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AIAssistantFloating from '../components/student/AIAssistantFloating.vue'

const router = useRouter()
const user = JSON.parse(localStorage.getItem('user') || '{}')
const userName = computed(() => user.name || user.username || '同学')
const userInitial = computed(() => (user.name || user.username || 'S').charAt(0).toUpperCase())
const userPoints = computed(() => user.points || 0)

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.dashboard { display: flex; min-height: 100vh; }

.sidebar {
  width: 240px;
  background: var(--student-bg);
  color: white;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 22px 20px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.brand-icon { font-size: 24px; }
.brand-name { font-size: 15px; font-weight: 700; letter-spacing: 0.5px; }

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  margin: 12px 12px 8px;
  background: rgba(255,255,255,0.07);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(10px);
}
.user-avatar {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 700; flex-shrink: 0;
}
.user-name { font-size: 14px; font-weight: 600; color: #fff; }
.user-points { font-size: 11px; color: #ffd666; margin-top: 2px; }

.sidebar-nav {
  flex: 1;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  max-height: calc(100vh - 220px);
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-group-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: rgba(255,255,255,0.5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 0 16px 8px;
  margin-top: 8px;
}
.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.65);
  text-decoration: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}
.sidebar-nav a:hover {
  background: rgba(255,255,255,0.08);
  color: #fff;
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
}
.sidebar-nav a.router-link-active {
  background: linear-gradient(135deg, var(--student-primary), var(--primary-light));
  color: white;
  box-shadow: var(--shadow-md);
  transform: translateX(4px);
}
.nav-icon { font-size: 16px; width: 20px; text-align: center; }

.logout-btn {
  margin: 12px;
  padding: 12px 16px;
  background: rgba(245,108,108,0.15);
  color: #f56c6c;
  border: 1px solid rgba(245,108,108,0.25);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}
.logout-btn:hover {
  background: rgba(245,108,108,0.25);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.content { flex: 1; background: #f4f6fb; overflow-y: auto; min-width: 0; }
</style>