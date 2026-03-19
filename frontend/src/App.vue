<template>
  <LoadingPage ref="loadingRef" />
  <div class="main-page">
    <NavBar />
    <router-view />
    <Footer />
  </div>
</template>

<script setup>
import LoadingPage from './components/common/LoadingPage.vue'
import NavBar from './components/layout/NavBar.vue'
import Footer from './components/layout/Footer.vue'
</script>
