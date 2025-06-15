import { createRouter, createWebHistory } from 'vue-router'
import SignupView from '@/views/SignupView.vue'
import HomeView from '@/views/HomeView.vue'
import FeedView from '../views/FeedView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import TrendView from '../views/TrendView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import DiscoverMusic from '@/views/DiscoverMusic.vue'

const routes = [
  {
    path: '/signup',
    name: 'Signup',
    component: SignupView
  },
  {
    path: '/',
    name: 'SignupRedirect',
    redirect: '/signup',
  },
  {
    path: '/feed',
    name: 'feed',
    component: FeedView
  },
  {
    path: '/discover',
    name: 'discover',
    component: DiscoverMusic
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatView
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: NotificationsView
  },
  {
    path: '/profile/edit',
    name: 'editprofile',
    component: EditProfileView
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/profile/:id/friends',
    name: 'friends',
    component: FriendsView
  },
  {
    path: '/:id',
    name: 'postview',
    component: PostView
  },
  {
    path: '/trends/:id',
    name: 'trendview',
    component: TrendView
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Guard global de autenticación
router.beforeEach((to, from, next) => {
  // Aquí asume que el token de autenticación está en localStorage
  const isAuthenticated = !!localStorage.getItem('user.access')
  if (!isAuthenticated && to.path !== '/signup') {
    next('/signup')
  } else if (isAuthenticated && to.path === '/signup') {
    next('/') // Opcional: redirige a home si ya está autenticado
  } else {
    next()
  }
})

export default router