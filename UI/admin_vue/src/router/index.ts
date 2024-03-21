import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import editMenu from '../views/editMenu.vue'
import articleLists from '../views/articleLists.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:id/:language/:country',
    name: 'edit',
    component: editMenu
  },
  {
    path: '/page/list',
    name: 'page',
    component: articleLists
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
