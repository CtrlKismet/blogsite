<template>
  <div class="blog-archive">
    <div class="archive-header">
      <svg class="year-marker" width="14" height="14" viewBox="0 0 14 14">
        <circle cx="7" cy="7" r="5" fill="var(--color-primary)" stroke="var(--color-secondary-solid)" stroke-width="2"/>
      </svg>
      <span class="archive-year">{{ year }}</span>
      <span class="archive-count">{{ articles.length }} 篇</span>
    </div>
    <div class="archive-content">
      <div
        class="blog-detail"
        v-for="article in articles"
        :key="article.id"
      >
        <span class="archive-dot">
          <svg width="10" height="10" viewBox="0 0 10 10">
            <circle cx="5" cy="5" r="3.5" fill="var(--dot-fill, var(--color-card))" stroke="currentColor" stroke-width="1.5"/>
          </svg>
        </span>
        <div class="blog-ellipsis ellipsis">
          <router-link :to="`/blog/${article.id}`">
            {{ article.title }}
          </router-link>
        </div>
        <div class="blog-time">{{ formatDate(article.published_at) }}</div>
      </div>
    </div>
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
