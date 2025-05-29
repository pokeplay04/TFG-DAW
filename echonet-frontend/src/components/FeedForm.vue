<template>
  <form @submit.prevent="submitForm" method="post" class="card p-4 shadow-sm">
    <!-- Texto del post -->
    <div class="mb-3">
      <label for="postBody" class="form-label">En que estás pensando?</label>
      <textarea v-model="body" id="postBody" class="form-control" rows="3" placeholder="Escribe algo..."></textarea>
    </div>

    <!-- Checkbox de privacidad -->
    <div class="form-check mb-3">
      <input class="form-check-input" type="checkbox" v-model="is_private" id="isPrivate">
      <label class="form-check-label" for="isPrivate">Privado</label>
    </div>

    <!-- Vista previa de la imagen -->
    <div v-if="url" class="mb-3">
      <label class="form-label">Preview de la imagen:</label><br />
      <img :src="url" class="rounded img-thumbnail" style="max-width: 150px;" />
    </div>

    <!-- Selector de archivo e imagen -->
    <div class="d-flex justify-content-between align-items-center border-top pt-3">
      <div>
        <label class="btn btn-outline-secondary btn-sm">
          Adjuntar imagen
          <input type="file" ref="file" @change="onFileChange" hidden />
        </label>
      </div>

      <!--  1. Aquí se debe añadir el buscador (Songlist) que al enviar el formulario (publicar el post) guardará en la base de datos el track_id -->

      <!-- Botón de envío -->
      <button type="submit" class="btn btn-success">
        Post
      </button>
    </div>
  </form>
</template>

<script>
import axios from "@/utils/axios"

export default {
    props: {
        user: Object,
        posts: Array
    },

    data() {
        return {
            body: '',
            is_private: false,
            url: null,
        }
    },

    methods: {
        onFileChange(event) {
            const file = event.target.files[0];

            if (file && file.type.startsWith("image/")) {
                const reader = new FileReader();

                reader.onload = (e) => {
                    this.url = e.target.result;
                };

                reader.readAsDataURL(file);
            } else {
                this.url = null;
                this.$refs.file.value = null;
                alert("Porfavor seleccione un archivo de imagen válido.");
            }
        },

        // 2. El metodo de arriba hace que al seleccionar un archivo de imagen, se muestre una vista previa de la imagen seleccionada.
        //    se podria hacer algo parecido con el componente SongList, al seleccionar una canción se muestre una vista previa de la
        //     canción seleccionada (futuro componente previewTrack) o poner directamente el embed de la canción en el formulario de envio del post


        submitForm() {
            console.log('submitForm', this.body);

            let formData = new FormData();
            formData.append('image', this.$refs.file.files[0]);
            formData.append('body', this.body);
            formData.append('is_private', this.is_private);

            axios
                .post('posts/create/', formData, { // 3. Esta llamada axios (al backend) envia todo y ya en el backend se encarga de guardar la musica en su tabla correspondiente
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data);

                    this.posts.unshift(response.data);
                    this.body = '';
                    this.is_private = false;
                    this.$refs.file.value = null;
                    this.url = null;

                    if (this.user) {
                        this.user.posts_count += 1;
                    }
                })
                .catch(error => {
                    console.log('error', error);
                });
        }
    }
}
</script>