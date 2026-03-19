<template>
  <div class="blog-archive">
    <div class="archive-header">
      <span></span>
      <span class="archive-year">{{ year }}</span>
      <span>{{ articles.length }} 篇</span>
    </div>
    <div class="archive-content">
      <div
        class="blog-detail"
        v-for="article in articles"
        :key="article.id"
      >
        <span class="archive-points">●</span>
        <div class="blog-ellipsis ellipsis">
          <router-link :to="`/blog/${article.id}`">
            {{ article.title }}
          </router-link>
        </div>
        <div class="blog-time">{{ formatDate(article.published_at) }}</div>
      </div>
    </div>
    <div class="archive-footer"></div>
  </div>
</template>

<script setup lang="ts">
import type { ArchiveArticle } from '../../types'

defineProps<{
  year: string | number
  articles: ArchiveArticle[]
}>()

function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return (d.getMonth() + 1) + '-' + d.getDate()
}
</script>
