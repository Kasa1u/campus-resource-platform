<template>
  <div class="page-container">
    <h2>我的积分</h2>

    <div class="points-hero">
      <div class="points-circle">
        <div class="points-value">{{ totalPoints }}</div>
        <div class="points-label">当前积分</div>
      </div>
      <div class="points-summary">
        <div class="summary-item">
          <span class="summary-num add">+{{ totalAdded }}</span>
          <span class="summary-desc">累计获得</span>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
          <span class="summary-num deduct">-{{ totalDeducted }}</span>
          <span class="summary-desc">累计消耗</span>
        </div>
      </div>
    </div>

    <div class="rewards-section">
      <h3 class="section-title"><IconTrophy class="section-icon-svg" /> 积分兑换</h3>
      <div class="rewards-grid">
        <div v-for="prize in prizes" :key="prize.id" class="reward-card" :class="{ disabled: prize.points_required > totalPoints }">
          <div class="reward-image">
            <img :src="prize.image_url || 'https://via.placeholder.com/120'" :alt="prize.name" />
          </div>
          <div class="reward-info">
            <div class="reward-name">{{ prize.name }}</div>
            <div class="reward-points">{{ prize.points_required }} 积分</div>
            <div class="reward-stock">剩余：{{ prize.stock }}</div>
            <button 
              @click="exchangePrize(prize)" 
              class="exchange-btn"
              :disabled="prize.points_required > totalPoints || prize.stock === 0"
            >
              {{ prize.stock === 0 ? '已兑完' : '立即兑换' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="records-card">
      <h3 class="records-title">积分明细</h3>
      <div v-if="records.length > 0" class="record-list">
        <div v-for="record in records" :key="record.id" class="record-item">
          <div class="record-left">
            <span class="record-icon">
              <IconGift v-if="record.type === 'add'" class="record-icon-svg" />
              <IconDownload v-else class="record-icon-svg" />
            </span>
            <div>
              <div class="record-reason">{{ record.reason }}</div>
              <div class="record-time">{{ formatDate(record.record_date) }}</div>
            </div>
          </div>
          <span :class="['record-points', record.type]">
            {{ record.type === 'add' ? '+' : '-' }}{{ record.points }}
          </span>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="empty-icon">
          <IconGift class="empty-icon-svg" />
        </div>
        <p>暂无积分记录</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { IconGift, IconTrophy, IconDownload } from '@/components/icons'

const totalPoints = ref(0)
const records = ref<any[]>([])
const prizes = ref<any[]>([])

const totalAdded = computed(() =>
  records.value.filter(r => r.type === 'add').reduce((s, r) => s + r.points, 0)
)
const totalDeducted = computed(() =>
  records.value.filter(r => r.type === 'deduct').reduce((s, r) => s + r.points, 0)
)

const formatDate = (d: string) => new Date(d).toLocaleString('zh-CN')

const exchangePrize = async (prize: any) => {
  if (confirm(`确定要兑换"${prize.name}"吗？将消耗 ${prize.points_required} 积分`)) {
    try {
      const token = localStorage.getItem('token')
      await axios.post('http://127.0.0.1:8000/api/points/exchange/', {
        prize_id: prize.id
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert('兑换成功！')
      // 刷新数据
      fetchPointsData()
      fetchPrizes()
    } catch (e: any) {
      alert(e.response?.data?.error || '兑换失败')
    }
  }
}

const fetchPointsData = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/points/user/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    totalPoints.value = res.data.total_points
    records.value = res.data.records
  } catch (e) {
    console.error('获取积分记录失败', e)
  }
}

const fetchPrizes = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/points/prizes/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    prizes.value = res.data
  } catch (e) {
    console.error('获取奖品列表失败', e)
  }
}

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) totalPoints.value = JSON.parse(userStr).points || 0
  fetchPointsData()
  fetchPrizes()
})
</script>

<style scoped>
.page-container { padding: 24px; }
.page-container h2 { margin: 0 0 24px; font-size: 22px; color: #1a1a2e; }

.points-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 36px 40px;
  display: flex;
  align-items: center;
  gap: 48px;
  margin-bottom: 28px;
  color: white;
  box-shadow: 0 8px 24px rgba(102,126,234,0.35);
}
.points-circle {
  text-align: center;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  width: 140px;
  height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 3px solid rgba(255,255,255,0.3);
  flex-shrink: 0;
}
.points-value { font-size: 44px; font-weight: 700; line-height: 1; }
.points-label { font-size: 13px; opacity: 0.85; margin-top: 6px; }

.points-summary { display: flex; align-items: center; gap: 40px; }
.summary-item { text-align: center; }
.summary-num { display: block; font-size: 32px; font-weight: 700; }
.summary-num.add { color: #a8f0c6; }
.summary-num.deduct { color: #ffb3b3; }
.summary-desc { font-size: 13px; opacity: 0.85; margin-top: 4px; display: block; }
.summary-divider { width: 1px; height: 50px; background: rgba(255,255,255,0.25); }

/* 兑换区样式 */
.rewards-section { margin-bottom: 28px; }
.section-title { margin: 0 0 20px; font-size: 18px; color: #1a1a2e; display: flex; align-items: center; gap: 8px; }
.section-icon-svg { width: 22px; height: 22px; color: #f59e0b; }
.rewards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
.reward-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s; border: 2px solid transparent; }
.reward-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.12); }
.reward-card.disabled { opacity: 0.6; filter: grayscale(0.8); }
.reward-card.disabled .exchange-btn { background: #ccc; cursor: not-allowed; }
.reward-image { width: 100%; height: 140px; overflow: hidden; background: #f5f5f5; display: flex; align-items: center; justify-content: center; }
.reward-image img { width: 100%; height: 100%; object-fit: cover; }
.reward-info { padding: 16px; }
.reward-name { font-size: 15px; font-weight: 600; color: #303133; margin-bottom: 8px; }
.reward-points { font-size: 18px; font-weight: 700; color: #f59e0b; margin-bottom: 6px; }
.reward-stock { font-size: 13px; color: #909399; margin-bottom: 12px; }
.exchange-btn { width: 100%; padding: 10px; background: linear-gradient(135deg, #f59e0b, #fbbf24); color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.exchange-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4); }

.records-card {
  background: white;
  border-radius: 16px;
  padding: 28px 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.records-title { margin: 0 0 20px; font-size: 16px; color: #303133; }

.record-list { display: flex; flex-direction: column; gap: 4px; }
.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-radius: 10px;
  transition: background 0.15s;
}
.record-item:hover { background: #f8f9fc; }
.record-left { display: flex; align-items: center; gap: 14px; }
.record-icon { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: #f5f7fa; border-radius: 50%; }
.record-icon-svg { width: 20px; height: 20px; color: #606266; }
.empty-icon-svg { width: 48px; height: 48px; color: #c0c4cc; }
.record-reason { font-size: 14px; color: #303133; font-weight: 500; }
.record-time { font-size: 12px; color: #909399; margin-top: 3px; }
.record-points { font-size: 18px; font-weight: 700; }
.record-points.add { color: #67c23a; }
.record-points.deduct { color: #f56c6c; }

.empty-state { text-align: center; padding: 48px 20px; color: #c0c4cc; }
.empty-icon { display: flex; align-items: center; justify-content: center; margin-bottom: 12px; }
.empty-state p { margin: 0; font-size: 14px; }
</style>