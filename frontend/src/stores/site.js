import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSiteStore = defineStore('site', () => {
  const siteTitle = ref('CtrlKismet\'s Blog')
  const siteDescription = ref('')

  return { siteTitle, siteDescription }
})
