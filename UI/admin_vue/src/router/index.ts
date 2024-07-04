import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import editMenu from '../views/editMenu.vue'
import articleLists from '../views/articleLists.vue'
import categoryList from '../views/categoryList.vue'
import categoryDetail from '../views/categoryDetail.vue'

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
  },
  {
    path: '/category/:country',
    name: 'category_list',
    component: categoryList
  },
  {
    path: '/category/:country/:cat_id',
    name: 'category_detail',
    component: categoryDetail
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
