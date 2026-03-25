<template>
  <div class="main-page">
    <NavBar />
    <div class="page-body">
      <router-view v-slot="{ Component }">
        <transition name="content-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import NavBar from './components/layout/NavBar.vue'
import Footer from './components/layout/Footer.vue'
</script>
