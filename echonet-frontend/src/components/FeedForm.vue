<template>
  <form @submit.prevent="submitForm" method="post" class="card p-4 shadow-sm">
    <!-- Texto del post -->
    <div class="mb-3">
      <label for="postBody" class="form-label">¿En qué estás pensando?</label>
      <textarea v-model="body" id="postBody" class="form-control" rows="3" placeholder="Escribe algo..."></textarea>
    </div>

    <!-- Vista previa de imagen -->
    <div v-if="url" class="mb-3 position-relative">
      <label class="form-label">Preview de la imagen:</label><br />
      <img :src="url" class="rounded img-thumbnail" style="max-width: 150px;" />
      <button @click="removeImage" type="button" class="btn btn-danger btn-sm position-absolute" style="top: 0; right: 0;">✖</button>
    </div>

    <!-- Vista previa de canción seleccionada -->
    <div v-if="selectedTrack" class="mb-3 d-flex align-items-center gap-3 border p-2 rounded position-relative">
      <img :src="selectedTrack.track_image" alt="track" style="width: 50px; height: 50px; object-fit: cover;" class="rounded">
      <div>
        <div class="fw-bold">{{ selectedTrack.track_name }}</div>
        <div class="text-muted">{{ selectedTrack.track_artist }}</div>
      </div>
      <button @click="removeTrack" type="button" class="btn btn-danger btn-sm position-absolute" style="top: 5px; right: 5px;">✖</button>
    </div>

    <!-- Botones: Adjuntar imagen y buscar canción -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="gap-2 d-flex">
        <label class="btn btn-outline-secondary btn-sm mb-0">
          Adjuntar imagen
          <input type="file" ref="file" @change="onFileChange" hidden />
        </label>

        <button type="button" class="btn btn-outline-primary btn-sm" @click="showSongSearch = true">
          Buscar canción
        </button>
      </div>

      <div class="gap-2 d-flex">
        <!-- Checkbox de privacidad -->
        <div class="form-check justify-content-end mb-0 pt-4">
          <input class="form-check-input" type="checkbox" v-model="is_private" id="isPrivate">
          <label class="form-check-label" for="isPrivate">Privado</label>
        </div>

        <!-- Botón de envío -->
        <div class="d-flex justify-content-end pt-3">
          <button type="submit" class="btn btn-success">Post</button>
        </div>
      </div>

    </div>

    <!-- Popup modal -->
    <div 
      v-if="showSongSearch" 
      class="modal-overlay"
      @click.self="showSongSearch = false"
    >
      <div class="modal-content">
        <!-- Barra superior del modal -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span class="text-muted">Escribe para buscar canción...</span>
          <button class="btn btn-sm btn-danger position-relative" @click="showSongSearch = false">
            ✖ <!-- Solo el botón de cierre -->
          </button>
        </div>
        <SongList @select="handleTrackSelect" />
      </div>
    </div>
  </form>
</template>

<script>
import axios from "@/utils/axios"
import { useToastStore } from "@/stores/toast";
import SongList from "@/components/SongList.vue"

export default {
  props: {
    user: Object,
    posts: Array
  },
  components: {
    SongList
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  data() {
    return {
      body: '',
      is_private: false,
      url: null,
      selectedTrack: null,
      showSongSearch: false
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader()
        reader.onload = e => this.url = e.target.result
        reader.readAsDataURL(file)
      } else {
        this.url = null
        this.$refs.file.value = null
        this.toastStore.showToast(5000, "Por favor, selecciona un archivo de imagen válido", "bg-danger");
      }
    },
    handleTrackSelect(track) {
      this.selectedTrack = track
      this.showSongSearch = false
    },
    removeImage() {
      this.url = null
      this.$refs.file.value = null
    },
    removeTrack() {
      this.selectedTrack = null
    },
    submitForm() {
      if (!this.body.trim() && !this.$refs.file?.files[0] && !this.selectedTrack) {
        this.toastStore.showToast(5000, "No se puede enviar un post vacío", "bg-danger");
        return
      }

      const formData = new FormData()
      if (this.$refs.file?.files[0]) {
        formData.append('image', this.$refs.file.files[0])
      }
      formData.append('body', this.body)
      formData.append('is_private', this.is_private)
      if (this.selectedTrack?.track_id) {
        formData.append('track_id', this.selectedTrack.track_id)
      }

      axios.post('posts/create/', formData, {
        headers: { "Content-Type": "multipart/form-data" }
      }).then(response => {
        this.posts.unshift(response.data)
        this.body = ''
        this.is_private = false
        this.$refs.file.value = null
        this.url = null
        this.selectedTrack = null
      }).catch(error => {
        console.log('error', error)
      })
    }
  }
}
</script>

<style scoped>
.position-relative {
  position: relative;
}

.position-absolute {
  position: absolute;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

/* Posicionamiento del botón de cierre */
.modal-content .btn.btn-sm.btn-danger {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

</style>