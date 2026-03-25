<template>
  <nav class="head-bar" :class="{ loaded: isLoaded, hidden: isHidden }">
    <div class="nav-item nav-home hover">
      <router-link to="/">.◕ᴗ◕.</router-link>
    </div>
    <div class="nav-menu">
      <div class="nav-item hover">
        <router-link to="/archive">归档</router-link>
      </div>
    </div>
    <div class="nav-item nav-about hover">
      <router-link to="/about">About</router-link>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isHidden = ref(false)
const isLoaded = ref(false)
const topThreshold = 80

function handleScroll(): void {
  if (!isLoaded.value) return
  isHidden.value = window.scrollY > topThreshold
}

onMounted(() => {
  // Trigger entrance animation after a frame
  requestAnimationFrame(() => { isLoaded.value = true })
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
