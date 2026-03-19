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
        <div class="blog-content" v-html="article.content_html" ref="contentRef"></div>
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
    <Sidebar
      mode="toc"
      :toc-items="tocItems"
      :active-toc-index="activeTocIndex"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import type { ArticleDetail, ArticleNav, TocItem } from '../types'
import TurnPage from '../components/article/TurnPage.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArticle } from '../api/articles'
import { formatTime } from '../utils/time'

const route = useRoute()
const article = ref<ArticleDetail | null>(null)
const prevArticle = ref<ArticleNav | null>(null)
const nextArticle = ref<ArticleNav | null>(null)
const contentRef = ref<HTMLElement | null>(null)
const tocItems = ref<TocItem[]>([])
const activeTocIndex = ref(0)

function buildToc(): void {
  if (!contentRef.value) return
  const headings = contentRef.value.querySelectorAll('h1, h2, h3, h4, h5, h6')
  const items: TocItem[] = []
  headings.forEach((el, index) => {
    const id = `heading-${index + 1}`
    el.id = id
    items.push({
      title: el.textContent || '',
      pos: id,
      level: parseInt(el.tagName.substring(1))
    })
  })
  tocItems.value = items
  if (items.length > 0) {
    activeTocIndex.value = 0
  }
}

function handleScroll(): void {
  if (tocItems.value.length === 0) return
  let currentIndex = 0
  for (let i = 0; i < tocItems.value.length; i++) {
    const el = document.getElementById(tocItems.value[i].pos)
    if (el && window.scrollY >= el.offsetTop - 100) {
      currentIndex = i
    }
  }
  activeTocIndex.value = currentIndex
}

async function fetchArticle(id: number | string): Promise<void> {
  try {
    const res = await getArticle(id)
    article.value = res.data
    prevArticle.value = res.data.prev_article || null
    nextArticle.value = res.data.next_article || null
    // 构建目录
    await nextTick()
    buildToc()
  } catch (e) {
    console.error('获取文章失败', e)
  }
}

onMounted(() => {
  fetchArticle(route.params.id as string)
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

watch(() => route.params.id, (newId) => {
  if (newId) fetchArticle(newId as string)
})
</script>
