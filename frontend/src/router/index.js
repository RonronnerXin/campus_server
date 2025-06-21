import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/login.vue'
import Register from '../views/register.vue'
import LostFound from '../views/lostitem.vue'
import Community from '../views/Community.vue'
import PublishItem from '../views/PublishItem.vue'
import PublishPost from '../views/PublishPost.vue'
import PostList from '../components/PostList.vue'
import LostItemDetail from '../views/itemdetail.vue'
import PostDetail from '../views/blogdetail.vue'
import Profile from '../views/profile.vue'
import BlogEditor from '../views/blogeditor.vue'
import LostItemEditor from '../views/lostitemeditor.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    children: [
      {
        path: '', // 默认子路由
        name: 'LostFound',
        component: LostFound
      },
      {
        path: 'lost-found', // 保留这个路由
        redirect: '/' // 重定向到根路径
      },
      {
        path: 'community',
        name: 'Community',
        component: Community
      },
      {
        path: 'publishItem',
        name: 'PublishItem',
        component: PublishItem
      },
      {
        path: 'publishPost',
        name: 'PublishPost',
        component: PublishPost
      },
      {
        path: 'lostitemdetail/:id',
        name: 'LostItemDetail',
        component: LostItemDetail
      },
      {
        path: 'blogdetail/:id',
        name: 'PostDetail',
        component: PostDetail
      },
      {
        path: 'profile',
        name: 'profile',
        component: Profile
      },
        {
        path: '/blog/edit/:id',
        name: 'EditBlog',
        component: BlogEditor,
      },
        {
        path: '/lost-found/edit/:id',
        name: 'EditLostItem',
        component: LostItemEditor,
      },
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