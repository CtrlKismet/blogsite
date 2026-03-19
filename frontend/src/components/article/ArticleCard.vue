<template>
  <div class="article-card">
    <div class="time-stamp">
      <p>{{ month }}</p>
      <p>{{ day }}</p>
    </div>
    <router-link :to="`/blog/${article.id}`" class="art-content">
      <div class="art-title ellipsis">{{ article.title }}</div>
      <div class="art-ellipsis">{{ article.summary }}</div>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const month = computed(() => {
  if (!props.article.published_at) return ''
  const d = new Date(props.article.published_at)
  return (d.getMonth() + 1) + '月'
})

const day = computed(() => {
  if (!props.article.published_at) return ''
  const d = new Date(props.article.published_at)
  return d.getDate() + ''
})
</script>
