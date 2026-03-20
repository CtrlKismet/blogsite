<template>
  <div class="top-rocket" :class="{ visible: isVisible }" @click="scrollToTop">
    <i class="fa fa-2x fa-arrow-up"></i>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const scrollThreshold = 260

function handleScroll(): void {
  if (window.innerWidth <= 900) return
  isVisible.value = window.scrollY > scrollThreshold
}

function scrollToTop(): void {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
