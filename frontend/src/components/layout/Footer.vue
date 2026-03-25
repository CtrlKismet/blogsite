<template>
  <div class="footer" :class="{ visible: isVisible }">
    <div class="text">
      <span>&copy; CtrlKismet's Blog</span>
      <span> | Powered by
        <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>
        &amp;
        <a href="https://vuejs.org/" target="_blank">Vue 3</a>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isVisible = ref(false)
const router = useRouter()

// Initial load: show after content settles
onMounted(() => {
  setTimeout(() => { isVisible.value = true }, 1500)
})

// Route change: hide briefly, show after new content enters
router.afterEach(() => {
  isVisible.value = false
  setTimeout(() => { isVisible.value = true }, 1200)
})
</script>
