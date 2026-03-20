import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

import './styles/global.css'
import './styles/layout.css'
import './styles/components.css'
import './styles/responsive.css'
import 'katex/dist/katex.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

import { initVisibility } from './utils/visibility'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')

// 页面可见性切换（标题 + Favicon）
initVisibility()
