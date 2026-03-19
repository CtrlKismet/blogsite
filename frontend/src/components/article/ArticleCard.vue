<template>
  <div class="article-card">
    <div class="time-stamp">
      <p>{{ year }}</p>
      <hr />
      <p>{{ monthDay }}</p>
    </div>
    <router-link :to="`/blog/${article.id}`" class="art-content">
      <div class="art-title ellipsis">{{ article.title }}</div>
      <div class="art-ellipsis">{{ article.summary }}</div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ArticleSummary } from '../../types'

const props = defineProps<{
  article: ArticleSummary
}>()

const year = computed((): string | number => {
  if (!props.article.published_at) return ''
  const d = new Date(props.article.published_at)
  return d.getFullYear()
})

const monthDay = computed((): string => {
  if (!props.article.published_at) return ''
  const d = new Date(props.article.published_at)
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${m}/${day}`
})
</script>
