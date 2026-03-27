<template>
  <div class="empty-state">
    <div class="empty-icon">
      <slot name="icon">
        <IconInbox v-if="type === 'default'" class="empty-icon-svg" />
        <IconSearch v-else-if="type === 'search'" class="empty-icon-svg" />
        <IconDocument v-else-if="type === 'no-data'" class="empty-icon-svg" />
        <IconMessageCircle v-else-if="type === 'no-comment'" class="empty-icon-svg" />
      </slot>
    </div>
    <h3 class="empty-title">{{ title }}</h3>
    <p class="empty-description">{{ description }}</p>
    <div v-if="showAction" class="empty-actions">
      <button @click="$emit('action')" class="action-btn">
        {{ actionText }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { IconInbox, IconSearch, IconDocument, IconMessageCircle } from '@/components/icons'

defineProps({
  type: {
    type: String,
    default: 'default',
    validator: (value: string) => ['default', 'search', 'no-data', 'no-comment'].includes(value)
  },
  title: {
    type: String,
    default: '暂无数据'
  },
  description: {
    type: String,
    default: '这里空空如也'
  },
  showAction: {
    type: Boolean,
    default: false
  },
  actionText: {
    type: String,
    default: '立即操作'
  }
})

defineEmits(['action'])
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 64px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.empty-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: #f5f7fa;
  border-radius: 50%;
}

.empty-icon-svg {
  width: 40px;
  height: 40px;
  color: #c0c4cc;
}

.empty-title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.empty-description {
  margin: 0 0 24px;
  font-size: 14px;
  color: #909399;
}

.empty-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.action-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}
</style>
