<template>
  <div class="container mt-5">
    <!-- Header -->
    <header class="mb-4">
      <h1 class="text-center text-light">Descubrir Música</h1>
    </header>
<ul class="nav nav-tabs mt-3 mb-4" role="tablist">
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

    <!-- Tab Content -->
    <div class="tab-content bg-white">
      <!-- Canciones -->
      <div v-if="currentTab === 'songs'" class="row g-3">
        <div
          v-for="(friend, index) in friendsTracks"
          :key="index"
          class="col-md-6 col-lg-4"
        >
        <p>{{ friend }}</p>
         <PreviewItem :item="friend.items" searchType="track" />

        </div>
      </div>

      <!-- Artistas -->
      <div v-if="currentTab === 'artists'" class="row g-3">
        <div
          v-for="(friend, index) in friendsArtists"
          :key="index"
          class="col-md-6 col-lg-4"
        >
         <PreviewItem :item="friend.items" searchType="artist" />

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
import PreviewItem from "@/components/PreviewItem.vue";

  export default {
    components: {
      SongList,
      PreviewItem,
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
        currentTab: "songs",
        loading: false,
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
      await this.getFriendsArtists();

      // Procesar canciones
      this.randomSongs = this.friendsTracks.flatMap((friendData) =>
        friendData.items.map((track) => ({
          name: track.track_name,
          artist: track.track_artist,
          image_url: track.track_image,
        }))
      );

      // Procesar artistas
      this.randomArtists = this.friendsArtists.flatMap((friendData) =>
        friendData.items.map((artist) => ({
          name: artist.artist_name,
          image_url: artist.artist_image,
        }))
      );

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
            this.friendsTracks.push({
              friend: friend,
              items: response.data.results,
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
            this.friendsArtists.push({
              friend: friend,
              items: response.data.results,
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

/* Estilo de tabs como en ProfileView */
.nav-tabs {
  background-color: #fff;
  border-bottom: 1px solid #dee2e6;
  border-radius: 0.375rem 0.375rem 0 0;
  overflow-x: auto;
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



<!-- 

FriendsTracks[
  {
    track_name: "Song Title",
    track_artist: "Artist Name",
    track_image: "https://example.com/image.jpg"
    track_url: "https://example.com/track"
    friend: {
      display_name: "Friend Name",
      email: "
      friends
      get_avatar
      id
      posts
    }
  }
  {
    track_name: "Song Title",
    track_artist: "Artist Name",
    track_image: "https://example.com/image.jpg"
    track_url: "https://example.com/track"
    friend: {
      display_name: "Friend Name",
      email: "
      friends
      get_avatar
      id
      posts
    }
  }
]



-->