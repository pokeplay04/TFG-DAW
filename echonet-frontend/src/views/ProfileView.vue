<template>
  <div class="container-fluid h-100">
    <!-- Contenido principal -->
    <div class="row g-4 h-100">
      <!-- Columna izquierda: Perfil (sticky) -->
      <div class="col-lg-4 col-md-6 position-sticky top-0">
        <div class="bg-white p-4 rounded shadow-sm overflow-y-auto" style="height: 650px;">
          <!-- Avatar y nombre -->
            <div class="d-flex flex-column align-items-center mb-3">
            <img :src="user.get_avatar" alt="Avatar" class="rounded-circle mb-3" style="width: 80%; object-fit: cover;">
            <h2>{{ user.display_name }}</h2>
            </div>
          <!-- Botones de acción -->
          <div class="mt-3 d-flex flex-wrap gap-2 justify-content-between">
            <div class="d-flex gap-2">
              <RouterLink :to="{ name: 'friends', params: { id: user.id }}" class="btn btn-outline-secondary btn-sm">{{ user.friends_count }} amigos</RouterLink>
              <button class="btn btn-outline-secondary btn-sm" @click="sendDirectMessage" v-if="userStore.user.id !== user.id">Enviar mensaje</button>
              <button class="btn btn-outline-primary btn-sm" @click="sendFriendshipRequest" v-if="userStore.user.id !== user.id && can_send_friendship_request">Enviar solicitud</button>
            </div>
            <div class="d-flex gap-2">
              <RouterLink to="/profile/edit" class="btn btn-dark btn-sm" v-if="userStore.user.id === user.id">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00BE29" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 20h9" />
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                </svg>
              </RouterLink>
              <button class="btn btn-dark btn-sm" @click="logout" v-if="userStore.user.id === user.id">
                <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00BE29" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 16l4-4-4-4" />
                  <path d="M10 12h8" />
                  <path d="M4 4v16" />
                </svg>
              </button>
            </div>
          </div>
          <!-- Now Playing -->
          <div class="bg-light border rounded p-3 my-4">
            <h5 class="mb-3">Escuchando:</h5>
            <div v-if="trackNowPlaying" class="d-flex align-items-center">
              <img :src="trackNowPlaying.track_image" alt="Portada" class="me-3 rounded-circle spinning-disk" style="width: 60px; height: 60px; object-fit: cover;">
              <div>
                <strong>{{ trackNowPlaying.track_name }}</strong><br>
                <small>{{ trackNowPlaying.track_artist }}</small>
              </div>
            </div>
            <div v-else class="text-muted">
              No hay ninguna canción reproduciéndose actualmente.
            </div>
          </div>
        </div>
      </div>
      <!-- Columna derecha: Tabs principales -->
      <div class="col-lg-8 col-md-6 bg-white rounded"  style="height: 650px;">
        <!-- Tabs principales -->
        <ul class="nav nav-tabs mt-3" role="tablist">
          <li class="nav-item" role="presentation">
            <a class="nav-link active" data-bs-toggle="tab" href="#gallery" role="tab" aria-selected="true">Galería musical</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link" data-bs-toggle="tab" href="#posts" role="tab" aria-selected="false">Posts ({{ user.posts_count }})</a>
          </li>
        </ul>
        <!-- Contenido de tabs principales -->
        <div class="tab-content mt-3">
          <!-- Galería musical -->
          <div class="tab-pane fade show active" role="tabpanel" id="gallery">
            <!-- Sub-tabs de galería musical -->
            <ul class="nav nav-tabs mt-3" role="tablist">
              <li class="nav-item" role="presentation">
                <a class="nav-link active" data-bs-toggle="tab" href="#tracks" role="tab" aria-selected="true">Canciones</a>
              </li>
              <li class="nav-item" role="presentation">
                <a class="nav-link" data-bs-toggle="tab" href="#albums" role="tab" aria-selected="false">Álbumes</a>
              </li>
              <li class="nav-item" role="presentation">
                <a class="nav-link" data-bs-toggle="tab" href="#artists" role="tab" aria-selected="false">Artistas</a>
              </li>
            </ul>
            <!-- Contenido de sub-tabs -->
            <div class="tab-content mt-3">
              <!-- Canciones -->
              <div class="tab-pane fade show active" role="tabpanel" id="tracks">
                <div class="row g-3">
                  <div class="col-md-6 col-lg-4" v-for="(track, index) in musicGallery.tracks" :key="index">
                    <PreviewItem :item="track" searchType="track" />
                  </div>
                  <div v-if="musicGallery.tracks.length === 0" class="col-12 text-center text-muted">No hay canciones en la galería.</div>
                </div>
              </div>
              <!-- Álbumes -->
              <div class="tab-pane fade" role="tabpanel" id="albums">
                <div class="row g-3">
                  <div class="col-md-6 col-lg-4" v-for="(album, index) in musicGallery.albums" :key="index">
                    <PreviewItem :item="album" searchType="album" />
                  </div>
                  <div v-if="musicGallery.albums.length === 0" class="col-12 text-center text-muted">No hay álbumes en la galería.</div>
                </div>
              </div>
              <!-- Artistas -->
              <div class="tab-pane fade" role="tabpanel" id="artists">
                <div class="row g-3">
                  <div class="col-md-6 col-lg-4" v-for="(artist, index) in musicGallery.artists" :key="index">
                    <PreviewItem :item="artist" searchType="artist" />
                  </div>
                  <div v-if="musicGallery.artists.length === 0" class="col-12 text-center text-muted">No hay artistas en la galería.</div>
                </div>
              </div>
            </div>
          </div>
          <!-- Posts -->
          <div class="tab-pane fade" role="tabpanel" id="posts">
            <div class="posts-container bg-white rounded shadow-sm overflow-y-auto" style="max-height: calc(100vh - 200px);">
              <div class="bg-white border rounded p-4 mb-4" v-for="post in posts" :key="post.id">
                <FeedItem :post="post" @deletePost="deletePost"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import FeedItem from "../components/FeedItem.vue";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";
