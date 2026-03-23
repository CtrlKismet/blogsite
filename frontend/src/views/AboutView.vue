<template>
  <div class="content">
    <main>
      <div class="blog about" v-if="article">
        <div class="blog-header">
          <div class="blog-title">{{ article.title }}</div>
        </div>
        <div class="blog-content" v-html="article.content_html" ref="contentRef"></div>
        <div class="blog-footer">
          <span class="modified-time" v-if="article.updated_at">
            最后修改于 {{ formatTime(article.updated_at) }}
          </span>
        </div>
      </div>
      <div v-else-if="!loading" style="text-align: center; padding: 2em;">
        About 页面暂未配置
      </div>
    </main>
    <Sidebar
      mode="toc"
      :toc-items="tocItems"
      :active-toc-index="activeTocIndex"
      :show-avatar="true"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import type { AboutArticle, TocItem } from '../types'
import Sidebar from '../components/layout/Sidebar.vue'
import { getAbout } from '../api/articles'
import { formatTime } from '../utils/time'
import { renderMath } from '../utils/math'

const article = ref<AboutArticle | null>(null)
const loading = ref(false)
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

async function fetchAbout(): Promise<void> {
  loading.value = true
  try {
    const res = await getAbout()
    article.value = res.data
    await nextTick()
    buildToc()
    if (contentRef.value) renderMath(contentRef.value)
  } catch (e) {
    console.error('获取 About 页面失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAbout()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
