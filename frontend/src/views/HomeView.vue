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
      <div v-if="articles.length === 0 && !loading" style="text-align: center; padding: 2em;">
        暂无文章
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
import { ref, onMounted } from 'vue'
import type { ArticleSummary, Tag } from '../types'
import ArticleCard from '../components/article/ArticleCard.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArticles } from '../api/articles'
import { getTags } from '../api/tags'

const articles = ref<ArticleSummary[]>([])
const tags = ref<Tag[]>([])
const filterTag = ref<Tag | null>(null)
const loading = ref(false)

async function fetchArticles(tagId: number | null = null): Promise<void> {
  loading.value = true
  try {
    const params: { page: number; page_size: number; tag_id?: number } = { page: 1, page_size: 20 }
    if (tagId) params.tag_id = tagId
    const res = await getArticles(params)
    const items = res.data.items || []
    // 按 id 倒序排列
    items.sort((a, b) => b.id - a.id)
    articles.value = items
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
  fetchArticles(tag.id)
}

function removeFilter(): void {
  filterTag.value = null
  fetchArticles()
}

onMounted(() => {
  fetchArticles()
  fetchTags()
})
</script>
