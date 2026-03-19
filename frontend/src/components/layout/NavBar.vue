<template>
  <nav class="head-bar" :class="{ hidden: isHidden }">
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
const topThreshold = 80

function handleScroll(): void {
  isHidden.value = window.scrollY > topThreshold
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
