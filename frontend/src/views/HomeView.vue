<template>
  <div class="content">
    <main>
      <div class="filter" v-if="filterTag">
        {{ filterTag.name }} 的查询结果：
        <span class="remove-icon" @click="removeFilter">✕</span>
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
      :tags="tags"
      :active-tag="filterTag?.id"
      @tag-click="onTagClick"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ArticleCard from '../components/article/ArticleCard.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArticles } from '../api/articles'
import { getTags } from '../api/tags'

const articles = ref([])
const tags = ref([])
const filterTag = ref(null)
const loading = ref(false)

async function fetchArticles(tagId = null) {
  loading.value = true
  try {
    const params = { page: 1, size: 20 }
    if (tagId) params.tag_id = tagId
    const res = await getArticles(params)
    articles.value = res.data.items || []
  } catch (e) {
    console.error('获取文章列表失败', e)
  } finally {
    loading.value = false
  }
}

async function fetchTags() {
  try {
    const res = await getTags()
    tags.value = res.data || []
  } catch (e) {
    console.error('获取标签失败', e)
  }
}

function onTagClick(tag) {
  if (filterTag.value?.id === tag.id) {
    removeFilter()
    return
  }
  filterTag.value = tag
  fetchArticles(tag.id)
}

function removeFilter() {
  filterTag.value = null
  fetchArticles()
}

onMounted(() => {
  fetchArticles()
  fetchTags()
})
</script>
