<template>
  <div class="page-container">
    <h2>资源管理</h2>
    <div class="filter-section">
      <div class="category-tabs">
        <button 
          :class="['tab-btn', resourceCategory === 'all' ? 'active' : '']"
          @click="resourceCategory = 'all'"
        >
          全部资源
        </button>
        <button 
          :class="['tab-btn', resourceCategory === 'online' ? 'active' : '']"
          @click="resourceCategory = 'online'"
        >
          🌐 网络课程
        </button>
        <button 
          :class="['tab-btn', resourceCategory === 'campus' ? 'active' : '']"
          @click="resourceCategory = 'campus'"
        >
          🏫 校内课程
        </button>
        <button 
          :class="['tab-btn', resourceCategory === 'books' ? 'active' : '']"
          @click="resourceCategory = 'books'"
        >
          📚 书籍资源
        </button>
      </div>
      
      <div class="search-box">
        <input v-model="searchText" placeholder="搜索资源标题或描述..." class="search-input" />
      </div>
      <div class="filter-box">
        <select v-model="filterType" class="filter-select">
          <option value="">全部类型</option>
          <option v-for="t in courseTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <select v-model="sortBy" class="filter-select">
          <option value="downloads">下载最多</option>
          <option value="points">积分最低</option>
          <option value="newest">最新上传</option>
        </select>
      </div>
    </div>
    <div class="toolbar">
      <button @click="showAddDialog = true" class="btn-add">添加资源</button>
      <button @click="fetchCourses" class="btn-refresh">刷新</button>
    </div>
    <div class="resource-grid">
      <div v-for="course in filteredCourses" :key="course.id" class="resource-card">
        <div class="resource-header">
          <h3 class="resource-title">{{ course.title }}</h3>
          <span :class="['status-tag', course.status]">{{ getStatusText(course.status) }}</span>
        </div>
        <div class="resource-meta">
          <span class="type-tag">{{ course.type?.name || '未分类' }}</span>
          <span>💎 {{ course.points_required }} 积分</span>
          <span>📥 {{ course.downloads }} 次下载</span>
        </div>
        <p class="resource-description">{{ course.description || '暂无描述' }}</p>
        <div class="resource-footer">
          <div class="resource-info">
            <span v-if="course.is_second_hand">🏷️ 二手 - {{ course.price }}元</span>
            <span>📅 {{ formatTime(course.upload_date) }}</span>
          </div>
          <div class="resource-actions">
            <button @click="editCourse(course)" class="btn-edit">编辑</button>
            <button @click="deleteCourse(course.id)" class="btn-delete">删除</button>
          </div>
        </div>
      </div>
      
      <div v-if="filteredCourses.length === 0" class="empty-state">
        <p>暂无资源</p>
      </div>
    </div>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <h3>{{ showEditDialog ? '编辑资源' : '添加资源' }}</h3>
        <form @submit.prevent="saveCourse">
          <div class="form-group">
            <label>资源名称</label>
            <input v-model="currentCourse.title" placeholder="请输入资源名称" required />
          </div>
          <div class="form-group">
            <label>资源类型</label>
            <select v-model="currentCourse.type" required>
              <option value="">请选择类型</option>
              <option v-for="type in courseTypes" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>资源描述</label>
            <textarea v-model="currentCourse.description" placeholder="请输入资源描述" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>文件地址</label>
            <input v-model="currentCourse.file_url" placeholder="请输入文件地址" />
          </div>
          <div class="form-group">
            <label>所需积分</label>
            <input v-model.number="currentCourse.points_required" type="number" min="0" placeholder="请输入所需积分" />
          </div>
          <div class="form-group">
            <label>是否二手</label>
            <input v-model="currentCourse.is_second_hand" type="checkbox" />
          </div>
          <div class="form-group">
            <label>价格</label>
            <input v-model.number="currentCourse.price" type="number" min="0" step="0.01" placeholder="请输入价格" />
          </div>
          <div class="form-group">
            <label>封面图片</label>
            <input v-model="currentCourse.cover_image" placeholder="请输入封面图片地址" />
          </div>
          <div class="dialog-actions">
            <button type="button" @click="closeDialog" class="btn-cancel">取消</button>
            <button type="submit" class="btn-submit">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const resourceCategory = ref('all')
const searchText = ref('')
const filterType = ref('')
const sortBy = ref('newest')
const currentCourse = ref({
  id: 0,
  title: '',
  type: '',
  description: '',
  file_url: '',
  points_required: 0,
  is_second_hand: false,
  price: 0,
  cover_image: ''
})

const getStatusText = (status: string) => {
  const map: any = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    active: '已发布'
  }
  return map[status] || status
}