import PreviewItem from "../components/PreviewItem.vue";

export default {
  name: "ProfileView",
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return { userStore, toastStore };
  },
  components: {
    FeedItem,
    PreviewItem,
  },
  data() {
    return {
      posts: [],
      user: {
        id: localStorage.getItem("user_id"),
        get_avatar: localStorage.getItem("get_avatar"),
        display_name: localStorage.getItem("name"),
        bio: localStorage.getItem("bio") || "",
        friends_count: localStorage.getItem("friends_count"),
        posts_count: localStorage.getItem("posts_count"),
      },
      can_send_friendship_request: null,
      trackNowPlaying: null,
      musicGallery: {
        tracks: [],
        albums: [],
        artists: [],
      },
      activeTab: "tracks",
      searchQueries: {
        track: "",
        album: "",
        artist: "",
      },
    };
  },
  mounted() {
    this.getFeed();
    this.getGallery();
    this.getNowPlaying();
    setInterval(() => this.getNowPlaying(), 10000); // Actualizar cada 10 segundos
  },
  watch: {
    "$route.params.id": {
      handler: function () {
        this.getFeed();
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },
    sendDirectMessage() {
      axios
        .get(`chat/${this.$route.params.id}/get-or-create/`)
        .then(() => this.$router.push("/chat"))
        .catch((error) => console.log("error", error));
    },
    sendFriendshipRequest() {
      axios
        .post(`friends/${this.$route.params.id}/request/`)
        .then((response) => {
          this.can_send_friendship_request = false;
          if (response.data.message === "request already sent") {
            this.toastStore.showToast(
              5000,
              "La solicitud ya ha sido enviada.",
              "bg-warning"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Solicitud enviada.",
              "bg-success"
            );
          }
        })
        .catch((error) => console.log("error", error));
    },
    getFeed() {
      axios
        .get(`posts/profile/${this.$route.params.id}/`)
        .then((response) => {
          this.posts = response.data.posts;
          this.user = response.data.user;
          this.can_send_friendship_request =
            response.data.can_send_friendship_request;
        })
        .catch((error) => console.log("error", error));
    },
    getGallery() {
      axios
        .get(`gallery/${this.$route.params.id}/`)
        .then((response) => {
          this.musicGallery = response.data;
        })
        .catch((error) => console.log("error", error));
    },
    getNowPlaying() {
      axios
        .get(`spotify/now-playing/`, {
          params: { spotifyuser_pk: this.$route.params.id },
        })
        .then((response) => {
          this.trackNowPlaying = response.data || null;
        })
        .catch((error) => console.log("error", error));
    },
    logout() {
      this.userStore.removeToken();
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
/* Estilo general */
.container-fluid {
  max-width: 1400px;
  margin: 0 auto;
}
/* Tarjetas de galería */
.card {
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: scale(1.02);
}
/* Publicaciones */
.posts-container {
  scrollbar-width: thin;
  scrollbar-color: #ccc #f8f9fa;
}
/* Scrollbar estilizado */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}
::-webkit-scrollbar-track {
  background-color: #f8f9fa;
}
.spinning-disk {
  animation: spin 4s linear infinite;
  border: 2px solid #dee2e6; /* Opcional: para un borde bonito */
  object-fit: cover; /* Por si la imagen no es cuadrada */
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}


/* Responsive */
@media (max-width: 768px) {
  .col-lg-4 {
    flex-basis: 100%;
  }
  .posts-container {
    height: calc(100vh - 300px);
  }
}
</style>