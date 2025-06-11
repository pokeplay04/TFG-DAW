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
                                    <img :src="user.get_avatar" class="rounded-circle" width="40" height="40"  v-if="user.id !== userStore.user.id" />
                                    <p class="fw-bold small mb-0" v-if="user.id !== userStore.user.id">{{ user.display_name }}</p>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-9">
                <div v-if="activeConversation && activeConversation.users" class="d-flex align-items-center gap-3 px-4 bg-white border rounded justify-content-between">
                    <template v-for="user in activeConversation.users" :key="user.id">
                        <template v-if="user.id !== userStore.user.id" class="">
                            <div class="d-flex align-items-center gap-3">
                                <img :src="user.get_avatar" class="rounded-circle" width="70" height="70" />
                                <h5><RouterLink :to="{ name: 'profile', params: { id: user.id } }" style="text-decoration: none;">{{ user.display_name }}</RouterLink></h5>
                            </div>
                            <div class="d-flex align-items-center gap-2">
                                <button type="button" class="btn btn-outline-primary btn-sm" @click="showSongSearch = true">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#4cd964" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M3 17a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />
                                        <path d="M9 17v-13h10v6" />
                                        <path d="M9 8h10" />
                                        <path d="M17.8 20.817l-2.172 1.138a.392 .392 0 0 1 -.568 -.41l.415 -2.411l-1.757 -1.707a.389 .389 0 0 1 .217 -.665l2.428 -.352l1.086 -2.193a.392 .392 0 0 1 .702 0l1.086 2.193l2.428 .352a.39 .39 0 0 1 .217 .665l-1.757 1.707l.414 2.41a.39 .39 0 0 1 -.567 .411l-2.172 -1.138z" />
                                    </svg>
                                </button>
                                <div v-if="selectedTrack" clas="align-items-center">
                                    <iframe
                                        :src="`https://open.spotify.com/embed/track/${selectedTrack}`" 
                                        width="400px"
                                        height="80"
                                        frameborder="0"
                                        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                                        loading="lazy"
                                        style="border-radius:12px">
                                    </iframe>
                                </div>
                            </div>
                        </template>
                    </template>
                    <!-- Modal para SongList -->
                    <div v-if="showSongSearch" class="modal-overlay" @click.self="showSongSearch = false" style="position: fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:9999;">
                        <div class="modal-content" style="background:white; padding:2rem; border-radius:12px; max-width:600px; width:90%; max-height:90vh; overflow-y:auto; position:relative;">
                            <button class="btn btn-sm btn-danger float-end" @click="showSongSearch = false">✖</button>
                            <SongList search_type="track" @select="handleTrackSelect" />
                        </div>
                    </div>
                </div>
                <div 
                    class="bg-white border rounded p-3"
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
                            rows="2"
                            style="resize: none;"
                        ></textarea>

                        <button class="btn btn-primary btn-sm">Enviar</button>
                    </form>
                </div>

            </div>
        </div>
    </div>
</template>
<script>
import axios from "@/utils/axios"
import { useUserStore } from '@/stores/user'
import SongList from '../components/SongList.vue'

export default {
    name: 'chat',

    components: {
        SongList
    },
    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            selectedTrack: null,
            conversations: [],
            activeConversation: {},
            body: '',
            intervalId: null, // <-- Guardamos el ID del intervalo aquí
            showSongSearch: false
        }
    },

    mounted() {
        this.getConversations()

        this.intervalId = setInterval(() => {  // <-- Guardamos el ID para poder limpiarlo después
            if (this.activeConversation && this.activeConversation.id) {
                console.log('Fetching messages for conversation:', this.activeConversation)
                this.getMessages()
            }
        }, 1000)
    },

    beforeUnmount() {  // <-- Aquí limpiamos el intervalo cuando el componente se desmonta
        clearInterval(this.intervalId)
    },

    methods: {
        handleTrackSelect(track) {
            this.selectedTrack = track.track_id
            axios
                .post(`chat/${this.activeConversation.id}/music/`, {
                    track_id: track.track_id,
                })
                .then(response => {
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
                    this.selectedTrack = response.data.track_id
                    this.scrollToBottom()
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