const filteredCourses = computed(() => {
  let result = courses.value.filter(course => {
    const matchesSearch = searchText.value === '' || 
                         course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         (course.description && course.description.toLowerCase().includes(searchText.value.toLowerCase()))
    const matchesType = filterType.value === '' || course.type === filterType.value
    
    // 按分类过滤
    let matchesCategory = true
    if (resourceCategory.value === 'online') {
      matchesCategory = course.type_name === '视频' || course.type_name === 'MOOC'
    } else if (resourceCategory.value === 'campus') {
      matchesCategory = course.type_name === '课件' || course.type_name === '作业'
    } else if (resourceCategory.value === 'books') {
      matchesCategory = course.type_name === '文档' || course.type_name === '电子书'
    }
    
    return matchesSearch && matchesType && matchesCategory
  })
  
  // 排序
  if (sortBy.value === 'downloads') {
    result.sort((a, b) => b.downloads - a.downloads)
  } else if (sortBy.value === 'points') {
    result.sort((a, b) => a.points_required - b.points_required)
  } else if (sortBy.value === 'newest') {
    result.sort((a, b) => new Date(b.upload_date).getTime() - new Date(a.upload_date).getTime())
  }
  
  return result
})

const fetchCourses = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/teacher/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courses.value = response.data
  } catch (error) {
    console.error('获取资源列表失败', error)
  }
}

const fetchCourseTypes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courseTypes.value = response.data
  } catch (error) {
    console.error('获取资源类型失败', error)
  }
}

const editCourse = (course: any) => {
  currentCourse.value = {
    id: course.id,
    title: course.title,
    type: course.type?.id || '',
    description: course.description || '',
    file_url: course.file_url || '',
    points_required: course.points_required || 0,
    is_second_hand: course.is_second_hand || false,
    price: course.price || 0,
    cover_image: course.cover_image || ''
  }
  showEditDialog.value = true
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  currentCourse.value = {
    id: 0,
    title: '',
    type: '',
    description: '',
    file_url: '',
    points_required: 0,
    is_second_hand: false,
    price: 0,
    cover_image: ''
  }
}

const saveCourse = async () => {
  try {
    const token = localStorage.getItem('token')
    if (showEditDialog.value) {
      // 编辑现有课程
      await axios.put(`http://127.0.0.1:8000/api/courses/${currentCourse.value.id}/`, currentCourse.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      // 添加新课程
      await axios.post('http://127.0.0.1:8000/api/courses/create/', currentCourse.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    closeDialog()
    fetchCourses()
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

const deleteCourse = async (id: number) => {
  if (confirm('确定要删除这个课程吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/courses/${id}/delete/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      courses.value = courses.value.filter(c => c.id !== id)
      alert('删除成功')
    } catch (error) {
      alert('删除失败')
    }
  }
}

onMounted(() => {
  fetchCourses()
  fetchCourseTypes()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.filter-section { margin-bottom: 20px; }
.category-tabs { display: flex; gap: 10px; margin-bottom: 15px; }
.tab-btn { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.tab-btn.active { background: #409eff; color: white; border-color: #409eff; }
.search-box { margin-bottom: 15px; }
.search-input { width: 300px; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }
.filter-box { display: flex; gap: 10px; margin-bottom: 15px; }
.filter-select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }
.toolbar { margin-bottom: 20px; display: flex; gap: 10px; }
.btn-add, .btn-refresh { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }
.btn-add { background: #67c23a; color: white; }
.btn-refresh { background: #409eff; color: white; }
/* 卡片式布局 */
.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.resource-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
}

.resource-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.resource-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  flex: 1;
}

.resource-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.type-tag {
  padding: 4px 12px;
  background: #f0f0f0;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.resource-description {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.resource-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.resource-info {
  font-size: 13px;
  color: #999;
  display: flex;
  gap: 12px;
}

.resource-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
  grid-column: 1 / -1;
}
.status-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.status-tag.pending { background: #fdf6ec; color: #e6a23c; }
.status-tag.approved, .status-tag.active { background: #f0f9eb; color: #67c23a; }
.status-tag.rejected { background: #fef0f0; color: #f56c6c; }
.actions { display: flex; gap: 5px; }
.btn-edit, .btn-delete { padding: 4px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
.btn-edit { background: #409eff; color: white; }
.btn-delete { background: #f56c6c; color: white; }
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.dialog { background: white; padding: 24px; border-radius: 8px; min-width: 450px; max-height: 90vh; overflow-y: auto; }
.dialog h3 { margin: 0 0 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 8px; color: #666; font-weight: 500; }
.form-group input, .form-group textarea, .form-group select { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.dialog-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-cancel { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
