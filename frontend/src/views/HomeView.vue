<template>
  <div class="content">
    <main>
      <div class="filter-bar" v-if="filterTag || filterYear !== null" aria-label="当前筛选">
        <span class="filter-bar-label">筛选</span>
        <span class="filter-chip" v-if="filterTag">
          <i class="fa fa-tag" aria-hidden="true"></i>
          <span class="filter-chip-text">{{ filterTag.name }}</span>
          <button
            class="filter-chip-remove"
            type="button"
            :aria-label="`取消标签 ${filterTag.name} 筛选`"
            @click="removeTagFilter"
          ><i class="fa fa-times" aria-hidden="true"></i></button>
        </span>
        <span class="filter-chip" v-if="filterYear !== null">
          <i class="fa fa-calendar" aria-hidden="true"></i>
          <span class="filter-chip-text">{{ filterYear }} 年</span>
          <button
            class="filter-chip-remove"
            type="button"
            :aria-label="`取消 ${filterYear} 年筛选`"
            @click="removeYearFilter"
          ><i class="fa fa-times" aria-hidden="true"></i></button>
        </span>
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
      <div ref="sentinelRef" style="height: 1px;"></div>
    </main>
    <Sidebar
      mode="tags"
      :tags="tags"
      :active-tag="filterTag?.id"
      :years="years"
      :active-year="filterYear"
      @tag-click="onTagClick"
      @year-click="onYearClick"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { ArticleSummary, Tag } from '../types'
import ArticleCard from '../components/article/ArticleCard.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArticles, getArchive, type ArticleListParams } from '../api/articles'
import { getTags } from '../api/tags'
import { parseFilterInteger } from '../utils/filters'

const route = useRoute()
const router = useRouter()
const articles = ref<ArticleSummary[]>([])
const tags = ref<Tag[]>([])
const filterTagId = computed(() => parseFilterInteger(route.query.tag_id))
const filterTag = computed<Tag | null>(() => {
  const id = filterTagId.value
  if (id === null) return null
  return tags.value.find((tag) => tag.id === id) || { id, name: `标签 #${id}` }
})
const years = ref<number[]>([])
const filterYear = computed(() => parseFilterInteger(route.query.year, 9999))
const loading = ref(false)
const currentPage = ref(1)
const hasMore = ref(true)
const sentinelRef = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null
let latestRequest = 0

async function fetchArticles(reset: boolean = true): Promise<void> {
  if (!reset && (!hasMore.value || loading.value)) return
  const request = ++latestRequest
  if (reset) {
    currentPage.value = 1
    hasMore.value = true
    articles.value = []
  }
  loading.value = true
  let succeeded = false
  try {
    const params: ArticleListParams = { page: currentPage.value, page_size: 10 }
    if (filterTagId.value !== null) params.tag_id = filterTagId.value
    if (filterYear.value !== null) params.year = filterYear.value
    const res = await getArticles(params)
    if (request !== latestRequest) return
    const items = res.data.items || []
    hasMore.value = currentPage.value < res.data.total_pages

    // 按 id 倒序排列
    items.sort((a, b) => b.id - a.id)
    
    if (reset) {
      articles.value = items
    } else {
      articles.value.push(...items)
    }
    currentPage.value++
    succeeded = true
  } catch (e) {
    if (request === latestRequest) console.error('获取文章列表失败', e)
  } finally {
    if (request === latestRequest) {
      loading.value = false
      if (succeeded) nextTick(() => checkSentinel())
    }
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

async function fetchYears(): Promise<void> {
  try {
    const res = await getArchive()
    years.value = [...new Set((res.data || []).map((group) => group.year))].sort((a, b) => b - a)
  } catch (e) {
    console.error('获取年份失败', e)
  }
}

function setFilters(tagId: number | null, year: number | null): void {
  const query = { ...route.query }
  delete query.tag_id
  delete query.year
  if (tagId !== null) query.tag_id = String(tagId)
  if (year !== null) query.year = String(year)
  void router.push({ path: route.path, query, hash: route.hash })
}

function onTagClick(tag: Tag): void {
  setFilters(filterTagId.value === tag.id ? null : tag.id, filterYear.value)
}

function removeTagFilter(): void {
  setFilters(null, filterYear.value)
}

function onYearClick(year: number): void {
  setFilters(filterTagId.value, filterYear.value === year ? null : year)
}

function removeYearFilter(): void {
  setFilters(filterTagId.value, null)
}

function handleScroll(): void {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement
  // 提前500px触发加载
  if (scrollTop + clientHeight >= scrollHeight - 500) {
    if (!loading.value && hasMore.value) {
      fetchArticles(false)
    }
  }
}

function setupObserver(): void {
  if (observer) observer.disconnect()
  if (!sentinelRef.value) return
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !loading.value && hasMore.value) {
      fetchArticles(false)
    }
  }, { rootMargin: '500px' })
  observer.observe(sentinelRef.value)
}

function checkSentinel(): void {
  if (!sentinelRef.value || loading.value || !hasMore.value) return
  const rect = sentinelRef.value.getBoundingClientRect()
  if (rect.top < window.innerHeight + 500) {
    fetchArticles(false)
  }
}

onMounted(() => {
  fetchTags()
  fetchYears()
  window.addEventListener('scroll', handleScroll)
})

watch([filterTagId, filterYear], () => {
  if (route.name === 'Home') fetchArticles()
}, { immediate: true })

watch(sentinelRef, (el) => {
  if (el) setupObserver()
})

onUnmounted(() => {
  latestRequest++
  window.removeEventListener('scroll', handleScroll)
  if (observer) observer.disconnect()
})
</script>
