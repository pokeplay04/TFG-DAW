<template>
  <div class="mb-4 d-flex justify-content-between align-items-center">
    <div class="d-flex align-items-center gap-3">
      <img :src="post.created_by.get_avatar" class="rounded-circle" style="width: 40px; height: 40px; object-fit: cover;">
      <p class="mb-0">
        <strong>
          <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }">{{ post.created_by.display_name }}</RouterLink>
        </strong>
      </p>
    </div>
    <p class="text-muted mb-0">{{ post.created_at_formatted }} ago</p>
  </div>

  <p>{{ post.body }}</p>
  
  <template v-if="post.attachments.length">
    <img
      v-for="image in post.attachments"
      :key="image.id"
      :src="image.get_image"
      class="w-100 mb-3 rounded"
    />
  </template>

   <!-- En este componente se deberá comprobar si el post tiene music attachment y si es así se muestra el iframe (de la misma forma que se hace en el chat) -->
   <!-- Aquí no hace falta buscador ya que esto es un post ya publicado, sólo se muestra lo que ya está subido, igual que con la imagen -->
   <!-- En este caso el valor de track_id que irá en la url del embed la sacará de la base de datos 
    de la misma forma que está obteniendo datos como body(linea 14), image(linea 18), etc...   -->
    <!-- Te recomiendo que te guíes de ChatView pero saltandote toda la parte del buscador SongList ya que aquí no lo usamos -->
    <!-- Fijate también en el codigo de arriba ya que es parecido lo que hay que hacer ♥ -->


  <div class="my-4 d-flex justify-content-between align-items-center">
    <div class="d-flex align-items-center gap-4">
      <div class="d-flex align-items-center gap-2" @click="likePost(post.id)" role="button">
        <!-- LIKE -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#39ff65" style="width: 16px; height: 16px;">
          <path d="M11 11.5v-1a1.5 1.5 0 0 1 3 0v1.5" />
          <path d="M17 12v-6.5a1.5 1.5 0 0 1 3 0v10.5a6 6 0 0 1 -6 6h-2h.208a6 6 0 0 1 -5.012 -2.7a69.74 69.74 0 0 1 -.196 -.3c-.312 -.479 -1.407 -2.388 -3.286 -5.728a1.5 1.5 0 0 1 .536 -2.022a1.867 1.867 0 0 1 2.28 .28l1.47 1.47" />
          <path d="M14 10.5a1.5 1.5 0 0 1 3 0v1.5" />
          <path d="M8 13v-8.5a1.5 1.5 0 0 1 3 0v7.5" />
        </svg>
        <span class="text-muted small">{{ post.likes_count }} likes</span>
      </div>

      <div class="d-flex align-items-center gap-2">
        <!-- COMMENTS -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#39ff65" style="width: 16px; height: 16px;">
          <path d="M7 10h10" />
          <path d="M9 14h5" />
          <path d="M12.4 3a5.34 5.34 0 0 1 4.906 3.239a5.333 5.333 0 0 1 -1.195 10.6a4.26 4.26 0 0 1 -5.28 1.863l-3.831 2.298v-3.134a2.668 2.668 0 0 1 -1.795 -3.773a4.8 4.8 0 0 1 2.908 -8.933a5.33 5.33 0 0 1 4.287 -2.16" />
        </svg>
        <RouterLink :to="{ name: 'postview', params: { id: post.id } }" class="text-muted small">
          {{ post.comments_count }} comentarios
        </RouterLink>
      </div>

      <div v-if="post.is_private" class="d-flex align-items-center gap-2 text-muted small">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#39ff65" style="width: 16px; height: 16px;">
          <path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z" />
          <path d="M8 11m0 1a1 1 0 0 1 1 -1h6a1 1 0 0 1 1 1v3a1 1 0 0 1 -1 1h-6a1 1 0 0 1 -1 -1z" />
          <path d="M10 11v-2a2 2 0 1 1 4 0v2" />
        </svg>
        <span>Privado</span>
      </div>
    </div>

    <div role="button" @click="toggleExtraModal">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#39ff65" style="width: 16px; height: 16px;">
        <path d="M12 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" />
        <path d="M12 19m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" />
        <path d="M12 5m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" />
      </svg>
    </div>
  </div>

  <div v-if="showExtraModal">
    <div class="d-flex align-items-center gap-4">
      <div class="d-flex align-items-center gap-2 text-danger small" @click="deletePost" v-if="userStore.user.id === post.created_by.id" role="button">
        <!-- BORRAR -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" style="width: 16px; height: 16px;">
          <path d="M4 7h16" />
          <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
          <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
          <path d="M10 12l4 4m0 -4l-4 4" />
        </svg>
        <span>Borrar post</span>
      </div>

      <!-- REPORTAR -->
      <div class="d-flex align-items-center gap-2 text-warning small" @click="reportPost" role="button">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" style="width: 16px; height: 16px;">
          <path d="M5 5a5 5 0 0 1 7 0a5 5 0 0 0 7 0v9a5 5 0 0 1 -7 0a5 5 0 0 0 -7 0v-9z" />
          <path d="M5 21v-7" />
        </svg>
        <span>Reportar post</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios"
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    props: {
        post: Object
    },

    emits: ['deletePost'],

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    data() {
        return {
            showExtraModal: false
        }
    },

    methods: {
        likePost(id) {
            axios
                .post(`posts/${id}/like/`)
                .then(response => {
                    if (response.data.message == "like created") {
                        this.post.likes_count += 1;
                    }else if (response.data.message == "like deleted") {
                        this.post.likes_count -= 1;
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

        reportPost() {
            axios
                .post(`posts/${this.post.id}/report/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'El post ha sido reportado', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        deletePost() {
            this.$emit('deletePost', this.post.id)

            axios
                .delete(`posts/${this.post.id}/delete/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'El post ha sido borrado', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        toggleExtraModal() {
            console.log('toggleExtraModal')

            this.showExtraModal = !this.showExtraModal
        }
    },
    components: { RouterLink }
}
</script>