<template>
  <div class="page-container">
    <div class="page-header">
      <button @click="goBack" class="btn-back">← 返回数据分析</button>
      <h2>资源总览</h2>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-value">{{ totalResources }}</div>
        <div class="summary-label">总资源数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ activeResources }}</div>
        <div class="summary-label">已发布</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ pendingResources }}</div>
        <div class="summary-label">待审核</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ rejectedResources }}</div>
        <div class="summary-label">已拒绝</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ totalDownloads }}</div>
        <div class="summary-label">总下载次数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ totalComments }}</div>
        <div class="summary-label">总评论数</div>
      </div>
    </div>

    <!-- 资源类型分布 -->
    <div class="type-distribution">
      <h3>资源类型分布</h3>
      <div class="type-grid">
        <div v-for="(count, type) in resourceTypeDistribution" :key="type" class="type-card">
          <div class="type-value">{{ count }}</div>
          <div class="type-label">{{ type }}</div>
        </div>
      </div>
    </div>

    <!-- 资源列表 -->
    <div class="resource-section">
      <h3>资源列表</h3>
      <div class="filter-bar">
        <input v-model="searchText" placeholder="搜索资源标题..." class="search-input" />
        <select v-model="filterStatus" class="filter-select">
          <option value="">全部状态</option>
          <option value="active">已发布</option>
          <option value="pending">待审核</option>
          <option value="rejected">已拒绝</option>
        </select>
      </div>
      
      <div class="resource-list">
        <div v-for="resource in filteredResources" :key="resource.id" class="resource-card">
          <div class="resource-title">{{ resource.title }}</div>
          <div class="resource-meta">
            <span class="type-tag">{{ resource.type_name || '未分类' }}</span>
            <span>💎 {{ resource.points_required }} 积分</span>
            <span>📥 {{ resource.downloads }} 次下载</span>
            <span :class="['status-tag', resource.status]">{{ getStatusText(resource.status) }}</span>
          </div>
          <div class="resource-uploader">
            上传人：{{ resource.uploader?.name || resource.uploader?.username || '未知' }}
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
const resources = ref<any[]>([])
const searchText = ref('')
const filterStatus = ref('')

const totalResources = computed(() => resources.value.length)
const activeResources = computed(() => resources.value.filter(r => r.status === 'active').length)
const pendingResources = computed(() => resources.value.filter(r => r.status === 'pending').length)
const rejectedResources = computed(() => resources.value.filter(r => r.status === 'rejected').length)
const totalDownloads = computed(() => resources.value.reduce((sum, r) => sum + (r.downloads || 0), 0))
const totalComments = computed(() => resources.value.reduce((sum, r) => sum + (r.comment_count || 0), 0))
const resourceTypeDistribution = computed(() => {
  const distribution: any = {}
  resources.value.forEach(r => {
    const type = r.type_name || '未分类'
    distribution[type] = (distribution[type] || 0) + 1
  })
  return distribution
})

const filteredResources = computed(() => {
  return resources.value.filter(resource => {
    const matchSearch = searchText.value === '' || 
                       resource.title.toLowerCase().includes(searchText.value.toLowerCase())
    const matchStatus = filterStatus.value === '' || resource.status === filterStatus.value
    return matchSearch && matchStatus
  })
})

const getStatusText = (status: string) => {
  const map: any = { active: '已发布', pending: '待审核', rejected: '已拒绝', approved: '已通过' }
  return map[status] || status
}

const fetchResources = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    resources.value = response.data
  } catch (error) {
    console.error('获取资源列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchResources()
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
  color: #67c23a;
  margin-bottom: 10px;
}

.summary-label {
  font-size: 14px;
  color: #666;
}

.resource-section h3 {
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

.resource-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.resource-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.resource-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.resource-meta {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.type-tag {
  padding: 3px 10px;
  background: #f0f0f0;
  border-radius: 12px;
  font-size: 12px;
}

.status-tag {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.status-tag.active {
  background: #f6ffed;
  color: #52c41a;
}

.status-tag.pending {
  background: #fff7e6;
  color: #fa8c16;
}

.status-tag.rejected {
  background: #fff1f0;
  color: #f5222d;
}

.resource-uploader {
  font-size: 14px;
  color: #999;
}

.type-distribution {
  margin-bottom: 30px;
}

.type-distribution h3 {
  margin-bottom: 20px;
  color: #333;
}

.type-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.type-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.type-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.type-label {
  font-size: 14px;
  color: #666;
}
</style>
