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
                                    >{{ user.name }}</p>
                                </template>
                            </div>

                            <span class="text-muted small">{{ conversation.modified_at_formatted }} ago</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-9">
                <div class="bg-white border rounded mb-4 p-3">
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
                                    <span class="text-muted small">{{ message.created_at_formatted }} ago</span>
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
                                    <span class="text-muted small">{{ message.created_at_formatted }} ago</span>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <div class="bg-white border rounded">
                    <form @submit.prevent="submitForm">
                        <div class="p-3">
                            <textarea v-model="body" class="form-control" placeholder="What do you want to say?" rows="3"></textarea>
                        </div>
                        <div class="p-3 border-top d-flex justify-content-between">
                            <button class="btn btn-primary">Send</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"
import { useUserStore } from '@/stores/user'

export default {
    name: 'chat',

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            conversations: [],
            activeConversation: {},
            body: ''
        }
    },

    mounted() {
        this.getConversations()
    },
    
    methods: {
        setActiveConversation(id) {
            this.activeConversation = id
            this.getMessages()
        },

        getConversations() {
            axios
                .get('chat/')
                .then(response => {
                    this.conversations = response.data

                    if (this.conversations.length) {
                        this.activeConversation = this.conversations[0].id
                    }

                    this.getMessages()
                })
                .catch(error => {
                    console.log(error)
                })
        },

        getMessages() {
            axios
                .get(`chat/${this.activeConversation}/`)
                .then(response => {
                    this.activeConversation = response.data
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
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>
