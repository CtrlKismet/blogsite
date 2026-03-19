<template>
  <div class="turn-page">
    <div class="pre" v-if="prev" @click="$router.push(`/blog/${prev.id}`)">
      <i>←</i>
      <span class="ellipsis">{{ prev.title }}</span>
    </div>
    <div class="pre" v-else></div>
    <div class="nxt" v-if="next" @click="$router.push(`/blog/${next.id}`)">
      <span class="ellipsis">{{ next.title }}</span>
      <i>→</i>
    </div>
    <div class="nxt" v-else></div>
  </div>
</template>

<script setup>
defineProps({
  prev: {
    type: Object,
    default: null
  },
  next: {
    type: Object,
    default: null
  }
})
</script>
