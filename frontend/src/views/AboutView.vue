<template>
  <div class="content">
    <main>
      <div class="blog about" v-if="article">
        <div class="blog-content" v-html="article.content_html"></div>
      </div>
      <div v-else-if="!loading" style="text-align: center; padding: 2em;">
        About 页面暂未配置
      </div>
    </main>
    <Sidebar :tags="[]" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getAbout } from '../api/articles'

const article = ref(null)
const loading = ref(false)

async function fetchAbout() {
  loading.value = true
  try {
    const res = await getAbout()
    article.value = res.data
  } catch (e) {
    console.error('获取 About 页面失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAbout()
})
</script>
