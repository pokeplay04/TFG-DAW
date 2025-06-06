<template>
  <div class="container mt-5">
    <!-- Header -->
    <header class="mb-4">
      <h1 class="text-center text-light">Descubrir Música</h1>
    </header>

    <!-- Tabs -->
    <div class="tabs-container mb-4">
      <a
        v-for="(tab, index) in tabs"
        :key="index"
        :class="['tab', { 'tab-active': currentTab === tab.value }]"
        @click="currentTab = tab.value"
      >
        {{ tab.label }}
      </a>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Canciones -->
      <div v-if="currentTab === 'songs'" class="row g-3">
        <div
          v-for="(randomSong, index) in randomSongs"
          :key="index"
          class="col-md-6 col-lg-4"
        >
          <div class="card h-100">
            <img
              :src="randomSong.image_url"
              class="card-img-top"
              alt="Portada de la canción"
            />
            <div class="card-body">
              <h5 class="card-title">{{ randomSong.name }}</h5>
              <p class="card-text">{{ randomSong.artist }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Artistas -->
      <div v-if="currentTab === 'artists'" class="row g-3">
        <div
          v-for="(randomArtist, index) in randomArtists"
          :key="index"
          class="col-md-6 col-lg-4"
        >
          <div class="card h-100">
            <img
              :src="randomArtist.image_url"
              class="card-img-top"
              alt="Portada del artista"
            />
            <div class="card-body">
              <h5 class="card-title">{{ randomArtist.name }}</h5>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Spinner de Carga -->
    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import SongList from "@/components/SongList.vue";
import { useUserStore } from "@/stores/user";

export default {
  components: {
    SongList,
  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      friends: [],
      friendsTracks: [],
      friendsArtists: [],
      randomSongs: [],
      randomArtists: [],
      currentTab: "songs", // Variable para controlar la pestaña activa
      loading: false, // Indicador de carga
      tabs: [
        { label: "Canciones", value: "songs" },
        { label: "Artistas", value: "artists" },
      ],
    };
  },
  async mounted() {
    this.loading = true;
    await this.getFriends();
    await this.getFriendsTracks();
    console.log(this.friendsTracks)
    await this.getFriendsArtists();
        console.log(this.friendsArtists)

    this.loading = false;
  },

  methods: {
    async getFriends() {
      try {
        const response = await axios.get(`friends/${this.userStore.user.id}/`);
        this.friends = response.data.friends;
      } catch (error) {
        console.log("error", error);
      }
    },
    async getFriendsTracks() {
      this.friendsTracks = [];
      for (const friend of this.friends) {
        try {
          const response = await axios.get(`/spotify/top/`, {
            params: {
              spotifyuser_pk: friend.id,
              search_type: "tracks",
              time_range: "short_term",
            },
          });
          this.friendsTracks.push({
            friend: friend,
            items: response.data.results,
          });
        } catch (error) {
          console.log("error", error);
        }
      }
    },
    async getFriendsArtists() {
      this.friendsArtists = [];
      for (const friend of this.friends) {
        try {
          const response = await axios.get(`/spotify/top/`, {
            params: {
              spotifyuser_pk: friend.id,
              search_type: "artists",
              time_range: "short_term",
            },
          });
          this.friendsArtists.push({
            friend: friend,
            items: response.data.results,
          });
        } catch (error) {
          console.log("error", error);
        }
      }
    },
  },
};
</script>

<style scoped>
/* Estilos Generales */
body {
  background: linear-gradient(to bottom, #1b1e27, #2c2f39);
  color: white;
}

.container {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
}

/* Tabs */
.tabs-container {
  display: flex;
  gap: 10px;
}

.tab {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 5px 5px 0 0;
  background-color: white;
  color: #333;
  font-weight: bold;
  text-decoration: none;
  transition: all 0.3s ease;
}

.tab:hover {
  background-color: #f0f0f0;
}

.tab-active {
  background-color: #f0f0f0;
  box-shadow: 0 -2px 0 #4e73df inset;
}

/* Cards */
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

/* Spinner de Carga */
.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>