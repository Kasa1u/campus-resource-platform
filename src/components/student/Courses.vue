<template>
  <div class="page-container">
    <h2>资源浏览</h2>
    
    <!-- 分类卡片入口 -->
    <div v-if="!showResourceList" class="category-entrance">
      <div class="category-card" @click="enterCategory('online')">
        <div class="category-icon">🌐</div>
        <h3>网络课程</h3>
        <p>精选优质在线课程资源</p>
        <div class="category-count">{{ getCount('online') }} 个资源</div>
      </div>
      <div class="category-card" @click="enterCategory('campus')">
        <div class="category-icon">🏫</div>
        <h3>校内课程</h3>
        <p>本校教师上传的课程资源</p>
        <div class="category-count">{{ getCount('campus') }} 个资源</div>
      </div>
      <div class="category-card" @click="enterCategory('books')">
        <div class="category-icon">📚</div>
        <h3>书籍资源</h3>
        <p>电子书、文档等学习资料</p>
        <div class="category-count">{{ getCount('books') }} 个资源</div>
      </div>
    </div>
    
    <!-- 资源列表页面 -->
    <div v-else class="resource-list-page">
      <div class="page-header">
        <button @click="backToCategories" class="btn-back">← 返回分类</button>
        <h3>{{ getCategoryTitle() }}</h3>
      </div>
      
      <div class="filter-section">
        <div class="search-box">
          <input v-model="searchText" :placeholder="getPlaceholder()" class="search-input" />
        </div>
        <div class="filter-box">
          <select v-model="filterType" class="filter-select">
            <option value="">全部类型</option>
            <option v-for="t in filteredTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
          <select v-model="sortBy" class="filter-select">
            <option value="downloads">下载最多</option>
            <option value="points">积分最低</option>
            <option value="newest">最新上传</option>
          </select>
        </div>
      </div>

    <div class="course-grid">
      <div v-for="course in filteredCourses" :key="course.id" class="course-card">
        <div class="course-header">
          <span class="course-type">{{ course.type_name || '未分类' }}</span>
          <span class="course-points">💎 {{ course.points_required }} 积分</span>
        </div>
        <h3 class="course-title">{{ course.title }}</h3>
        <p class="course-description">{{ course.description }}</p>
        <div class="course-meta">
          <span>👨‍🏫 {{ course.uploader?.name || course.uploader?.username || '未知' }}</span>
          <span>📥 {{ course.downloads }} 次下载</span>
        </div>
        <div class="course-actions">
          <button @click="toggleCollect(course)" :class="['btn-collect', isCollected(course.id) ? 'collected' : '']">
            {{ isCollected(course.id) ? '★ 已收藏' : '☆ 收藏' }}
          </button>
          <button @click="viewDetails(course)" class="btn-view">查看详情</button>
          <button @click="downloadCourse(course)" class="btn-download">下载</button>
        </div>
      </div>
      
      <div v-if="filteredCourses.length === 0" class="empty-state">
        <p>暂无课程数据</p>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const searchText = ref('')
const filterType = ref('')
const sortBy = ref('downloads')
const currentCategory = ref('')
const showResourceList = ref(false)
const collections = ref<any[]>([])

const filteredTypes = computed(() => {
  if (currentCategory.value === 'online') {
    // 网络课程类型：视频、MOOC 等
    return courseTypes.value.filter(type => type.name === '视频' || type.name === 'MOOC')
  } else if (currentCategory.value === 'campus') {
    // 校内课程类型：课件、作业等
    return courseTypes.value.filter(type => type.name === '课件' || type.name === '作业')
  } else if (currentCategory.value === 'books') {
    // 书籍资源类型：文档、电子书等
    return courseTypes.value.filter(type => type.name === '文档' || type.name === '电子书')
  }
  return courseTypes.value
})

const filteredCourses = computed(() => {
  let result = courses.value.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchText.value.toLowerCase())
    const matchesType = !filterType.value || course.type === filterType.value
    
    // 根据标签页过滤
    let matchesTab = true
    if (currentCategory.value === 'online') {
      // 网络课程：视频、MOOC 类型
      matchesTab = course.type_name === '视频' || course.type_name === 'MOOC'
    } else if (currentCategory.value === 'campus') {
      // 校内课程：课件、作业类型
      matchesTab = course.type_name === '课件' || course.type_name === '作业'
    } else if (currentCategory.value === 'books') {
      // 书籍资源：文档、电子书类型
      matchesTab = course.type_name === '文档' || course.type_name === '电子书'
    }
    
    return matchesSearch && matchesType && matchesTab
  })
  
  if (sortBy.value === 'downloads') {
    result.sort((a, b) => b.downloads - a.downloads)
  } else if (sortBy.value === 'points') {
    result.sort((a, b) => a.points_required - b.points_required)
  } else if (sortBy.value === 'newest') {
    result.sort((a, b) => new Date(b.upload_date).getTime() - new Date(a.upload_date).getTime())
  }
  
  return result
})

const fetchCourseTypes = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/')
    courseTypes.value = response.data
  } catch (error) {
    console.error('获取课程类型失败', error)
  }
}

