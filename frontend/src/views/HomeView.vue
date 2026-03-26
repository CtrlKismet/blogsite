<template>
  <div class="content">
    <main>
      <div class="filter" v-if="filterTag">
        {{ filterTag.name }} 的查询结果：
        <span class="remove-icon" @click="removeFilter"><i class="fa fa-remove"></i></span>
      </div>
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
      <div v-if="loading" style="text-align: center; padding: 2em; color: var(--color-text-light);">
        加载中...
      </div>
      <div v-else-if="articles.length === 0" style="text-align: center; padding: 2em; color: var(--color-text-light);">
        暂无文章
      </div>
      <div v-else-if="!hasMore" style="text-align: center; padding: 2em; color: var(--color-text-light);">
        已经到底啦 .◕ᴗ◕.
      </div>
    </main>
    <Sidebar
      mode="tags"
      :tags="tags"
      :active-tag="filterTag?.id"
      @tag-click="onTagClick"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { ArticleSummary, Tag } from '../types'
import ArticleCard from '../components/article/ArticleCard.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArticles } from '../api/articles'
import { getTags } from '../api/tags'

const articles = ref<ArticleSummary[]>([])
const tags = ref<Tag[]>([])
const filterTag = ref<Tag | null>(null)
const loading = ref(false)
const currentPage = ref(1)
const hasMore = ref(true)

async function fetchArticles(tagId: number | null = null, reset: boolean = true): Promise<void> {
  if (reset) {
    currentPage.value = 1
    hasMore.value = true
    articles.value = []
  }
  if (!hasMore.value || loading.value) return

  loading.value = true
  try {
    const params: { page: number; page_size: number; tag_id?: number } = { page: currentPage.value, page_size: 10 }
    if (tagId) params.tag_id = tagId
    const res = await getArticles(params)
    const items = res.data.items || []
    
    if (items.length < params.page_size) {
      hasMore.value = false
    }

    // 按 id 倒序排列
    items.sort((a, b) => b.id - a.id)
    
    if (reset) {
      articles.value = items
    } else {
      articles.value.push(...items)
    }
    currentPage.value++
  } catch (e) {
    console.error('获取文章列表失败', e)
  } finally {
    loading.value = false
  }
}

async function fetchTags(): Promise<void> {
  try {
    const res = await getTags()
    tags.value = res.data || []
  } catch (e) {
    console.error('获取标签失败', e)
  }
}

function onTagClick(tag: Tag): void {
  if (filterTag.value?.id === tag.id) {
    removeFilter()
    return
  }
  filterTag.value = tag
  fetchArticles(tag.id, true)
}

function removeFilter(): void {
  filterTag.value = null
  fetchArticles(null, true)
}

function handleScroll(): void {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement
  // 提前500px触发加载
  if (scrollTop + clientHeight >= scrollHeight - 500) {
    if (!loading.value && hasMore.value) {
      fetchArticles(filterTag.value?.id || null, false)
    }
  }
}

onMounted(() => {
  fetchArticles()
  fetchTags()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
