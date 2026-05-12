<template>
  <div class="page-container fade-in">
    <div class="page-header">
      <div class="header-content">
        <h2>资源上传</h2>
        <p class="subtitle">上传课件、笔记或闲置书籍，赚取积分并帮助他人</p>
      </div>
      <button @click="openUploadModal" class="btn btn-primary">
        <IconUpload class="btn-icon" /> 发布新资源
      </button>
    </div>

    <div class="resource-grid">
      <div v-for="res in myResources" :key="res.id" class="resource-card card slide-up" @click="openResourceDetail(res)">
        <div class="card-status" :class="res.status">
          {{ getStatusText(res.status) }}
        </div>
        <div class="card-body">
          <h3 class="res-title">{{ res.title }}</h3>
          <p class="res-type">{{ res.type_name }}</p>
          <p class="res-desc">{{ res.description || '暂无描述' }}</p>
          <div class="res-meta">
            <div class="meta-item">
              <IconDownload class="meta-icon" />
              <span>{{ res.downloads }} 次下载</span>
            </div>
            <div class="meta-item" v-if="res.is_second_hand">
              <IconTag class="meta-icon" />
              <span class="second-hand-tag">二手 ¥{{ res.price }}</span>
            </div>
            <div class="meta-item" v-else-if="res.points_required > 0">
              <IconStar class="meta-icon" />
              <span class="points-tag">{{ res.points_required }} 积分</span>
            </div>
          </div>
          <div class="res-stats">
            <div class="stat-item">
              <IconClock class="stat-icon" />
              <span>{{ formatDate(res.upload_date) }}</span>
            </div>
            <div class="stat-item" v-if="res.rating">
              <IconStar class="stat-icon" />
              <span>{{ res.rating }} 分</span>
            </div>
          </div>
          <p v-if="res.status === 'rejected'" class="reject-reason">
            驳回原因: {{ res.reject_reason || '不符合平台规范' }}
          </p>
        </div>
        <div class="card-footer" @click.stop>
          <button @click="viewResource(res)" class="btn btn-outline btn-sm">
            <IconEye class="btn-icon" />
            <span>查看</span>
          </button>
          <button @click="deleteResource(res.id)" class="btn btn-danger btn-sm">
            <IconTrash class="btn-icon" />
            <span>删除</span>
          </button>
        </div>
      </div>
      
      <div v-if="myResources.length === 0" class="empty-state card full-width fade-in">
        <IconBook class="empty-icon" />
        <p class="empty-title">你还没有分享过任何资源</p>
        <p class="empty-sub">上传优质资源，帮助他人的同时赚取积分</p>
        <button @click="openUploadModal" class="btn btn-primary mt-4">
          <IconUpload class="btn-icon" />
          <span>发布新资源</span>
        </button>
      </div>
    </div>

    <!-- 资源详情模态框 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-card modal-large slide-up" @click.stop>
        <div class="modal-header">
          <h3>资源详情</h3>
          <button @click="closeDetailModal" class="btn-close"><IconClose /></button>
        </div>
        <div class="modal-body" v-if="selectedResource">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <label>资源标题</label>
                <span>{{ selectedResource.title }}</span>
              </div>
              <div class="detail-item">
                <label>资源分类</label>
                <span>{{ selectedResource.type_name }}</span>
              </div>
              <div class="detail-item">
                <label>上传时间</label>
                <span>{{ formatDateTime(selectedResource.upload_date) }}</span>
              </div>
              <div class="detail-item">
                <label>状态</label>
                <span :class="['status-badge', selectedResource.status]">{{ getStatusText(selectedResource.status) }}</span>
              </div>
              <div class="detail-item" v-if="selectedResource.is_second_hand">
                <label>价格</label>
                <span class="price-tag">¥{{ selectedResource.price }}</span>
              </div>
              <div class="detail-item" v-else-if="selectedResource.points_required > 0">
                <label>所需积分</label>
                <span class="points-tag">{{ selectedResource.points_required }} 积分</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>资源描述</h4>
            <p class="description">{{ selectedResource.description || '暂无描述' }}</p>
          </div>

          <div class="detail-section">
            <h4>统计信息</h4>
            <div class="stats-grid">
              <div class="stat-card">
                <IconDownload class="stat-card-icon" />
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ selectedResource.downloads || 0 }}</div>
                  <div class="stat-card-label">下载次数</div>
                </div>
              </div>
              <div class="stat-card">
                <IconStar class="stat-card-icon" />
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ selectedResource.rating || 0 }}</div>
                  <div class="stat-card-label">平均评分</div>
                </div>
              </div>
              <div class="stat-card">
                <IconMessageCircle class="stat-card-icon" />
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ selectedResource.comments_count || 0 }}</div>
                  <div class="stat-card-label">评论数</div>
                </div>
              </div>
              <div class="stat-card">
                <IconCollection class="stat-card-icon" />
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ selectedResource.collections_count || 0 }}</div>
                  <div class="stat-card-label">收藏数</div>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="selectedResource.status === 'rejected'">
            <h4>驳回原因</h4>
            <p class="reject-reason-full">{{ selectedResource.reject_reason || '不符合平台规范' }}</p>
          </div>

          <div class="detail-actions">
            <button @click="viewResource(selectedResource)" class="btn btn-primary">
              <IconEye class="btn-icon" />
              <span>查看资源页面</span>
            </button>
            <button @click="copyLink(selectedResource.file_url)" class="btn btn-outline" v-if="selectedResource.file_url">
              <IconLink class="btn-icon" />
              <span>复制链接</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showUploadModal" class="modal-overlay" @click="closeUploadModal">
      <div class="modal-card slide-up" @click.stop>
        <div class="modal-header">
          <h3>发布新资源</h3>
          <button @click="closeUploadModal" class="btn-close"><IconClose /></button>
        </div>
        <form @submit.prevent="submitResource" class="modal-body">
          
          <div class="form-group">
            <label>资源标题 <span class="required">*</span></label>
            <input v-model="formData.title" placeholder="如：2023年高等数学期末复习笔记" required class="input" />
          </div>

          <div class="form-group">
            <label>所属分类 <span class="required">*</span></label>
            <select v-model="formData.type_id" required class="input">
              <option value="" disabled>请选择分类</option>
              <optgroup v-for="(subTypes, mainCat) in groupedTypes" :key="mainCat" :label="String(mainCat)">
                <option v-for="t in subTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
              </optgroup>
            </select>
          </div>

          <div class="form-group">
            <label>资源描述</label>
            <textarea v-model="formData.description" placeholder="简要介绍这份资料的内容和适用人群..." rows="3" class="input"></textarea>
          </div>

          <div class="form-group">
            <label>文件或网盘链接 <span class="required">*</span></label>
            <input v-model="formData.file_url" placeholder="请填写百度网盘链接或其他文件地址" required class="input" />
          </div>

          <div class="form-group">
            <label>所需积分</label>
            <input v-model="formData.points_required" type="number" min="0" placeholder="0" class="input" />
            <small class="form-hint">设置为0表示免费</small>
          </div>

          <div class="form-row">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.is_second_hand" />
              这是闲置二手实体书/物品
            </label>
          </div>
          <div v-if="formData.is_second_hand" class="form-group">
            <label>转让价格 (¥)</label>
            <input v-model="formData.price" type="number" step="0.01" min="0" placeholder="例如：15.5" class="input" />
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeUploadModal" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">提交审核</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

