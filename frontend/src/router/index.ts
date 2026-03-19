import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/archive',
    name: 'Archive',
    component: () => import('../views/ArchiveView.vue'),
    meta: { title: '归档' }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue'),
    meta: { title: '关于' }
  },
  {
    path: '/blog/:id',
    name: 'BlogDetail',
    component: () => import('../views/BlogDetailView.vue'),
    meta: { title: '文章详情' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/admin/new',
    name: 'NewArticle',
    component: () => import('../views/admin/EditorView.vue'),
    meta: { title: '新建文章', requiresAuth: true }
  },
  {
    path: '/admin/edit/:id',
    name: 'EditArticle',
    component: () => import('../views/admin/EditorView.vue'),
    meta: { title: '编辑文章', requiresAuth: true }
  },
  {
    path: '/admin/edit/about',
    name: 'EditAbout',
    component: () => import('../views/admin/EditorView.vue'),
    meta: { title: '编辑关于', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

// 路由守卫：认证检查
router.beforeEach((to, from, next) => {
  // 更新页面标题
  document.title = to.meta.title
    ? `${to.meta.title} - Blog`
    : 'Blog'

  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  next()
})

export default router
