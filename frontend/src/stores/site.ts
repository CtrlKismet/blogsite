import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/index'

export const useSiteStore = defineStore('site', () => {
  const siteTitle = ref('CtrlKismet\'s Blog')
  const siteDescription = ref('')

  async function fetchSiteInfo(): Promise<void> {
    try {
      const res = await api.get('/site/info')
      if (res.data) {
        siteTitle.value = res.data.site_title || siteTitle.value
        siteDescription.value = res.data.site_description || ''
      }
    } catch {
      // Use defaults on failure
    }
  }

  return { siteTitle, siteDescription, fetchSiteInfo }
})
