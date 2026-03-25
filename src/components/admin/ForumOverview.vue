<template>
  <div class="page-container">
    <div class="page-header">
      <button @click="goBack" class="btn-back">← 返回数据分析</button>
      <h2>论坛帖子总览</h2>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-value">{{ totalPosts }}</div>
        <div class="summary-label">总帖子数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ totalComments }}</div>
        <div class="summary-label">总评论数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ activePosts }}</div>
        <div class="summary-label">活跃帖子</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ topPostAuthor }}</div>
        <div class="summary-label">最高产作者</div>
      </div>
    </div>

    <!-- 帖子列表 -->
    <div class="post-section">
      <h3>帖子列表</h3>
      <div class="filter-bar">
        <input v-model="searchText" placeholder="搜索帖子标题..." class="search-input" />
      </div>
      
      <div class="post-list">
        <div v-for="post in filteredPosts" :key="post.id" class="post-card">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-meta">
            <span>👤 {{ post.author?.name || post.author?.username || '未知' }}</span>
            <span>📅 {{ formatTime(post.post_date) }}</span>
            <span>💬 {{ post.comment_count || 0 }} 评论</span>
          </div>
          <div class="post-content">{{ post.content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'

const router = useRouter()
const posts = ref<any[]>([])
const searchText = ref('')

const totalPosts = computed(() => posts.value.length)
const totalComments = computed(() => posts.value.reduce((sum, p) => sum + (p.comment_count || 0), 0))
const activePosts = computed(() => posts.value.filter(p => p.comment_count > 0).length)
const topPostAuthor = computed(() => {
  const authorCount: any = {}
  posts.value.forEach(p => {
    const author = p.author?.name || p.author?.username || '未知'
    authorCount[author] = (authorCount[author] || 0) + 1
  })
  let topAuthor = '无'
  let maxCount = 0
  for (const [author, count] of Object.entries(authorCount)) {
    if (count > maxCount) {
      maxCount = count
      topAuthor = `${author} (${count}篇)`
    }
  }
  return topAuthor
})

const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    return searchText.value === '' || 
           post.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
           (post.content && post.content.toLowerCase().includes(searchText.value.toLowerCase()))
  })
})

const fetchPosts = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/forum/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    posts.value = response.data
  } catch (error) {
    console.error('获取帖子列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchPosts()
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
  color: #f56c6c;
  margin-bottom: 10px;
}

.summary-label {
  font-size: 14px;
  color: #666;
}

.post-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.filter-bar {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.post-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.post-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.post-content {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>