const fetchCourses = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/courses/')
    courses.value = response.data
  } catch (error) {
    console.error('获取课程列表失败', error)
  }
}

const enterCategory = (category: string) => {
  console.log('进入分类:', category)
  currentCategory.value = category
  showResourceList.value = true
}

const backToCategories = () => {
  console.log('返回分类')
  showResourceList.value = false
}

const getCategoryTitle = () => {
  const titles: any = { online: '网络课程', campus: '校内课程', books: '书籍资源' }
  return titles[currentCategory.value] || '资源列表'
}

const getCount = (category: string) => {
  if (category === 'online') {
    return courses.value.filter(c => c.type_name === '视频' || c.type_name === 'MOOC').length
  } else if (category === 'campus') {
    return courses.value.filter(c => c.type_name === '课件' || c.type_name === '作业').length
  } else if (category === 'books') {
    return courses.value.filter(c => c.type_name === '文档' || c.type_name === '电子书').length
  }
  return 0
}

const fetchCollections = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = response.data
  } catch (error) {
    console.error('获取收藏列表失败', error)
  }
}

const isCollected = (courseId: number) => {
  return collections.value.some(c => c.resource && c.resource.id === courseId)
}

const toggleCollect = async (course: any) => {
  try {
    const token = localStorage.getItem('token')
    
    if (isCollected(course.id)) {
      const collection = collections.value.find(c => c.resource && c.resource.id === course.id)
      if (collection) {
        await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${collection.id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }
      collections.value = collections.value.filter(c => c.resource && c.resource.id !== course.id)
      alert('已取消收藏')
    } else {
      await axios.post('http://127.0.0.1:8000/api/courses/collect/', 
        { resource: course.id },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      await fetchCollections()
      alert('收藏成功')
    }
  } catch (error) {
    alert('操作失败')
  }
}

const viewDetails = (course: any) => {
  alert(`课程详情:\n\n名称: ${course.title}\n类型: ${course.type_name}\n\n描述: ${course.description}\n\n所需积分: ${course.points_required}`)
}

const downloadCourse = async (course: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/courses/${course.id}/download/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    course.downloads += 1
    alert('下载成功！')
  } catch (error: any) {
    alert(error.response?.data?.error || '下载失败')
  }
}

const getPlaceholder = () => {
  if (currentCategory.value === 'online') {
    return '搜索网络课程...'
  } else if (currentCategory.value === 'campus') {
    return '搜索校内课程...'
  } else {
    return '搜索书籍...'
  }
}

onMounted(() => {
  fetchCourseTypes()
  fetchCourses()
  fetchCollections()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.tab-section { display: flex; gap: 10px; margin-bottom: 24px; border-bottom: 1px solid #eaeaea; }
.tab-btn { padding: 10px 20px; border: none; background: none; border-bottom: 2px solid transparent; cursor: pointer; font-size: 14px; font-weight: 500; color: #666; transition: all 0.3s; }
.tab-btn:hover { color: #409eff; }
.tab-btn.active { color: #409eff; border-bottom-color: #409eff; }
.filter-section { margin-bottom: 24px; }
.search-box { display: flex; gap: 10px; margin-bottom: 16px; }
.search-input { flex: 1; padding: 10px 16px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.filter-box { display: flex; gap: 12px; }
.filter-select { padding: 10px 16px; border: 1px solid #ddd; border-radius: 6px; min-width: 150px; }

.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
.course-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); transition: transform 0.2s; }
.course-card:hover { transform: translateY(-4px); }
.course-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.course-type { display: inline-block; padding: 4px 12px; background: #e6f7ff; color: #1890ff; border-radius: 4px; font-size: 12px; }
.course-points { color: #e6a23c; font-size: 14px; }
.course-title { font-size: 18px; font-weight: 600; margin: 0 0 8px; color: #333; }
.course-description { color: #666; font-size: 14px; margin: 0 0 16px; line-height: 1.6; }
.course-meta { display: flex; justify-content: space-between; color: #999; font-size: 13px; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #eee; }
.course-actions { display: flex; gap: 8px; }
.btn-collect, .btn-view, .btn-download { flex: 1; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; }
.btn-collect { background: #f0f9eb; color: #67c23a; }
.btn-collect.collected { background: #67c23a; color: white; }
.btn-view { background: #f4f4f5; color: #909399; }
.btn-download { background: #409eff; color: white; }

.empty-state { text-align: center; padding: 60px 20px; color: #999; }

/* 分类卡片入口样式 */
.category-entrance {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.category-card {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

.category-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.category-card h3 {
  margin: 0 0 10px;
  color: #333;
  font-size: 20px;
}

.category-card p {
  margin: 0 0 20px;
  color: #666;
  font-size: 14px;
}

.category-count {
  display: inline-block;
  padding: 6px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

/* 资源列表页面样式 */
.resource-list-page {
  margin-top: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.btn-back {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-back:hover {
  background: #e0e0e0;
}

.page-header h3 {
  margin: 0;
  color: #333;
  font-size: 20px;
}
</style>
