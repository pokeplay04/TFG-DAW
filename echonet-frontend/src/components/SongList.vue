<template>
  <div class="p-4 bg-white border rounded shadow-sm w-100">
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
      :key="song[search_type + '_id']"
      class="d-flex align-items-center justify-content-between mb-3 w-100"
    >
      <div class="flex-grow-1 me-2 text-truncate">
        <PreviewItem :item="song" :search-type="search_type" />
      </div>


      <button @click="$emit('select', song)" class="btn btn-sm btn-success">
        Añadir
      </button>
    </div>

  </div>
</template>


<script>
import axios from '@/utils/axios'
import PreviewItem from '@/components/PreviewItem.vue'


export default {
  components: { PreviewItem },
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
          console.error('Error al buscar :', error)
          this.songs = []
        })
        .finally(() => {
          this.loading = false
        })
    }
  }
}

</script>
