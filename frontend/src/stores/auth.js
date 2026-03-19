import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, verify as apiVerify } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const isAuthenticated = computed(() => !!token.value)

  async function login(username, password) {
    const res = await apiLogin(username, password)
    token.value = res.data.access_token
    localStorage.setItem('token', token.value)
    return res
  }

  async function checkAuth() {
    if (!token.value) return false
    try {
      await apiVerify()
      return true
    } catch {
      logout()
      return false
    }
  }

  function logout() {
    token.value = ''
    localStorage.removeItem('token')
  }

  return { token, isAuthenticated, login, checkAuth, logout }
})
