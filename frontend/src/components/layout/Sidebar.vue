<template>
  <aside>
    <!-- About 页显示头像 -->
    <div class="sculptrue" v-if="showAvatar">
      <img src="/images/head.jpg" alt="avatar" />
    </div>
    <Clock />
    <div class="date-display">{{ dateStr }}</div>
    <hr />
    <!-- 目录模式（博客详情页） -->
    <div class="menu-list" id="list_of_menu" v-if="mode === 'toc' && (tocItems ?? []).length > 0">
      <div class="list-title">目录</div>
      <div
        class="list-item"
        :class="{ 'list-item-active': activeTocIndex === index }"
        v-for="(item, index) in tocItems"
        :key="item.pos"
      >
        <a :href="'#' + item.pos" @click.prevent="scrollToHeading(item.pos)">{{ item.title }}</a>
      </div>
    </div>
    <!-- 标签模式（首页） -->
    <div class="tag-list" id="list_of_tags" v-if="mode === 'tags'">
      <div class="list-title">标签</div>
      <div
        class="list-item"
        :class="{ 'list-item-active': activeTag === tag.id }"
        v-for="tag in tags"
        :key="tag.id"
      >
        <a @click="$emit('tagClick', tag)">{{ tag.name }}</a>
      </div>
    </div>
    <TopRocket />
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Tag, TocItem } from '../../types'
import Clock from '../common/Clock.vue'
import TopRocket from '../common/TopRocket.vue'

const props = defineProps<{
  tags?: Tag[]
  activeTag?: number | null
  mode?: 'tags' | 'toc' | 'none'
  tocItems?: TocItem[]
  activeTocIndex?: number
  showAvatar?: boolean
}>()

defineEmits<{
  tagClick: [tag: Tag]
}>()

const chznDay: string[] = ['日', '一', '二', '三', '四', '五', '六']
const dateStr = ref('')

function updateDate(): void {
  const now = new Date()
  dateStr.value =
    now.getFullYear() + '/' +
    (now.getMonth() + 1) + '/' +
    now.getDate() + '     ' +
    '星期' + chznDay[now.getDay()]
}

function scrollToHeading(pos: string): void {
  const el = document.getElementById(pos)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  updateDate()
})
</script>
