<template>
  <div class="clock">
    <div class="time-num" :style="{ transform: transforms[0] }">{{ digits[0] }}</div>
    <div class="time-num" :style="{ transform: transforms[1] }">{{ digits[1] }}</div>
    <span>:</span>
    <div class="time-num" :style="{ transform: transforms[2] }">{{ digits[2] }}</div>
    <div class="time-num" :style="{ transform: transforms[3] }">{{ digits[3] }}</div>
    <span>:</span>
    <div class="time-num" :style="{ transform: transforms[4] }">{{ digits[4] }}</div>
    <div class="time-num" :style="{ transform: transforms[5] }">{{ digits[5] }}</div>
  </div>
</template>

<script setup lang="ts">
/**
 * Clock 组件 — 保留原有翻转缩放动画
 * 6 个数字格 + 2 个冒号分隔符
 * 布局通过 CSS grid 实现（见 components.css aside .clock）
 */
import { ref, onMounted, onUnmounted } from 'vue'

const fade: string[] = ['scale(0,0)', 'scale(1,1)']
const digits = ref<string[]>(['0', '0', '0', '0', '0', '0'])
const transforms = ref<string[]>([
  'scale(1,1)', 'scale(1,1)', 'scale(1,1)',
  'scale(1,1)', 'scale(1,1)', 'scale(1,1)'
])

const cnt: number[] = [0, 0, 0, 0, 0, 0]
const number: string[] = ['-1', '-1', '-1', '-1', '-1', '-1']
let intervalId: ReturnType<typeof setInterval> | null = null

function refreshTime(): void {
  const timeNow = new Date()
    .toTimeString()
    .substring(0, 8)
    .replace(/:/g, '')

  for (let i = 0; i < 6; i++) {
    if (timeNow[i] === number[i]) continue
    cnt[i] = (cnt[i] + 1) % 2
    if (cnt[i] !== 0) {
      digits.value[i] = timeNow[i]
      number[i] = timeNow[i]
    }
    transforms.value[i] = fade[cnt[i]]
  }
}

function startClock(): void {
  // 立即显示当前时间，避免初始 00:00:00
  const timeNow = new Date().toTimeString().substring(0, 8).replace(/:/g, '')
  for (let i = 0; i < 6; i++) {
    digits.value[i] = timeNow[i]
    number[i] = timeNow[i]
  }
  if (!intervalId) {
    intervalId = setInterval(refreshTime, 500)
  }
}

function stopClock(): void {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

defineExpose({ startClock, stopClock })

onMounted(() => {
  startClock()
})

onUnmounted(() => {
  stopClock()
})
</script>
