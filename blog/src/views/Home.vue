<template>
  <HeadbarVue />
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
  </div>
</template>

<script>
import HeadbarVue from '../components/Headbar.vue';

export default {
  name:"layout",
  components: {
    HeadbarVue
  }
}
</script>
