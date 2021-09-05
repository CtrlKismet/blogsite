import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/css/global.css'
import './assets/css/font-awesome-4.7.0.min.css' // https://cdnjs.loli.net/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css

createApp(App).use(store).use(router).mount('#app')
