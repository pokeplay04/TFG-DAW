<template>
  <div class="container mt-2">
    <div class="row g-4">
      <!-- Left Section -->
      <div class="col-lg-5">
        <div class="bg-white border rounded p-5 shadow-sm">
          <h1 class="mb-4 h4">Editar perfil</h1>

          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="name" class="form-label">Nombre <span class="text-danger">*</span></label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                class="form-control"
                placeholder="Tu nombre de usuario"
              />
            </div>

            <div class="mb-3">
              <label for="avatar" class="form-label">Avatar</label>
              <div class="input-group">
                <input
                  type="file"
                  ref="file"
                  class="form-control"
                  id="avatar"
                  accept="image/*"
                  @change="handleFileChange"
                />
              </div>
            </div>

            <!-- Error messages -->
            <div v-if="errors.length > 0" class="alert alert-danger">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>

            <!-- Avatar Preview -->
            <div class="mt-4 text-center">
                <img
                v-if="avatarPreview"
                :src="avatarPreview"
                alt="Vista previa del avatar"
                class="img-fluid rounded shadow-sm"
                style="max-width: 200px;"
                />
            </div>

            <button type="submit" class="btn btn-primary">Guardar cambios</button>
          </form>
        </div>
      </div>

      <!-- Right Section -->
      <div class="col-lg-7">
        <div class="bg-white border rounded p-5 shadow-sm">
          <h1 class="mb-4 h4">Tus items favoritos</h1>

          <!-- Tabs -->
          <ul class="nav nav-tabs mb-3">
            <li class="nav-item">
              <a class="nav-link active" data-bs-toggle="tab" href="#songs-tab">Canciones</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-bs-toggle="tab" href="#albums-tab">Álbumes</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-bs-toggle="tab" href="#artists-tab">Artistas</a>
            </li>
          </ul>

          <!-- Tab Content -->
          <div class="tab-content mb-4">
            <div class="tab-pane fade show active" id="songs-tab">
              <div class="row d-flex flex-row flex-wrap">
                <div class="col-6" >
                  <div class="row d-flex flex-row flex-wrap" v-for="(track, index) in musicGallery.tracks" :key="index">
                    <PreviewItem :item="track" searchType="track" class="col-10" />
                    <button class="btn btn-sm btn-danger m-2 col-1" @click="deleteItem(track.id, 'track')" title="Eliminar"> &times; </button>
                  </div>
                </div>
                <div class="col-6" >
                  <SongList search_type="track" @select="selectTrack" />
                </div>
              </div>
            </div>
            <div class="tab-pane fade" id="albums-tab">
              <div class="row d-flex flex-row flex-wrap">
                <div class="col-6">
                  <div class="row d-flex flex-row flex-wrap" v-for="(album, index) in musicGallery.albums" :key="index">
                    <PreviewItem :item="album" searchType="album" class="col-10"/>
                    <button  class="btn btn-sm btn-danger m-2 col-1" @click="deleteItem(album.id, 'album')" title="Eliminar" > &times;</button>
                  </div>
                </div>
                <div class="col-6">
                  <SongList search_type="album" @select="selectAlbum" />
                </div>
              </div>
            </div>
            <div class="tab-pane fade" id="artists-tab">
              <div class="row d-flex flex-row flex-wrap">
                <div class="col-6">
                  <div class="row d-flex flex-row flex-wrap" v-for="(artist, index) in musicGallery.artists" :key="index">
                    <PreviewItem :item="artist" searchType="artist" class="col-10"/>
                    <button class="btn btn-sm btn-danger m-2 col-1" @click="deleteItem(artist.id, 'artist')" title="Eliminar"> &times;</button>
                  </div>
                </div>
                <div class="col-6">
                  <SongList search_type="artist" @select="selectArtist" />
                </div>
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
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import SongList from "@/components/SongList.vue";
import PreviewItem from "../components/PreviewItem.vue";