import { useToast } from '../../composables/useToast'
import axios from 'axios'
import { formatDate, formatDateTime } from '../../utils/timeFormat'
import { 
  IconUpload, 
  IconClose, 
  IconDownload, 
  IconStar, 
  IconClock, 
  IconEye, 
  IconTrash, 
  IconTag, 
  IconBook, 
  IconMessageCircle, 
  IconCollection,
  IconLink
} from '../icons'

const toast = useToast()
const router = useRouter()
const myResources = ref<any[]>([])
const types = ref<any[]>([])
const showUploadModal = ref(false)
const showDetailModal = ref(false)
const selectedResource = ref<any>(null)

const formData = ref({
  title: '', type_id: '', description: '', file_url: '', 
  points_required: 0, is_second_hand: false, price: 0
})

const groupedTypes = computed(() => {
  const groups: Record<string, any[]> = {}
  types.value.forEach(t => {
    const main = t.description || '其他未分类'
    if (!groups[main]) groups[main] = []
    groups[main].push(t)
  })
  return groups
})

const getStatusText = (status: string) => ({ pending: '待审核', active: '已发布', rejected: '已驳回' }[status] || '未知')

const fetchMyResources = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/courses/teacher/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    myResources.value = res.data
  } catch (error) {
    console.error('获取列表失败', error)
  }
}

const fetchTypes = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/courses/types/')
    types.value = res.data
  } catch (error) { console.error('获取分类失败') }
}

const openUploadModal = () => { showUploadModal.value = true }
const closeUploadModal = () => {
  showUploadModal.value = false
  formData.value = { title: '', type_id: '', description: '', file_url: '', points_required: 0, is_second_hand: false, price: 0 }
}

