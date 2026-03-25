<template>
  <div class="page-container">
    <div class="page-header">
      <button @click="goBack" class="btn-back">← 返回数据分析</button>
      <h2>用户总览</h2>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-value">{{ totalUsers }}</div>
        <div class="summary-label">总用户数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ teacherCount }}</div>
        <div class="summary-label">老师</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ studentCount }}</div>
        <div class="summary-label">学生</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ adminCount }}</div>
        <div class="summary-label">管理员</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ maleCount }}</div>
        <div class="summary-label">男性</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ femaleCount }}</div>
        <div class="summary-label">女性</div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="user-section">
      <h3>用户列表</h3>
      <div class="filter-bar">
        <input v-model="searchText" placeholder="搜索用户名..." class="search-input" />
        <select v-model="filterRole" class="filter-select">
          <option value="">全部角色</option>
          <option value="admin">管理员</option>
          <option value="teacher">老师</option>
          <option value="student">学生</option>
        </select>
      </div>
      
      <div class="user-list">
        <div v-for="user in filteredUsers" :key="user.id" class="user-card">
          <div class="user-avatar">{{ user.name.charAt(0) }}</div>
          <div class="user-info">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-username">@{{ user.username }}</div>
            <div class="user-meta">
              <span class="role-tag" :class="user.role">{{ getRoleText(user.role) }}</span>
              <span v-if="user.gender">⚧ {{ user.gender }}</span>
              <span v-if="user.major">📚 {{ user.major }}</span>
              <span v-if="user.grade">🎓 {{ user.grade }}级</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const users = ref<any[]>([])
const searchText = ref('')
const filterRole = ref('')

const totalUsers = computed(() => users.value.length)
const teacherCount = computed(() => users.value.filter(u => u.role === 'teacher').length)
const studentCount = computed(() => users.value.filter(u => u.role === 'student').length)
const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const maleCount = computed(() => users.value.filter(u => u.gender === '男' || u.gender === 'male').length)
const femaleCount = computed(() => users.value.filter(u => u.gender === '女' || u.gender === 'female').length)

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchSearch = searchText.value === '' || 
                       user.name.includes(searchText.value) ||
                       user.username.includes(searchText.value)
    const matchRole = filterRole.value === '' || user.role === filterRole.value
    return matchSearch && matchRole
  })
})

const getRoleText = (role: string) => {
  const map: any = { admin: '管理员', teacher: '老师', student: '学生' }
  return map[role] || role
}

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    // 尝试使用 users API，如果不存在则使用 students + teachers
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/auth/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const students = response.data
      
      const response2 = await axios.get('http://127.0.0.1:8000/api/auth/teachers/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const teachers = response2.data
      
      const response3 = await axios.get('http://127.0.0.1:8000/api/auth/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const admins = [response3.data].filter(u => u.role === 'admin')
      
      users.value = [...students, ...teachers, ...admins]
    } catch (e) {
      // 如果 API 不存在，使用备用方案
      const response = await axios.get('http://127.0.0.1:8000/api/stats/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (response.data.success) {
        // 从统计数据中获取用户分布
        userDistribution.value = response.data.userDistribution
      }
      users.value = []
    }
  } catch (error) {
    console.error('获取用户列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.page-container { padding: 20px; }

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.btn-back {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-back:hover {
  background: #e0e0e0;
}

.page-header h2 {
  margin: 0;
  color: #333;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.summary-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.summary-label {
  font-size: 14px;
  color: #666;
}

.user-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.filter-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input, .filter-select {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-input {
  flex: 1;
}

.filter-select {
  min-width: 150px;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.user-username {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.user-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #666;
}

.role-tag {
  padding: 3px 10px;
  background: #f0f0f0;
  border-radius: 12px;
  font-size: 12px;
}

.role-tag.admin {
  background: #fde2e2;
  color: #f56c6c;
}

.role-tag.teacher {
  background: #e6f7ff;
  color: #1890ff;
}

.role-tag.student {
  background: #f6ffed;
  color: #52c41a;
}
</style>
