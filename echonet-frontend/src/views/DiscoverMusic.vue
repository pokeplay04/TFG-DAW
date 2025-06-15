<template>
  <div class="container">
    <!-- Header -->
    <header class="mb-0 py-3 d-flex flex-column align-items-center justify-content-center bg-gradient" style="background: linear-gradient(90deg, #4e73df 0%, #1b1e27 100%); border-radius: 1rem;">
      <div class="d-flex align-items-center gap-3 mb-0">
      <svg width="36" height="36" viewBox="0 0 236.05 225.25" xmlns="http://www.w3.org/2000/svg">
        <path
        d="m122.37,3.31C61.99.91,11.1,47.91,8.71,108.29c-2.4,60.38,44.61,111.26,104.98,113.66,60.38,2.4,111.26-44.6,113.66-104.98C229.74,56.59,182.74,5.7,122.37,3.31Zm46.18,160.28c-1.36,2.4-4.01,3.6-6.59,3.24-.79-.11-1.58-.37-2.32-.79-14.46-8.23-30.22-13.59-46.84-15.93-16.62-2.34-33.25-1.53-49.42,2.4-3.51.85-7.04-1.3-7.89-4.81-.85-3.51,1.3-7.04,4.81-7.89,17.78-4.32,36.06-5.21,54.32-2.64,18.26,2.57,35.58,8.46,51.49,17.51,3.13,1.79,4.23,5.77,2.45,8.91Zm14.38-28.72c-2.23,4.12-7.39,5.66-11.51,3.43-16.92-9.15-35.24-15.16-54.45-17.86-19.21-2.7-38.47-1.97-57.26,2.16-1.02.22-2.03.26-3.01.12-3.41-.48-6.33-3.02-7.11-6.59-1.01-4.58,1.89-9.11,6.47-10.12,20.77-4.57,42.06-5.38,63.28-2.4,21.21,2.98,41.46,9.62,60.16,19.74,4.13,2.23,5.66,7.38,3.43,11.51Zm15.94-32.38c-2.1,4.04-6.47,6.13-10.73,5.53-1.15-.16-2.28-.52-3.37-1.08-19.7-10.25-40.92-17.02-63.07-20.13-22.15-3.11-44.42-2.45-66.18,1.97-5.66,1.15-11.17-2.51-12.32-8.16-1.15-5.66,2.51-11.17,8.16-12.32,24.1-4.89,48.74-5.62,73.25-2.18,24.51,3.44,47.99,10.94,69.81,22.29,5.12,2.66,7.11,8.97,4.45,14.09Z"
        fill="#fff"
        />
      </svg>
      <h2 class="text-light fs-2 fw-bold mb-0">Descubrir Música</h2>
      </div>
    </header>

    <!-- Tabs -->
    <ul class="nav nav-tabs mt-3" role="tablist">
      <li class="nav-item" role="presentation">
        <a
          class="nav-link"
          :class="{ active: currentTab === 'songs' }"
          data-bs-toggle="tab"
          href="#songs"
          role="tab"
          aria-selected="true"
          @click="currentTab = 'songs'"
        >
          Canciones
        </a>
      </li>
      <li class="nav-item" role="presentation">
        <a
          class="nav-link"
          :class="{ active: currentTab === 'artists' }"
          data-bs-toggle="tab"
          href="#artists"
          role="tab"
          aria-selected="false"
          @click="currentTab = 'artists'"
        >
          Artistas
        </a>
      </li>
    </ul>

    <!-- Contenido de las pestañas -->
    <div class="tab-content bg-white">

      <!-- Pestaña de Canciones -->
      <div v-if="currentTab === 'songs'" class="row g-3">
        <div
          v-for="(friend, index) in friendsTracks"
          :key="index"
          class="col-md-6 col-lg-4"
        >
          <div class="card shadow-sm">

            <!-- Info del amigo -->
            <div class="mb-2 d-flex justify-content-between align-items-center px-3 pt-3">
              <div class="d-flex align-items-center gap-3">
                <img
                  :src="friend.friend.get_avatar"
                  class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;"
                >
                <p class="mb-0">
                  <strong>
                    <RouterLink
                      :to="{ name: 'profile', params: { id: friend.friend.id } }"
                      class="text-decoration-none text-dark"
                    >
                      {{ friend.friend.display_name }}
                    </RouterLink>
                  </strong>
                </p>
              </div>
            </div>

            <!-- Imagen de la canción -->
            <img
              :src="friend.items.track_image"
              class="card-img-top"
              alt="Portada de la canción"
            >

            <!-- Detalles de la canción -->
            <div class="card-body">
              <h5 class="card-title">{{ friend.items.track_name }}</h5>
              <p class="card-text text-muted">{{ friend.items.track_artist }}</p>
              <a
                :href="friend.items.track_url"
                target="_blank"
                class="btn btn-primary btn-sm w-100"
              >
              Escuchar
                  <!-- Logo de Spotify -->
                  <svg width="20" height="20" viewBox="0 0 236.05 225.25" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="m122.37,3.31C61.99.91,11.1,47.91,8.71,108.29c-2.4,60.38,44.61,111.26,104.98,113.66,60.38,2.4,111.26-44.6,113.66-104.98C229.74,56.59,182.74,5.7,122.37,3.31Zm46.18,160.28c-1.36,2.4-4.01,3.6-6.59,3.24-.79-.11-1.58-.37-2.32-.79-14.46-8.23-30.22-13.59-46.84-15.93-16.62-2.34-33.25-1.53-49.42,2.4-3.51.85-7.04-1.3-7.89-4.81-.85-3.51,1.3-7.04,4.81-7.89,17.78-4.32,36.06-5.21,54.32-2.64,18.26,2.57,35.58,8.46,51.49,17.51,3.13,1.79,4.23,5.77,2.45,8.91Zm14.38-28.72c-2.23,4.12-7.39,5.66-11.51,3.43-16.92-9.15-35.24-15.16-54.45-17.86-19.21-2.7-38.47-1.97-57.26,2.16-1.02.22-2.03.26-3.01.12-3.41-.48-6.33-3.02-7.11-6.59-1.01-4.58,1.89-9.11,6.47-10.12,20.77-4.57,42.06-5.38,63.28-2.4,21.21,2.98,41.46,9.62,60.16,19.74,4.13,2.23,5.66,7.38,3.43,11.51Zm15.94-32.38c-2.1,4.04-6.47,6.13-10.73,5.53-1.15-.16-2.28-.52-3.37-1.08-19.7-10.25-40.92-17.02-63.07-20.13-22.15-3.11-44.42-2.45-66.18,1.97-5.66,1.15-11.17-2.51-12.32-8.16-1.15-5.66,2.51-11.17,8.16-12.32,24.1-4.89,48.74-5.62,73.25-2.18,24.51,3.44,47.99,10.94,69.81,22.29,5.12,2.66,7.11,8.97,4.45,14.09Z"
                      :style="{ fill: 'white', strokeWidth: 0 }"
                    />
                  </svg>
              </a> 
            </div>

          </div>
        </div>
      </div>

      <!-- Pestaña de Artistas -->
      <div v-if="currentTab === 'artists'" class="row g-3">
        <div
          v-for="(friend, index) in friendsArtists"
          :key="index"
          class="col-md-6 col-lg-4"
        >
          <div class="card shadow-sm">

            <!-- Info del amigo -->
            <div class="mb-2 d-flex justify-content-between align-items-center px-3 pt-3">
              <div class="d-flex align-items-center gap-3">
                <img
                  :src="friend.friend.get_avatar"
                  class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;"
                >
                <p class="mb-0">
                  <strong>
                    <RouterLink
                      :to="{ name: 'profile', params: { id: friend.friend.id } }"
                      class="text-decoration-none text-dark"
                    >
                      {{ friend.friend.display_name }}
                    </RouterLink>
                  </strong>
                </p>
              </div>
            </div>

            <!-- Imagen del artista -->
            <img
              :src="friend.items.artist_image"
              class="card-img-top"
              alt="Foto del artista"
            >

            <!-- Nombre del artista -->
            <div class="card-body">
              <h5 class="card-title">{{ friend.items.artist_name }}</h5>
              <a
                :href="friend.items.artist_url"
                target="_blank"
                class="btn btn-primary btn-sm w-100"
              >
                Ver artista
                  <!-- Logo de Spotify -->
                  <svg width="20" height="20" viewBox="0 0 236.05 225.25" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="m122.37,3.31C61.99.91,11.1,47.91,8.71,108.29c-2.4,60.38,44.61,111.26,104.98,113.66,60.38,2.4,111.26-44.6,113.66-104.98C229.74,56.59,182.74,5.7,122.37,3.31Zm46.18,160.28c-1.36,2.4-4.01,3.6-6.59,3.24-.79-.11-1.58-.37-2.32-.79-14.46-8.23-30.22-13.59-46.84-15.93-16.62-2.34-33.25-1.53-49.42,2.4-3.51.85-7.04-1.3-7.89-4.81-.85-3.51,1.3-7.04,4.81-7.89,17.78-4.32,36.06-5.21,54.32-2.64,18.26,2.57,35.58,8.46,51.49,17.51,3.13,1.79,4.23,5.77,2.45,8.91Zm14.38-28.72c-2.23,4.12-7.39,5.66-11.51,3.43-16.92-9.15-35.24-15.16-54.45-17.86-19.21-2.7-38.47-1.97-57.26,2.16-1.02.22-2.03.26-3.01.12-3.41-.48-6.33-3.02-7.11-6.59-1.01-4.58,1.89-9.11,6.47-10.12,20.77-4.57,42.06-5.38,63.28-2.4,21.21,2.98,41.46,9.62,60.16,19.74,4.13,2.23,5.66,7.38,3.43,11.51Zm15.94-32.38c-2.1,4.04-6.47,6.13-10.73,5.53-1.15-.16-2.28-.52-3.37-1.08-19.7-10.25-40.92-17.02-63.07-20.13-22.15-3.11-44.42-2.45-66.18,1.97-5.66,1.15-11.17-2.51-12.32-8.16-1.15-5.66,2.51-11.17,8.16-12.32,24.1-4.89,48.74-5.62,73.25-2.18,24.51,3.44,47.99,10.94,69.81,22.29,5.12,2.66,7.11,8.97,4.45,14.09Z"
                      :style="{ fill: 'white', strokeWidth: 0 }"
                    />
                  </svg>
              </a>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Spinner de carga -->
    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import { useUserStore } from "@/stores/user";

