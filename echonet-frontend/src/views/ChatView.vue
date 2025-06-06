<template>
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-3">
                <div class="p-3 bg-white border rounded">
                    <div>
                        <div 
                            class="d-flex justify-content-between align-items-center mb-3 cursor-pointer"
                            v-for="conversation in conversations"
                            :key="conversation.id"
                            @click="setActiveConversation(conversation.id)"
                            style="cursor: pointer;"
                        >
                            <div class="d-flex align-items-center gap-2">
                                <template v-for="user in conversation.users" :key="user.id">
                                    <img :src="user.get_avatar" class="rounded-circle" width="40" height="40" />
                                    <p 
                                        class="fw-bold small mb-0"
                                        v-if="user.id !== userStore.user.id"
                                    >{{ user.display_name }}</p>
                                </template>
                            </div>
                            <span class="text-muted small">Hace {{ conversation.modified_at_formatted }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-9">
                <div 
                    class="bg-white border rounded mb-4 p-3"
                    style="height: 500px; overflow-y: auto;"
                    ref="messagesContainer"
                >
                    <div class="d-flex flex-column">
                        <template v-for="message in activeConversation.messages" :key="message.id">
                            <div 
                                class="d-flex justify-content-end align-items-start mt-2"
                                v-if="message.created_by.id == userStore.user.id"
                            >
                                <div class="me-2">
                                    <div class="bg-primary text-white p-3 rounded-start rounded-bottom">
                                        <p class="mb-0 small">{{ message.body }}</p>
                                    </div>
                                    <span class="text-muted small">Hace {{ message.created_at_formatted }}</span>
                                </div>
                                <img :src="message.created_by.get_avatar" class="rounded-circle" width="40" height="40" />
                            </div>

                            <div 
                                class="d-flex align-items-start mt-2"
                                v-else
                            >
                                <img :src="message.created_by.get_avatar" class="rounded-circle me-2" width="40" height="40" />
                                <div>
                                    <div class="bg-light p-3 rounded-end rounded-bottom">
                                        <p class="mb-0 small">{{ message.body }}</p>
                                    </div>
                                    <span class="text-muted small">Hace {{ message.created_at_formatted }}</span>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <div class="bg-white border rounded p-2">
                    <form @submit.prevent="submitForm" class="d-flex align-items-start gap-2">
                        <textarea 
                            v-model="body" 
                            class="form-control form-control-sm" 
                            placeholder="¿Qué quieres decir?" 
                            rows="1"
                            style="resize: none;"
                        ></textarea>

                        <button class="btn btn-primary btn-sm">Enviar</button>
                    </form>
                </div>


                <!-- Camponente songlist desde donde buscamos y seleccionamos la canción que queremos -->
                <SongList search_type="track" @select="handleTrackSelect" /> 

                <!-- Iframe que muestra la canción seleccionada solo si la variable selectedTrack (la que indica la canción seleccionada) tiene valor -->
                <div v-if="selectedTrack" class="mt-4">
                <!-- Construimos la url en scr añadiendole el ID de la cancion seleccionada (valor de selectedTrack) ya que así es como funcionan las urls de Spotify -->
                <iframe
                    :src="`https://open.spotify.com/embed/track/${selectedTrack}`" 
                    width="40%"
                    height="80"
                    frameborder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                    style="border-radius:12px">
                </iframe>
                </div>
                


            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"
import { useUserStore } from '@/stores/user'
import SongList from '../components/SongList.vue' // Importar el componente SongList para podder usarlo en el script

export default {
    name: 'chat',

    components: {
        SongList // Registrar el componente SongList para poder usarlo en la vista
    },
    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            selectedTrack: null, // Variable para almacenar la canción seleccionada (su ID) que se va a establecer en el chat
            conversations: [],
            activeConversation: {},
            body: ''
        }
    },

mounted() {
    this.getConversations()

    setInterval(() => {
        if (this.activeConversation && this.activeConversation.id) {
            console.log('Fetching messages for conversation:', this.activeConversation)
            this.getMessages()
        }
    }, 1000)
},

    methods: {
        handleTrackSelect(track) { // Método para manejar la selección de una canción desde el componente SongList
            this.selectedTrack = track.track_id // Establecer el id de la canción seleccionada en el buscador a la variable selectedTrack
            // llamada a axios para guardar la canción seleccionada en la base de datos ç
            axios
                .post(`chat/${this.activeConversation.id}/music/`, { // Enviar la canción seleccionada al servidor mediante esta URL definida en el backend
                    track_id: track.track_id, // Se le pasa como parámetro el id de la canción seleccionada
                })
                .then(response => { // (Opcional y para Debug) Mostrar la respuesta del servidor en la consola
                    console.log('Track saved:', response.data)
                })
                .catch(error => {
                    console.error('Error saving track:', error)
                })
        },
        scrollToBottom() {
            this.$nextTick(() => {
                const container = this.$refs.messagesContainer
                if (container) {
                    container.scrollTop = container.scrollHeight
                }
            })
        },

        setActiveConversation(id) {
            this.activeConversation.id = id
            this.getMessages()
        },

        getConversations() {
            axios
                .get('chat/')
                .then(response => {
                    this.conversations = response.data

                    if (this.conversations.length) {
                        this.activeConversation.id = this.conversations[0].id
                    }
                    this.getMessages()

                })
                .catch(error => {
                    console.log(error)
                })
        },

        getMessages() {
            axios
                .get(`chat/${this.activeConversation.id}/`)
                .then(response => {
                    this.activeConversation = response.data
                    this.selectedTrack = response.data.track_id // Asignar la canción seleccionada guardada en la base de datos a la variable selectedTrack de la ...
                    this.scrollToBottom()                       // ... vista cada vez que se cargan los mensajes (se cambie de chat) para tenerlo siempre actualizado
                })
                .catch(error => {
                    console.log(error)
                })
        },

        submitForm() {
            axios
                .post(`chat/${this.activeConversation.id}/send/`, {
                    body: this.body
                })
                .then(response => {
                    this.activeConversation.messages.push(response.data)
                    this.body = ''
                    this.scrollToBottom()
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>