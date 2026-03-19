<template>
  <aside>
    <Clock />
    <div class="date-display">{{ dateStr }}</div>
    <hr />
    <div class="tag-list" id="list_of_tags">
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

<script setup>
import { ref, onMounted } from 'vue'
import Clock from '../common/Clock.vue'
import TopRocket from '../common/TopRocket.vue'

defineProps({
  tags: {
    type: Array,
    default: () => []
  },
  activeTag: {
    type: Number,
    default: null
  }
})

defineEmits(['tagClick'])

const chznDay = ['日', '一', '二', '三', '四', '五', '六']
const dateStr = ref('')

function updateDate() {
  const now = new Date()
  dateStr.value =
    now.getFullYear() + '/' +
    (now.getMonth() + 1) + '/' +
    now.getDate() + '     ' +
    '星期' + chznDay[now.getDay()]
}

onMounted(() => {
  updateDate()
})
</script>
