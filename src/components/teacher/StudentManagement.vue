<template>
  <div class="page-container">
    <h2>学生管理</h2>
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">{{ students.length }}</div>
        <div class="stat-label">我的学生</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ getMajorCount }}</div>
        <div class="stat-label">专业分布</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ getGradeCount }}</div>
        <div class="stat-label">年级分布</div>
      </div>
    </div>

    <div class="filter-bar">
      <input 
        v-model="searchText" 
        placeholder="搜索学生姓名或学号..." 
        class="search-input"
      />
      <select v-model="filterMajor" class="filter-select">
        <option value="">所有专业</option>
        <option v-for="major in majors" :key="major" :value="major">{{ major }}</option>
      </select>
      <select v-model="filterGrade" class="filter-select">
        <option value="">所有年级</option>
        <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}级</option>
      </select>
    </div>

    <div class="student-list">
      <div v-for="student in filteredStudents" :key="student.id" class="student-card">
        <div class="student-avatar">
          <div class="avatar-placeholder">{{ student.name.charAt(0) }}</div>
        </div>
        <div class="student-info">
          <h3>{{ student.name }}</h3>
          <p class="student-username">@{{ student.username }}</p>
          <div class="student-details">
            <span class="tag">{{ getGenderText(student.gender) }}</span>
            <span class="tag tag-primary">{{ student.major }}</span>
            <span class="tag tag-success">{{ student.grade }}级</span>
          </div>
          <div class="student-meta">
            <span>📧 {{ student.email }}</span>
            <span>📱 {{ student.phone || '未设置' }}</span>
          </div>
        </div>
        <div class="student-actions">
          <button @click="viewStudent(student)" class="btn-view">查看详情</button>
        </div>
      </div>
      
      <div v-if="filteredStudents.length === 0" class="empty-state">
        <div class="empty-icon">👥</div>
        <p>暂无学生</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const students = ref<any[]>([])
const searchText = ref('')
const filterMajor = ref('')
const filterGrade = ref('')

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('user') || '{}')
})

const majors = computed(() => {
  const set = new Set(students.value.map(s => s.major))
  return Array.from(set)
})

const grades = computed(() => {
  const set = new Set(students.value.map(s => s.grade))
  return Array.from(set)
})

const getMajorCount = computed(() => majors.value.length)
const getGradeCount = computed(() => grades.value.length)

const filteredStudents = computed(() => {
  return students.value.filter(student => {
    const matchesSearch = searchText.value === '' || 
                         student.name.includes(searchText.value) ||
                         student.username.includes(searchText.value)
    const matchesMajor = filterMajor.value === '' || student.major === filterMajor.value
    const matchesGrade = filterGrade.value === '' || student.grade === filterGrade.value
    return matchesSearch && matchesMajor && matchesGrade
  })
})

const getGenderText = (gender: string) => {
  const map: any = { male: '男', female: '女', other: '其他' }
  return map[gender] || '未知'
}

const fetchStudents = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/auth/students/', {
      headers: { Authorization: `Bearer ${token}` },
      params: { supervisor_id: currentUser.value.id }
    })
    students.value = response.data
  } catch (error) {
    console.error('获取学生列表失败', error)
    // 如果 API 不支持过滤，就在前端过滤
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/auth/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      // 过滤出当前老师的学生
      students.value = response.data.filter((s: any) => s.supervisor === currentUser.value.id)
    } catch (error) {
      console.error('获取学生列表失败', error)
    }
  }
}

const viewStudent = (student: any) => {
  alert(`查看学生详情：${student.name}\n学号：${student.username}\n专业：${student.major}\n年级：${student.grade}`)
}

onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
.page-container { padding: 20px; }

h2 { margin-bottom: 20px; color: #333; }

.stats-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-item {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
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

.student-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.student-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.student-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.student-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
}

.student-info {
  flex: 1;
}

.student-info h3 {
  margin: 0 0 5px;
  color: #333;
  font-size: 18px;
}

.student-username {
  margin: 0 0 10px;
  color: #999;
  font-size: 14px;
}

.student-details {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.tag {
  padding: 4px 12px;
  background: #f0f0f0;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.tag-primary {
  background: #e6f7ff;
  color: #1890ff;
}

.tag-success {
  background: #f6ffed;
  color: #52c41a;
}

.student-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #666;
}

.student-actions {
  flex-shrink: 0;
}

.btn-view {
  padding: 8px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view:hover {
  background: #66b1ff;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}
</style>
