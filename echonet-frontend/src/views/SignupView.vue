<template>
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center" style="background: linear-gradient(to right, #290642, #580F78, #B346DB);">
    <div class="row w-75 shadow rounded overflow-hidden" style="max-width: 900px;">

      <div class="col-md-6 text-white d-flex flex-column justify-content-center p-5" style="background-color: #580F78;">
        <h2 class="mb-3">Huola</h2>
        <p class="mb-5">Accede mediante tu cuenta de Spotify</p>
        <small class="mt-auto">trincame el pepino</small>
      </div>

      <!-- Lado derecho -->
      <div class="col-md-6 bg-white d-flex flex-column justify-content-center p-5 text-center">
        <h3 class="mb-4 text-black">¿Ya tienes una cuenta?</h3>
        <button @click="goToExternalLogin" class="btn w-100 text-white" style="background-color: #15CE00;">
          Iniciar sesión
        </button>
      </div>

    </div>
  </div>
</template>
<script>
import axios from "@/utils/axios"
import { useUserStore } from '@/stores/user'

export default {
  mounted() {
    const url = new URL(window.location.href);

    const access = url.searchParams.get("access");
    const refresh = url.searchParams.get("refresh");
    const id = url.searchParams.get("id");
    const name = url.searchParams.get("display_name");
    const email = url.searchParams.get("email");
    const avatar = url.searchParams.get("avatar");

    if (access && refresh) {
      const userStore = useUserStore();

      userStore.setToken({
        access,
        refresh,
      });

      userStore.setUserInfo({
        id,
        name,
        email,
        avatar,
      });

      // Aquí configuras Axios con el token recién recibido
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;

      // Limpias la URL para que no se queden los tokens
      window.history.replaceState({}, document.title, "/signup");

      // Guardas en localStorage por si se recarga la página
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      // Rediriges al feed
      this.$router.push("/feed");
    }

      // Si no hay token, lo quitas de localStorage
      if (!access) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
  },
  methods: {
    goToExternalLogin() {
      window.location.href = 'http://localhost:8000/api/spotify/login/'
    },
    getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift())
      return null
    }
  },

  methods: {
    goToExternalLogin() {
      window.location.href = 'http://localhost:8000/api/spotify/login/'
    }
  }
}
</script>