const openResourceDetail = (resource: any) => {
  selectedResource.value = resource
  showDetailModal.value = true
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedResource.value = null
}

const viewResource = (resource: any) => {
  router.push(`/student/courses/${resource.id}`)
}

const copyLink = (url: string) => {
  navigator.clipboard.writeText(url).then(() => {
    toast.success('链接已复制到剪贴板')
  }).catch(() => {
    toast.error('复制失败，请手动复制')
  })
}

const submitResource = async () => {
  if (!formData.value.type_id) {
    toast.warning('请选择资源分类！')
    return
  }

  try {
    const token = localStorage.getItem('token')
    if (!formData.value.is_second_hand) formData.value.price = 0
    
    const payload = {
      ...formData.value,
      type_id: Number(formData.value.type_id),
      price: Number(formData.value.price || 0),
      points_required: Number(formData.value.points_required || 0)
    }
    
    await axios.post('http://127.0.0.1:8000/api/courses/create/', payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('提交成功，请等待管理员审核！')
    closeUploadModal()
    fetchMyResources()
  } catch (error: any) { 
    console.error('上传失败详情:', error.response?.data)
    const errorMsg = error.response?.data?.type_id?.[0] || 
                     error.response?.data?.file_url?.[0] || 
                     error.response?.data?.detail ||
                     '提交失败，请检查填写内容'
    toast.error(errorMsg)
  }
}

const deleteResource = async (id: number) => {
  if (!confirm('确定要删除这份资源吗？')) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/courses/${id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('删除成功')
    fetchMyResources()
  } catch (error) { toast.error('删除失败') }
}

onMounted(() => {
  fetchMyResources()
  fetchTypes()
})
</script>

<style scoped>
.page-container { 
  padding: var(--spacing-lg); 
  max-width: 1200px; 
  margin: 0 auto; 
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-color);
}

.header-content h2 {
  font-size: var(--font-size-2xl); 
  font-weight: var(--font-weight-bold); 
  color: var(--text-primary); 
  margin-bottom: var(--spacing-xs); 
  font-family: var(--font-sf);
  display: flex;
  align-items: center;
  gap: 12px;
}

.subtitle { 
  color: var(--text-secondary); 
  font-size: var(--font-size-sm);
  margin: 0;
}

.btn {
  display: flex; 
  align-items: center; 
  gap: 8px; 
  padding: 10px 20px; 
  border-radius: var(--border-radius-md); 
  font-weight: var(--font-weight-medium); 
  font-size: 14px; 
  cursor: pointer; 
  border: none; 
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.btn:hover::before {
  opacity: 1;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%); 
  color: white;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.4);
}

.btn-secondary { 
  background: var(--bg-tertiary); 
  color: var(--text-secondary);
  border: 2px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--bg-secondary);
  border-color: var(--text-secondary);
}

.btn-danger { 
  background: rgba(239, 68, 68, 0.1); 
  color: #ef4444;
  border: 2px solid rgba(239, 68, 68, 0.3);
}

.btn-danger:hover { 
  background: #ef4444; 
  color: white;
  border-color: #ef4444;
}

.btn-outline {
  background: transparent;
  border: 2px solid var(--border-color);
  color: var(--text-secondary);
}

.btn-outline:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.05);
}

.btn-sm { 
  padding: 8px 14px; 
  font-size: 13px; 
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: var(--spacing-xl);
}

.card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-light);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.card-status {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: var(--border-radius-full);
  font-weight: var(--font-weight-semibold);
  z-index: 10;
}

.card-status.pending { 
  background: #fef3c7; 
  color: #d97706; 
}
.card-status.active { 
  background: #d1fae5; 
  color: #059669; 
}
.card-status.rejected { 
  background: #fee2e2; 
  color: #dc2626; 
}

.card-body {
  padding: 24px;
  flex: 1;
  margin-top: 10px;
}

.res-title {
  font-size: var(--font-size-lg); 
  font-weight: var(--font-weight-semibold); 
  color: var(--text-primary); 
  margin: 0 0 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.res-type {
  font-size: 13px; 
  color: var(--text-secondary); 
  margin-bottom: 12px;
  background: rgba(13, 148, 136, 0.1);
  color: var(--primary-color);
  padding: 4px 10px;
  border-radius: var(--border-radius-full);
  width: fit-content;
}

.res-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.res-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-tertiary);
}

.meta-icon {
  width: 14px;
  height: 14px;
  color: var(--text-tertiary);
}

.second-hand-tag {
  color: #f59e0b; 
  font-weight: var(--font-weight-semibold);
}

.points-tag {
  color: var(--primary-color);
  font-weight: var(--font-weight-semibold);
}

