<template>
  <div class="article-card">
    <div class="time-stamp">
      <p>{{ year }}</p>
      <p>{{ monthDay }}</p>
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

const year = computed(() => {
  if (!props.article.published_at) return ''
  const d = new Date(props.article.published_at)
  return d.getFullYear()
})

const monthDay = computed(() => {
  if (!props.article.published_at) return ''
  const d = new Date(props.article.published_at)
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${m}/${day}`
})
</script>
