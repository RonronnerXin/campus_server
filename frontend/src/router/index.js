import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/login.vue'
import Register from '../views/register.vue'
import LostFound from '../views/lostitem.vue'
import Community from '../views/Community.vue'
import PublishItem from '../views/PublishItem.vue'
import PostList from '../components/PostList.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    children: [
      {
        path: '',
        name: 'PostList',
        component: PostList
      },
      {
        path: 'lost-found',
        name: 'LostFound',
        component: LostFound
      },
      {
        path: 'community',
        name: 'Community',
        component: Community
      },
      {
        path: 'publish',
        name: 'PublishItem',
        component: PublishItem
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router