<template>
  <div class="skeleton" :class="{ 'skeleton-circle': type === 'circle', 'skeleton-square': type === 'square' }">
    <div v-if="type === 'text'" class="skeleton-text" :style="{ width: width, height: height }"></div>
    <div v-else-if="type === 'circle'" class="skeleton-circle" :style="{ width: width, height: height, borderRadius: '50%' }"></div>
    <div v-else-if="type === 'square'" class="skeleton-square" :style="{ width: width, height: height, borderRadius: borderRadius }"></div>
    <div v-else-if="type === 'card'" class="skeleton-card">
      <div class="skeleton-card-header">
        <div class="skeleton-circle" style="width: 40px; height: 40px"></div>
        <div class="skeleton-card-title">
          <div class="skeleton-text" style="width: 120px; height: 16px"></div>
          <div class="skeleton-text" style="width: 80px; height: 12px; margin-top: 8px"></div>
        </div>
      </div>
      <div class="skeleton-card-body">
        <div class="skeleton-text" style="width: 100%; height: 14px"></div>
        <div class="skeleton-text" style="width: 80%; height: 14px; margin-top: 8px"></div>
        <div class="skeleton-text" style="width: 90%; height: 14px; margin-top: 8px"></div>
      </div>
      <div class="skeleton-card-footer">
        <div class="skeleton-text" style="width: 60px; height: 12px"></div>
      </div>
    </div>
    <div v-else-if="type === 'list'" class="skeleton-list">
      <div v-for="i in count" :key="i" class="skeleton-list-item">
        <div class="skeleton-circle" style="width: 48px; height: 48px"></div>
        <div class="skeleton-list-content">
          <div class="skeleton-text" style="width: 200px; height: 16px"></div>
          <div class="skeleton-text" style="width: 150px; height: 14px; margin-top: 8px"></div>
          <div class="skeleton-text" style="width: 100px; height: 12px; margin-top: 6px"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  type: {
    type: String,
    default: 'text',
    validator: (value: string) => ['text', 'circle', 'square', 'card', 'list'].includes(value)
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '16px'
  },
  borderRadius: {
    type: String,
    default: '4px'
  },
  count: {
    type: Number,
    default: 3
  }
})
</script>

<style scoped>
.skeleton {
  display: inline-block;
  position: relative;
  overflow: hidden;
  background-color: var(--border-light);
}

.skeleton-text {
  background-color: var(--border-light);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.skeleton-circle {
  background-color: var(--border-light);
  border-radius: 50%;
  position: relative;
  overflow: hidden;
}

.skeleton-square {
  background-color: var(--border-light);
  position: relative;
  overflow: hidden;
}

.skeleton-card {
  background-color: var(--bg-primary);
  border-radius: var(--border-radius-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
  width: 100%;
}

.skeleton-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.skeleton-card-title {
  flex: 1;
}

.skeleton-card-body {
  margin-bottom: 16px;
}

.skeleton-card-footer {
  display: flex;
  justify-content: flex-end;
}

.skeleton-list {
  width: 100%;
}

.skeleton-list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-light);
}

.skeleton-list-item:last-child {
  border-bottom: none;
}

.skeleton-list-content {
  flex: 1;
}

/* 动画效果 */
.skeleton::after,
.skeleton-text::after,
.skeleton-circle::after,
.skeleton-square::after,
.skeleton-card::after,
.skeleton-list::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>