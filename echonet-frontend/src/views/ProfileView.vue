<template>
    <div class="container text-black">
        <div class="row">
            <!-- Left Section (Profile Info) -->
            <div class="col-lg-3">
                <div class="bg-white border rounded p-4 text-center">
                    <img :src="user.get_avatar" class="mb-6 rounded-circle">
                    
                    <p><strong>{{ user.name }}</strong></p>

                    <div class="mt-6 d-flex justify-content-around">
                        <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-muted">{{ user.friends_count }} friends</RouterLink>
                        <p class="text-muted">{{ user.posts_count }} posts</p>
                    </div>

                    <div class="mt-6">
                        <button 
                            class="btn btn-purple btn-sm w-100 mb-2" 
                            @click="sendFriendshipRequest"
                            v-if="userStore.user.id !== user.id && can_send_friendship_request"
                        >
                            Send friendship request
                        </button>

                        <button 
                            class="btn btn-purple btn-sm w-100 mb-2" 
                            @click="sendDirectMessage"
                            v-if="userStore.user.id !== user.id"
                        >
                            Send direct message
                        </button>

                        <RouterLink 
                            class="btn btn-purple btn-sm w-100 mb-2" 
                            to="/profile/edit"
                            v-if="userStore.user.id === user.id"
                        >
                            Edit profile
                        </RouterLink>

                        <button 
                            class="btn btn-danger btn-sm w-100" 
                            @click="logout"
                            v-if="userStore.user.id === user.id"
                        >
                            Log out
                        </button>
                    </div>
                </div>
            </div>

            <!-- Center Section (Feed) -->
            <div class="col-lg-6">
                <div 
                    class="bg-white border rounded p-4 mb-4"
                    v-if="userStore.user.id === user.id"
                >
                    <FeedForm 
                        :user="user" 
                        :posts="posts"
                    />
                </div>

                <div 
                    class="bg-white border rounded p-4 mb-4"
                    v-for="post in posts"
                    :key="post.id"
                >
                    <FeedItem :post="post" @deletePost="deletePost"/>
                </div>
            </div>

            <!-- Right Section (Suggested People & Trends) -->
            <div class="col-lg-3">
                <PeopleYouMayKnow />

                <Trends />
            </div>
        </div>
    </div>
</template>

<style scoped>
input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>

<script>
import axios from "@/utils/axios"
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import FeedForm from '../components/FeedForm.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    name: 'ProfileView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        FeedForm
    },

    data() {
        return {
            posts: [],
            user: {
                id: localStorage.getItem('user_id'),
                get_avatar: localStorage.getItem('get_avatar'),
                name: localStorage.getItem('name'),
                friends_count: localStorage.getItem('friends_count'),
                posts_count: localStorage.getItem('posts_count'),
            },
            can_send_friendship_request: null,
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: { 
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },

        sendDirectMessage() {
            axios
                .get(`chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        sendFriendshipRequest() {
            axios
                .post(`friends/${this.$route.params.id}/request/`)
                .then(response => {
                    this.can_send_friendship_request = false

                    if (response.data.message === 'request already sent') {
                        this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-warning')
                    } else {
                        this.toastStore.showToast(5000, 'The request was sent!', 'bg-success')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFeed() {
            axios
                .get(`posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    this.posts = response.data.posts
                    this.user = response.data.user
                    this.can_send_friendship_request = response.data.can_send_friendship_request
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            this.userStore.removeToken()
            this.$router.push('/login')
        }
    }
}
</script>