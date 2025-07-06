import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Game from '@/views/Game.vue'
import CabinDemo from '@/views/CabinDemo.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '🚢 全民航海求生游戏'
    }
  },
  {
    path: '/game',
    name: 'Game',
    component: Game,
    meta: {
      title: '游戏中 - 航海求生'
    }
  },
  {
    path: '/cabin-demo',
    name: 'CabinDemo',
    component: CabinDemo,
    meta: {
      title: '船舱环境演示 - 航海求生'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 更新页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '航海求生游戏'
  next()
})

export default router 