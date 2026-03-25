<template>
  <div class="page-container">
    <div class="back-btn" @click="goBack">← 返回论坛</div>
    
    <div v-if="post" class="post-detail">
      <div class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
          <span class="author">👤 {{ post.author?.name || post.author?.username }}</span>
          <span class="date">📅 {{ post.post_date }}</span>
          <span class="visible-tag">{{ getVisibleText(post.visible_to) }}</span>
        </div>
      </div>
      
      <div class="post-content">
        {{ post.content }}
      </div>
      
      <div class="post-actions">
        <button 
          v-if="canDelete" 
          @click="deletePost" 
          class="btn-delete"
        >
          🗑️ 删除帖子
        </button>
      </div>
      
      <div class="comments-section">
        <h3>💬 评论</h3>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author?.name || comment.author?.username }}</span>
              <span class="comment-date">{{ comment.comment_date }}</span>
            </div>
            <div class="comment-content">
              {{ comment.content }}
            </div>
          </div>
          <div v-if="comments.length === 0" class="empty-state">
            暂无评论，快来抢沙发吧！
          </div>
        </div>
        
        <!-- 发表评论 -->
        <div class="comment-form">
          <h4>发表评论</h4>
          <textarea 
            v-model="newComment" 
            placeholder="写下你的评论..." 
            rows="3"
          ></textarea>
          <button @click="submitComment" class="btn-submit" :disabled="!newComment.trim()">
            发表评论
          </button>
        </div>
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
const post = ref<any>(null)
const comments = ref<any[]>([])
const newComment = ref('')

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('user') || '{}')
})

const canDelete = computed(() => {
  if (!post.value) return false
  const user = currentUser.value
  // 作者本人或管理员可以删除
  return user.id === post.value.author?.id || user.role === 'admin'
})

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const fetchPost = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/${route.params.id}/`)
    post.value = response.data
  } catch (error) {
    console.error('获取帖子详情失败', error)
    alert('帖子不存在')
    goBack()
  }
}

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/${route.params.id}/comments/`)
    comments.value = response.data
  } catch (error) {
    console.error('获取评论失败', error)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/forum/${route.params.id}/comments/`, {
      content: newComment.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    newComment.value = ''
    fetchComments()
  } catch (error) {
    alert('评论失败')
  }
}

const deletePost = async () => {
  if (!confirm('确定要删除这个帖子吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/forum/${route.params.id}/delete/`, {
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
  fetchPost()
  fetchComments()
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

.post-detail {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.post-header {
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.post-header h1 {
  margin: 0 0 15px;
  color: #333;
  font-size: 24px;
}

.post-meta {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.post-content {
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  margin-bottom: 30px;
}

.post-actions {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
  margin-bottom: 30px;
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

.comments-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.comments-list {
  margin-bottom: 30px;
}

.comment-item {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.comment-author {
  font-weight: 600;
}

.comment-content {
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
}

.empty-state {
  text-align: center;
  color: #999;
  padding: 40px;
}

.comment-form h4 {
  margin-bottom: 15px;
  color: #333;
}

.comment-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
  margin-bottom: 15px;
}

.btn-submit {
  padding: 10px 24px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover {
  background: #66b1ff;
}

.btn-submit:disabled {
  background: #c0c4cc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}
</style>
