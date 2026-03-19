<template>
  <div class="loading-page" :class="{ 'fade-out': !isLoading }">
    <div class="loading-icon">⟳</div>
    <div class="loading-text">
      <p>Loading...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isLoading = ref(true)

function hide() {
  isLoading.value = false
}

onMounted(() => {
  // 页面就绪后自动隐藏 loading
  setTimeout(hide, 800)
})

defineExpose({ hide })
</script>
