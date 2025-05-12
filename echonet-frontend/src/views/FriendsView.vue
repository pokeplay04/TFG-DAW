<template>
    <div class="container">
        <div class="row g-4">
            <!-- Left column -->
            <div class="col-lg-3">
                <div class="text-center bg-white border rounded p-4">
                    <img :src="user.get_avatar" class="rounded-circle mb-3" width="100" height="100">
                    
                    <p><strong>{{ user.name }}</strong></p>

                    <div class="mt-3 d-flex justify-content-around">
                        <p class="text-muted small mb-0">{{ user.friends_count }} friends</p>
                        <p class="text-muted small mb-0">{{ user.posts_count }} posts</p>
                    </div>
                </div>
            </div>

            <!-- Center column -->
            <div class="col-lg-6">
                <!-- Friendship Requests -->
                <div 
                    v-if="friendshipRequests.length"
                    class="bg-white border rounded p-4 mb-4"
                >
                    <h2 class="h5 mb-4">Friendship requests</h2>

                    <div 
                        class="bg-light rounded p-4 text-center mb-3"
                        v-for="friendshipRequest in friendshipRequests"
                        :key="friendshipRequest.id"
                    >
                        <img :src="friendshipRequest.created_by.get_avatar" class="rounded-circle mb-3" width="80" height="80">
                    
                        <p>
                            <strong>
                                <RouterLink :to="{ name: 'profile', params: { id: friendshipRequest.created_by.id } }">
                                    {{ friendshipRequest.created_by.name }}
                                </RouterLink>
                            </strong>
                        </p>

                        <div class="mt-3 d-flex justify-content-around">
                            <p class="text-muted small mb-0">{{ user.friends_count }} friends</p>
                            <p class="text-muted small mb-0">{{ user.posts_count }} posts</p>
                        </div>

                        <div class="mt-3">
                            <button class="btn btn-success me-2" @click="handleRequest('accepted', friendshipRequest.created_by.id)">Accept</button>
                            <button class="btn btn-danger" @click="handleRequest('rejected', friendshipRequest.created_by.id)">Reject</button>
                        </div>
                    </div>

                    <hr>
                </div>

                <!-- Friends list -->
                <div 
                    v-if="friends.length"
                    class="bg-white border rounded p-4"
                >
                    <div class="row g-3">
                        <div 
                            class="col-md-6"
                            v-for="user in friends"
                            :key="user.id"
                        >
                            <div class="bg-light rounded text-center p-3 h-100">
                                <img :src="user.get_avatar" class="rounded-circle mb-3" width="80" height="80">
                            
                                <p>
                                    <strong>
                                        <RouterLink :to="{ name: 'profile', params: { id: user.id } }">{{ user.name }}</RouterLink>
                                    </strong>
                                </p>

                                <div class="mt-2 d-flex justify-content-around">
                                    <p class="text-muted small mb-0">{{ user.friends_count }} friends</p>
                                    <p class="text-muted small mb-0">{{ user.posts_count }} posts</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right column -->
            <div class="col-lg-3">
                <div class="mb-3">
                    <PeopleYouMayKnow />
                </div>
                <div>
                    <Trends />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'

export default {
    name: 'FriendsView',

    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    components: {
        PeopleYouMayKnow,
        Trends
    },

    data() {
        return {
            user: {},
            friendshipRequests: [],
            friends: []
        }
    },

    mounted() {
        this.getFriends()
    },

    methods: {
        getFriends() {
            axios
                .get(`/api/friends/${this.$route.params.id}/`)
                .then(response => {
                    this.friendshipRequests = response.data.requests
                    this.friends = response.data.friends
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        handleRequest(status, pk) {
            axios
                .post(`/api/friends/${pk}/${status}/`)
                .then(response => {
                    this.getFriends()
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>
