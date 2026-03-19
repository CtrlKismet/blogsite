<template>
  <div class="content" style="justify-content: center;">
    <main style="max-width: 400px;">
      <div class="blog" style="padding: 40px 30px;">
        <h2 style="text-align: center; margin-bottom: 1em;">登录</h2>
        <form @submit.prevent="handleLogin">
          <div class="blog-prop">
            <input
              v-model="username"
              type="text"
              placeholder="用户名"
              autocomplete="username"
            />
          </div>
          <div class="blog-prop">
            <input
              v-model="password"
              type="password"
              placeholder="密码"
              autocomplete="current-password"
            />
          </div>
          <div v-if="error" style="color: red; font-size: .7em; padding: 5px;">
            {{ error }}
          </div>
          <button
            type="submit"
            style="width: 100%; padding: 10px; margin-top: 15px; font-size: .9em;
                   border-radius: 5px; background-color: #fad070; border: 1px solid #ccc;
                   cursor: pointer; color: rgb(91, 40, 11);"
          >
            登录
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    const redirect = route.query.redirect || '/admin/new'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败'
  }
}
</script>
