<template>
  <LoadingPage ref="loadingRef" />
  <div class="main-page">
    <NavBar />
    <router-view v-slot="{ Component }">
      <transition name="content-fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import LoadingPage from './components/common/LoadingPage.vue'
import NavBar from './components/layout/NavBar.vue'
import Footer from './components/layout/Footer.vue'
</script>
