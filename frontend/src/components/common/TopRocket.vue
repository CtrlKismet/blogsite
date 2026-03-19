<template>
  <div class="top-rocket" :class="{ visible: isVisible }" @click="scrollToTop">
    ↑
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const scrollThreshold = 260

function handleScroll() {
  if (window.innerWidth <= 900) return
  isVisible.value = window.scrollY > scrollThreshold
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
