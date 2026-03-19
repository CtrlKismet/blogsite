<template>
  <div class="content">
    <main>
      <div class="blog" v-if="article">
        <!-- 头图 -->
        <div class="blog-header-image" v-if="article.header_image">
          <img :src="article.header_image" :alt="article.title" style="width: 100%; border-radius: 7px 7px 0 0;" />
        </div>
        <div class="blog-header">
          <div class="blog-title">{{ article.title }}</div>
          <div class="tag-list">
            标签：
            <span class="tag" v-for="tag in article.tags" :key="tag.id">
              {{ tag.name }}
            </span>
          </div>
        </div>
        <div class="blog-content" v-html="article.content_html"></div>
        <div class="blog-footer">
          <span>发布于 {{ formatTime(article.published_at) }}</span>
          <span class="modified-time" v-if="article.updated_at">
            最后修改于 {{ formatTime(article.updated_at) }}
          </span>
        </div>
      </div>

      <TurnPage :prev="prevArticle" :next="nextArticle" />

      <!-- Artalk 评论区占位 -->
      <div id="artalk-comment"></div>
    </main>
    <Sidebar :tags="[]" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import TurnPage from '../components/article/TurnPage.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArticle } from '../api/articles'
import { formatTime } from '../utils/time'

const route = useRoute()
const article = ref(null)
const prevArticle = ref(null)
const nextArticle = ref(null)

async function fetchArticle(id) {
  try {
    const res = await getArticle(id)
    article.value = res.data
    // TODO: 获取上下篇信息（后端提供）
  } catch (e) {
    console.error('获取文章失败', e)
  }
}

onMounted(() => {
  fetchArticle(route.params.id)
})

watch(() => route.params.id, (newId) => {
  if (newId) fetchArticle(newId)
})
</script>
