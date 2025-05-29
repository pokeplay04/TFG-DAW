<template>
  <div class="p-4 bg-white border rounded shadow-sm">
    <input
      v-model="search"
      class="form-control mb-3"
      type="text"
      placeholder="Buscar..."
    />

    <div v-if="songs.length === 0 && search">
      No se encontraron resultados
    </div>

    <div
      v-for="song in songs"
      :key="song.id"
      class="d-flex align-items-center justify-content-between mb-3"
    >
      <div class="d-flex align-items-center">
        <img :src="song.image" alt="Portada" class="rounded me-3" width="50" height="50" />
        <div>
          <strong>{{ song.title }}</strong><br />
          <small class="text-muted">{{ song.artist }}</small>
        </div>
      </div>

      <button @click="$emit('select', song)" class="btn btn-sm btn-primary">
        Añadir
      </button>
    </div>
  </div>
</template>


<script>
import axios from '@/utils/axios'

export default {
  name: 'SongList',

  props: {
    search_type: {
      type: String,
      default: 'track'  // Si no se especifica, buscará tracks
    }
  },

  data() {
    return {
      search: '',
      songs: [],
      loading: false
    }
  },

  watch: {
    search(newQuery) {
      this.fetchSongs()
    }
  },

  methods: {
    fetchSongs() {
      const query = this.search.trim()
      if (!query) {
        this.songs = []
        return
      }

      this.loading = true

      axios
        .get('spotify/search/', { params: { q: query, search_type: this.search_type } })
        .then(response => {
          this.songs = response.data.results
        })
        .catch(error => {
          console.error('Error al buscar canciones:', error)
          this.songs = []
        })
        .finally(() => {
          this.loading = false
        })
    }
  }
}

</script>