export default {
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      friends: [],
      friendsTracks: [],
      friendsArtists: [],
      currentTab: "songs",
      loading: false,
    };
  },
  async mounted() {
    this.loading = true;
    await this.getFriends();
    await this.getFriendsTracks();
    await this.getFriendsArtists();
    this.loading = false;
  },
  methods: {
    async getFriends() {
      try {
        const response = await axios.get(`friends/${this.userStore.user.id}/`);
        this.friends = response.data.friends;
      } catch (error) {
        console.error("Error al obtener amigos:", error);
      }
    },
    async getFriendsTracks() {
      this.friendsTracks = [];
      for (const friend of this.friends) {
        try {
          const response = await axios.get("/spotify/top/", {
            params: {
              spotifyuser_pk: friend.id,
              search_type: "tracks",
              time_range: "short_term",
            },
          });

          response.data.results.forEach(track => {
            this.friendsTracks.push({
              friend: friend,
              items: {
                ...track,
              },
            });
            // randomizar el orden de las canciones
            this.friendsTracks.sort(() => Math.random() - 0.5);
          });
        } catch (error) {
          console.error("Error al obtener canciones de amigo:", error);
        }
      }
    },
    async getFriendsArtists() {
      this.friendsArtists = [];
      for (const friend of this.friends) {
        try {
          const response = await axios.get("/spotify/top/", {
            params: {
              spotifyuser_pk: friend.id,
              search_type: "artists",
              time_range: "short_term",
            },
          });

          response.data.results.forEach(artist => {
            this.friendsArtists.push({
              friend: friend,
              items: {
                ...artist,
              },
            });
            // randomizar el orden de los artistas
            this.friendsArtists.sort(() => Math.random() - 0.5);
          });
        } catch (error) {
          console.error("Error al obtener artistas de amigo:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
body {
  background: linear-gradient(to bottom, #1b1e27, #2c2f39);
  color: white;
}

.container {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
}

.nav-tabs {
  background-color: #fff;
  border-bottom: 1px solid #dee2e6;
  border-radius: 0.375rem 0.375rem 0 0;
}

.nav-tabs .nav-link {
  color: #6c757d;
  font-weight: 500;
  border: 1px solid transparent;
  border-top-left-radius: 0.375rem;
  border-top-right-radius: 0.375rem;
  margin-bottom: -1px;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out;
}

.nav-tabs .nav-link.active,
.nav-tabs .nav-link:hover {
  color: #4e73df;
  background-color: #fff;
  border-color: #dee2e6 #dee2e6 #fff;
  box-shadow: inset 0 -2px 0 #4e73df;
}

.card {
  border: 1px solid #dee2e6;
  transition: transform 0.3s ease;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.card-body {
  padding: 1rem;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
}

.card-text {
  color: #adb5bd;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>