<template>
  <div class="loading-page" :class="{ 'fade-out': !isLoading }">
    <div class="loading-icon">
      <svg class="spinner" viewBox="0 0 50 50">
        <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="4"></circle>
      </svg>
    </div>
    <div class="loading-text">
      <p>Loading...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isLoading = ref(true)

function hide(): void {
  isLoading.value = false
  // 触发入场动画
  document.documentElement.classList.add('loaded')
}

onMounted(() => {
  // 页面就绪后自动隐藏 loading
  setTimeout(hide, 800)
})

defineExpose({ hide })
</script>

<style scoped>
.spinner {
  animation: rotate 1.4s linear infinite;
  width: 3em;
  height: 3em;
}

.spinner .path {
  stroke: rgb(91, 40, 11);
  stroke-linecap: round;
  animation: dash 1.4s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}
</style>