.res-stats {
  display: flex;
  gap: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.stat-icon {
  width: 12px;
  height: 12px;
  color: var(--text-tertiary);
}

.reject-reason {
  font-size: 12px; 
  color: #dc2626; 
  background: #fee2e2; 
  padding: 8px;
  border-radius: 4px; 
  margin-top: 12px;
}

.card-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: 12px;
  background: var(--bg-secondary);
}

.card-footer .btn {
  flex: 1;
  justify-content: center;
}

.full-width {
  grid-column: 1 / -1;
}

.empty-state {
  padding: 80px 40px;
  text-align: center;
  color: var(--text-tertiary);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: var(--spacing-md);
  color: var(--text-tertiary);
  opacity: 0.6;
}

.empty-title {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-xs);
  font-weight: var(--font-weight-medium);
}

.empty-sub {
  font-size: var(--font-size-sm);
  margin: 0 0 var(--spacing-md);
  color: var(--text-tertiary);
  max-width: 400px;
  line-height: 1.5;
}

.mt-4 {
  margin-top: 16px;
}

.modal-overlay {
  position: fixed; 
  inset: 0; 
  background: rgba(0,0,0,0.5); 
  backdrop-filter: blur(4px); 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 2000;
}

.modal-card {
  background: var(--bg-primary); 
  width: 100%; 
  max-width: 500px; 
  border-radius: var(--border-radius-xl); 
  box-shadow: var(--shadow-xl); 
  overflow: hidden;
}

.modal-large {
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 20px 24px; 
  border-bottom: 1px solid var(--border-light); 
  background: var(--bg-secondary);
  position: sticky;
  top: 0;
  z-index: 10;
}

.modal-header h3 {
  margin: 0; 
  font-size: 18px; 
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.btn-close {
  background: none; 
  border: none; 
  cursor: pointer; 
  color: var(--text-tertiary); 
  display: flex;
  padding: 4px;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s;
}

.btn-close:hover {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-section {
  border: 1px solid var(--border-light);
  border-radius: var(--border-radius-lg);
  padding: 20px;
  background: var(--bg-secondary);
}

.detail-section h4 {
  margin: 0 0 16px;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-light);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
}

.detail-item span {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: var(--font-weight-medium);
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: var(--font-weight-semibold);
}

.status-badge.pending { background: #fef3c7; color: #d97706; }
.status-badge.active { background: #d1fae5; color: #059669; }
.status-badge.rejected { background: #fee2e2; color: #dc2626; }

.price-tag {
  color: #f59e0b; 
  font-weight: var(--font-weight-semibold);
}

.description {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  white-space: pre-line;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.stat-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--border-radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  border-color: var(--primary-light);
}

.stat-card-icon {
  width: 24px;
  height: 24px;
  color: var(--primary-color);
  flex-shrink: 0;
}

.stat-card-content {
  flex: 1;
}

.stat-card-value {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  line-height: 1;
}

.stat-card-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.reject-reason-full {
  font-size: 14px;
  color: #dc2626;
  background: #fee2e2;
  padding: 12px;
  border-radius: 4px;
  margin: 0;
  line-height: 1.5;
}

.detail-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.detail-actions .btn {
  flex: 1;
  justify-content: center;
}

.form-group {
  display: flex; 
  flex-direction: column; 
  gap: 8px;
}

.form-group label {
  font-size: 14px; 
  font-weight: var(--font-weight-medium); 
  color: var(--text-secondary);
}

.required { 
  color: #ef4444; 
}

.input {
  padding: 12px 16px; 
  border: 2px solid var(--border-color); 
  border-radius: var(--border-radius-md); 
  background: var(--bg-secondary); 
  color: var(--text-primary); 
  transition: all 0.2s; 
  font-size: 14px;
}

.input:focus {
  border-color: var(--primary-color); 
  outline: none; 
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.form-row {
  display: flex; 
  align-items: center;
}

.checkbox-label {
  display: flex; 
  align-items: center; 
  gap: 8px; 
  font-size: 14px; 
  color: var(--text-primary); 
  cursor: pointer;
}

.form-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 4px;
}

.modal-footer {
  margin-top: 10px; 
  display: flex; 
  justify-content: flex-end; 
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.fade-in {
  animation: fadeIn var(--transition-normal);
}

.slide-up {
  animation: slideUp var(--transition-normal);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .resource-grid {
    grid-template-columns: 1fr;
  }
  
  .card-footer {
    flex-direction: column;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .detail-actions {
    flex-direction: column;
  }
  
  .modal-large {
    margin: 20px;
    max-height: calc(100vh - 40px);
  }
}
</style>