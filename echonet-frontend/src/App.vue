<template>
  <div class="min-vh-100" style="background-color: #100036;">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light border-bottom py-0 px-4" style="background-color: #350775;">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold fs-4 text-white" href="/feed">
          <img src="@/assets/logo.png" alt="Echonet Logo" width="150px" height="20%" class="d-inline-block align-text-top logo">
        </a>

        <div class="d-none d-lg-flex gap-4 mx-auto" v-if="userStore.user.isAuthenticated">
          <!-- HOME -->
          <RouterLink to="/feed" class="nav-link text-primary">
            <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#39ff65" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h-2l9 -9l9 9h-2" />
              <path d="M5 12v7a2 2 0 0 0 2 2h5" />
              <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2" />
              <path d="M19 22.5a4.75 4.75 0 0 1 3.5 -3.5a4.75 4.75 0 0 1 -3.5 -3.5a4.75 4.75 0 0 1 -3.5 3.5a4.75 4.75 0 0 1 3.5 3.5" />
            </svg>
          </RouterLink>

          <!-- DESCUBRIR MUSICA -->
          <RouterLink to="/discover" class="nav-link text-light">
            <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#39ff65" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
              <path d="M12 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" />
              <path d="M7 12a5 5 0 0 1 5 -5" />
              <path d="M12 17a5 5 0 0 0 5 -5" />
            </svg>
          </RouterLink>

          <!-- NOTIFICACIONES -->
          <RouterLink to="/notifications" class="nav-link text-light position-relative">
            <span v-if="hasUnreadNotifications" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 0.5rem; padding: 0.25em 0.4em;">!</span>
              <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#39ff65" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 5a2 2 0 0 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6" />
                <path d="M9 17v1a3 3 0 0 0 6 0v-1" />
              </svg>
          </RouterLink>

          <!-- BUSCAR -->
          <RouterLink to="/search" class="nav-link text-light">
            <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#39ff65" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 17a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />
              <path d="M9 17v-13h10v7" />
              <path d="M9 8h10" />
              <path d="M18 18m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" />
              <path d="M20.2 20.2l1.8 1.8" />
            </svg>
          </RouterLink>

          <!-- CHAT -->
          <RouterLink to="/chat" class="nav-link text-light">
            <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#39ff65" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 14l-3 -3h-7a1 1 0 0 1 -1 -1v-6a1 1 0 0 1 1 -1h9a1 1 0 0 1 1 1v10" />
              <path d="M14 15v2a1 1 0 0 1 -1 1h-7l-3 3v-10a1 1 0 0 1 1 -1h2" />
            </svg>
          </RouterLink>
        </div>

        <div class="d-flex align-items-center gap-3">
          <template v-if="userStore.user.isAuthenticated && userStore.user.id">
            <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }">
            <img
              v-if="userStore.user.avatar"
              :src="getAvatarUrl(userStore.user.avatar)"
              class="rounded-circle"
              style="width: 48px; height: 48px;"
            />            
          </RouterLink>
          </template>
          <template v-else>
            <RouterLink to="/signup" class="btn btn-primary">Acceder</RouterLink>
          </template>
        </div>
      </div>
    </nav>

    <main class="container py-2">
      <RouterView />
    </main>

    <Toast />
  </div>
</template>

<script>
import axios from 'axios'
import Toast from '@/components/Toast.vue'
import { useUserStore } from '@/stores/user'
import { onBeforeMount, onMounted, ref, onBeforeUnmount } from 'vue'

export default {
  components: {
    Toast
  },
  setup() {
    const userStore = useUserStore()
    const hasUnreadNotifications = ref(false)
    let pollInterval = null

    const getNotifications = () => {
      axios
        .get('api/notifications/')
        .then(response => {
          hasUnreadNotifications.value = response.data.length > 0
        })
        .catch(error => {
          console.log('Error al obtener notificaciones:', error)
        })
    }

    onBeforeMount(() => {
      userStore.initStore()
      const token = userStore.user.access
      axios.defaults.headers.common["Authorization"] = token ? "Bearer " + token : ""
      getNotifications()
    })

    onMounted(() => {
      // Actualiza cada 30 segundos
      pollInterval = setInterval(getNotifications, 5000)
    })

    onBeforeUnmount(() => {
      clearInterval(pollInterval)
    })

    return {
      userStore,
      hasUnreadNotifications
    }
  },
  methods: {
    getAvatarUrl(path) {
      return path.startsWith('http') ? path : `http://localhost:8000${path}` // BACKEND_URL
    }
  }
}
</script>