export default {
  components: {
    SongList,
    PreviewItem,

  },
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();

    return {
      toastStore,
      userStore,
    };
  },

  data() {
    return {
      form: {
        name: this.userStore.user.name,
      },
      errors: [],
      filePreview: "",
      avatarPreview: null,
      musicGallery: {
        tracks: [],
        albums: [],
        artists: [],
      },
    };
  },

  mounted() {
    this.getGallery();
  },

  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.filePreview = file.name;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.avatarPreview = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.filePreview = "";
        this.avatarPreview = null;
      }
    },

    getGallery() {
      axios
        .get(`gallery/${this.userStore.user.id}/`)
        .then((response) => {
          this.musicGallery = response.data;
          console.log("Gallery data:", this.musicGallery);
        })
        .catch((error) => console.log("error", error));
    },

    selectTrack(item) {
      // Comprobar si el track ya está en favoritos
      if (this.musicGallery.tracks.some(track => track.track_id === item.track_id)) {
      this.toastStore.showToast(5000, "Esta canción ya está en tus favoritos", "bg-danger");
      return;
      }
      if (this.musicGallery.tracks.length >= 18) {
      this.toastStore.showToast(5000, "No puedes añadir más de 18 canciones favoritas", "bg-danger");
      return;
      }
      axios
      .post(`gallery/${this.userStore.user.id}/save/`, {
        item: item,
        type: "track",
      })
      .then(response => {
        this.getGallery();
        console.log('Track saved:', response.data)
      })
      .catch(error => {
        console.error('Error saving track:', error)
      });
    },

    selectArtist(item) {
      // Comprobar si el artista ya está en favoritos
      if (this.musicGallery.artists.some(artist => artist.artist_id === item.artist_id)) {
      this.toastStore.showToast(5000, "Este artista ya está en tus favoritos", "bg-danger");
      return;
      }
      if (this.musicGallery.artists.length >= 18) {
      this.toastStore.showToast(5000, "No puedes añadir más de 18 artistas favoritos", "bg-danger");
      return;
      }
      axios
      .post(`gallery/${this.userStore.user.id}/save/`, {
        item: item,
        type: "artist",
      })
      .then(response => {
        this.getGallery();
        console.log('Artist saved:', response.data)
      })
      .catch(error => {
        console.error('Error saving artist:', error)
      });
    },

    selectAlbum(item) {
      // Comprobar si el álbum ya está en favoritos
      if (this.musicGallery.albums.some(album => album.album_id === item.album_id)) {
      this.toastStore.showToast(5000, "Este álbum ya está en tus favoritos", "bg-danger");
      return;
      }
      if (this.musicGallery.albums.length >= 18) {
      this.toastStore.showToast(5000, "No puedes añadir más de 18 álbumes favoritos", "bg-danger");
      return;
      }
      axios
      .post(`gallery/${this.userStore.user.id}/save/`, {
        item: item,
        type: "album",
      })
      .then(response => {
        this.getGallery();
        console.log('Album saved:', response.data)
      })
      .catch(error => {
        console.error('Error saving album:', error)
      });
    },

    deleteItem(itemId, itemType) {
      axios
        .post(`gallery/${this.userStore.user.id}/delete/`, {
          item_id: itemId,
          type: itemType,
        })
        .then(response => {
          this.toastStore.showToast(5000, "Elemento eliminado correctamente", "bg-success");
          this.getGallery(); // Recargar galería
        })
        .catch(error => {
          console.error('Error eliminando el elemento:', error);
          this.toastStore.showToast(5000, "No se pudo eliminar el elemento", "bg-danger");
        });
    },


    submitForm() {
      this.errors = [];

      if (!this.form.name.trim()) {
        this.errors.push("Falta el nombre");
      }
      if (this.form.name.length > 25) {
        this.errors.push("El nombre no debe superar los 25 caracteres");
      }

      const fileInput = this.$refs.file;
      const newAvatar = fileInput && fileInput.files && fileInput.files[0];

      if (this.errors.length === 0) {
        const formData = new FormData();
        if (newAvatar) {
          formData.append("avatar", newAvatar);
        }
        formData.append("display_name", this.form.name);

        axios
          .post("editprofile/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            if (response.data.message === "information updated") {
              this.toastStore.showToast(
                5000,
                "La información ha sido guardada",
                "bg-success"
              );

              this.userStore.setUserInfo({
                id: this.userStore.user.id,
                name: this.form.name,
                avatar: newAvatar ? response.data.user.get_avatar : this.userStore.user.avatar,
              });
            } else {
              this.toastStore.showToast(
                5000,
                `${response.data.message}. Por favor, inténtalo de nuevo`,
                "bg-danger"
              );
            }
          })
          .catch((error) => {
            console.error("Error al enviar los datos:", error);
          });
      }
    },
  },
};
</script>

<style scoped>
.bi-image {
  font-size: 3rem;
  color: #ced4da;
}
</style>