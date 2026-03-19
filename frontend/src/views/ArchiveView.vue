<template>
  <div class="content">
    <main>
      <ArchiveGroup
        v-for="group in archiveGroups"
        :key="group.year"
        :year="group.year"
        :articles="group.articles"
      />
      <div v-if="archiveGroups.length === 0 && !loading" style="text-align: center; padding: 2em;">
        暂无归档
      </div>
    </main>
    <Sidebar mode="none" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { ArchiveGroup as ArchiveGroupType } from '../types'
import ArchiveGroup from '../components/archive/ArchiveGroup.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import { getArchive } from '../api/articles'

const archiveGroups = ref<ArchiveGroupType[]>([])
const loading = ref(false)

async function fetchArchive(): Promise<void> {
  loading.value = true
  try {
    const res = await getArchive()
    archiveGroups.value = res.data || []
  } catch (e) {
    console.error('获取归档失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchArchive()
})
</script>
