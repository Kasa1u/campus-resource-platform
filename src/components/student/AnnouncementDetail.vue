<template>
  <div class="page-container">
    <div class="back-btn" @click="goBack">← 返回公告列表</div>
    
    <div v-if="announcement" class="announcement-detail">
      <div class="announcement-header">
        <h1>{{ announcement.title }}</h1>
        <div class="announcement-meta">
          <span class="author">👤 {{ announcement.author?.name || announcement.author?.username }}</span>
          <span class="date">📅 {{ announcement.publish_date }}</span>
        </div>
      </div>
      
      <div class="announcement-content">
        {{ announcement.content }}
      </div>
      
      <div v-if="canDelete" class="announcement-actions">
        <button @click="deleteAnnouncement" class="btn-delete">
          🗑️ 删除公告
        </button>
      </div>
    </div>
    
    <div v-else class="loading">
      加载中...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const announcement = ref<any>(null)

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('user') || '{}')
})

const canDelete = computed(() => {
  if (!announcement.value) return false
  const user = currentUser.value
  // 作者本人或管理员可以删除
  return user.id === announcement.value.author?.id || user.role === 'admin'
})

const fetchAnnouncement = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/announcements/${route.params.id}/`)
    announcement.value = response.data
  } catch (error) {
    console.error('获取公告详情失败', error)
    alert('公告不存在')
    goBack()
  }
}

const deleteAnnouncement = async () => {
  if (!confirm('确定要删除这个公告吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/announcements/${route.params.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('删除成功')
    goBack()
  } catch (error) {
    alert('删除失败')
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchAnnouncement()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.back-btn {
  display: inline-block;
  padding: 8px 16px;
  background: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #e0e0e0;
}

.announcement-detail {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.announcement-header {
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.announcement-header h1 {
  margin: 0 0 15px;
  color: #333;
  font-size: 24px;
}

.announcement-meta {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.announcement-content {
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  margin-bottom: 30px;
}

.announcement-actions {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
}

.btn-delete {
  padding: 8px 16px;
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete:hover {
  background: #f78989;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}
</style>
