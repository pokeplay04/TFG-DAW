<template>
  <div class="d-flex align-items-center p-2 rounded" style="max-width: 100%;">
    <!-- Imagen -->
    <img
      :src="itemData.image"
      alt="cover"
      class="me-2 rounded"
      style="width: 48px; height: 48px; object-fit: cover;"
    />

    <!-- Información -->
    <div class=" text-truncate flex-grow-1">
      <!-- Nombre del item -->
      <a
        :href="itemData.url"
        target="_blank"
        class="d-block text-black text-decoration-none fw-semibold text-truncate"
        style="max-width: 100%;"
      >
        {{ itemData.name }}
      </a>

      <!-- Artista (solo si es canción o álbum) -->
      <div v-if="itemData.artist" class="small text-muted text-truncate" style="max-width: 220px;">
        {{ itemData.artist }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PreviewItem',
  props: {
    item: {
      type: Object,
      required: true
    },
    searchType: {
      type: String,
      required: true,
      validator: value => ['track', 'album', 'artist'].includes(value)
    }
  },
  computed: {
    itemData() {
      const prefix = this.searchType

      if (prefix === 'track') {
        return {
          name: this.item[`${prefix}_name`],
          image: this.item[`${prefix}_image`],
          url: this.item[`${prefix}_url`],
          artist: this.item[`${prefix}_artist`]
        }
      }

      if (prefix === 'album') {
        return {
          name: this.item[`${prefix}_name`],
          image: this.item[`${prefix}_image`],
          url: this.item[`${prefix}_url`],
          artist: this.item[`${prefix}_artist`]
        }
      }

      if (prefix === 'artist') {
        return {
          name: this.item[`${prefix}_name`],
          image: this.item[`${prefix}_image`],
          url: this.item[`${prefix}_url`]
        }
      }

      return {}
    }
  }
}
</script>
