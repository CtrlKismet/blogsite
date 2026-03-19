<template>
  <div class="turn-page">
    <div class="pre" v-if="prev" @click="$router.push(`/blog/${prev.id}`)">
      <i>←</i>
      <span>上一篇</span>
      <span class="ellipsis">{{ prev.title }}</span>
    </div>
    <div class="pre" v-else></div>
    <div class="nxt" v-if="next" @click="$router.push(`/blog/${next.id}`)">
      <span>下一篇</span>
      <span class="ellipsis">{{ next.title }}</span>
      <i>→</i>
    </div>
    <div class="nxt" v-else></div>
  </div>
</template>

<script setup lang="ts">
import type { ArticleNav } from '../../types'

defineProps<{
  prev?: ArticleNav | null
  next?: ArticleNav | null
}>()
</script>
