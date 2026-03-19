<template>
  <div class="content">
    <main>
      <div class="newblog">
        <div class="blog-prop">
          <p>标题</p>
          <input v-model="form.title" type="text" placeholder="文章标题" />
        </div>

        <div class="blog-prop">
          <p>摘要</p>
          <textarea v-model="form.summary" rows="3" placeholder="文章摘要"></textarea>
        </div>

        <div class="blog-prop">
          <p>头图 URL</p>
          <input v-model="form.header_image" type="text" placeholder="可选，文章详情页顶部展示图" />
        </div>

        <div class="blog-prop">
          <p>标签</p>
          <div class="tag-list">
            <span
              class="tag"
              v-for="tag in allTags"
              :key="tag.id"
              :style="{
                backgroundColor: selectedTags.includes(tag.id)
                  ? 'rgba(255, 203, 83, 0.6)'
                  : '#d4d4d4'
              }"
              @click="toggleTag(tag.id)"
            >
              <label>{{ tag.name }}</label>
            </span>
          </div>
        </div>

        <div class="blog-prop">
          <p>内容</p>
          <!-- Markdown 编辑器占位，后续集成 -->
          <textarea
            v-model="form.content"
            rows="20"
            placeholder="Markdown 内容"
            style="font-family: monospace; font-size: .8em;"
          ></textarea>
        </div>

        <button type="button" @click="handleSubmit">
          {{ isEdit ? '更新文章' : '发布文章' }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Tag, ArticleForm } from '../../types'
import { getTags } from '../../api/tags'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => {
  return route.name === 'EditArticle' || route.name === 'EditAbout'
})

const form = ref<ArticleForm>({
  title: '',
  summary: '',
  header_image: '',
  content: ''
})

const allTags = ref<Tag[]>([])
const selectedTags = ref<number[]>([])

function toggleTag(tagId: number): void {
  const idx = selectedTags.value.indexOf(tagId)
  if (idx >= 0) {
    selectedTags.value.splice(idx, 1)
  } else {
    selectedTags.value.push(tagId)
  }
}

async function fetchTags(): Promise<void> {
  try {
    const res = await getTags()
    allTags.value = res.data || []
  } catch (e) {
    console.error('获取标签失败', e)
  }
}

async function handleSubmit(): Promise<void> {
  // TODO: 调用后端 API 创建/更新文章
  console.log('提交文章', {
    ...form.value,
    tag_ids: selectedTags.value
  })
}

onMounted(() => {
  fetchTags()
  // TODO: 编辑模式下加载已有文章数据
})
</script>
