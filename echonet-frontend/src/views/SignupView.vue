<template>
  <div class="d-flex overflow-hidden" style="height: 90vh;">

    <!-- Lado izquierdo - Visual musical -->
    <div class="col-md-6 d-none d-md-flex flex-column justify-content-center align-items-center text-white position-relative" :style="{ backgroundImage: `url(${fondoUrl})` }">
      <div class="text-center p-4 bg-white bg-opacity-25 rounded-3" style="max-width: 500px; backdrop-filter: blur(10px); color: #9CFF90;">
        <p class="lead "> Descubre personas que resuenen con tu música y la música que resuena con otras personas.
          <br />
          <strong>¡Bienvenido a Echonet!</strong>
        </p>
      </div>

              <!-- Simulación de reproductor -->
        <div class="player-card shadow-lg rounded p-4 mt-4 bg-dark bg-opacity-25 d-inline-block w-100">
            <img :src="currentTrack.album.cover" alt="Album cover" class="w-100 rounded mb-3 spinning-disk" />
          <h5>{{ currentTrack.name }}</h5>
          <p class="">{{ currentTrack.artist }}</p>
          <div class="d-flex justify-content-between align-items-center mt-3">
            <button class="btn btn-sm btn-outline-light"><i class="fas fa-pause"></i></button>
            <button class="btn btn-sm btn-outline-light"><i class="fas fa-forward"></i></button>
          </div>
        </div>


      <!-- Efecto de onda de audio (solo visual) -->
      <div class="audio-wave position-absolute bottom-0 start-0 w-100">
        <div class="wave-bar"></div>
        <div class="wave-bar delay-1"></div>
        <div class="wave-bar delay-2"></div>
        <div class="wave-bar delay-3"></div>
      </div>
    </div>

    <!-- Lado derecho - Login -->
    <div 
      class="col-md-6 col-12 d-flex flex-column justify-content-center align-items-center p-5 text-white"
      style="background: linear-gradient(to top, #140055 0%, #39008D 100%); border-left: 2px solid #1768EB;"
    >
      <img src="@/assets/logo.png" alt="Echonet Logo" height="18%" class="d-inline-block align-text-top logo mb-3" style="filter: brightness(0) saturate(100%) invert(67%) sepia(98%) saturate(749%) hue-rotate(61deg) brightness(97%) contrast(101%);">

      <div class="w-100" style="max-width: 500px;">

        <h3 class="mb-4 text-center">Accede con tu cuenta de Spotify</h3>
        <p class="text-center  mb-5" style="opacity: 0.9;">
          No necesitas contraseña, solo buena música.
        </p>

        <div class="d-flex justify-content-center">
          <button @click="goToExternalLogin" class="btn btn-spotify d-flex align-items-center justify-content-center gap-2 py-3">
            <span>Iniciar sesión con Spotify</span>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import { useUserStore } from '@/stores/user';
import fondoUrl from '@/assets/fondo.png'
import logoUrl from '@/assets/vinyl.png'


export default {
  data() {
    return {
      currentTrack: {
        name: "Bienvenido a Echonet",
        artist: "Echonet Team",
        album: {
          cover: logoUrl // Imagen de portada del álbum
        } 
      },
      fondoUrl // Importa la imagen
    };
  },
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

};
</script>

<style scoped>
/* Botón de Spotify */
.btn-spotify {
  background-color: #1DB954;
  color: white;
  border: none;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
.btn-spotify:hover {
  background-color: #1ed760;
}

/* Reproductor simulado */
.player-card {
  max-width: 300px;
}

/* Animación de ondas de audio */
.audio-wave {
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 5px;
}

.wave-bar {
  width: 6px;
  background: white;
  animation: wave 1s infinite ease-in-out;
}

.wave-bar.delay-1 {
  animation-delay: 0.2s;
}

.wave-bar.delay-2 {
  animation-delay: 0.4s;
}

.wave-bar.delay-3 {
  animation-delay: 0.6s;
}

.spinning-disk {
  animation: spin 4s linear infinite;
  object-fit: cover; /* Por si la imagen no es cuadrada */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes wave {
  0%, 100% {
    height: 10px;
  }
  50% {
    height: 40px;
  }
}
</style>

