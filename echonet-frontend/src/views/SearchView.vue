<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-9">
                <div class="bg-white border rounded p-2">
                    <form @submit.prevent="submitForm" class="d-flex">
                        <input 
                            v-model="query" 
                            type="search" 
                            class="form-control p-3" 
                            placeholder="¿Qué estás buscando?"
                        >

                        <button class="btn btn-purple ms-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
                                <line x1="16.65" y1="16.65" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </button>
                    </form>
                </div>

                <div class="row mt-4" v-if="users.length" style="overflow-x: auto; white-space: nowrap;">
                    <div class="d-flex flex-nowrap ">
                        <div 
                            class="col-md-3 mb-3" 
                            v-for="user in users" 
                            :key="user.id"
                        >
                            <div class="bg-white border rounded-lg text-center p-3">
                                <img :src="user.get_avatar" class="mb-3 rounded-circle" width="100">

                                <p>
                                    <strong>
                                        <RouterLink :to="{name: 'profile', params:{'id': user.id}}">{{ user.display_name }}</RouterLink>
                                    </strong>
                                </p>

                                <div class="d-flex justify-content-around">
                                    <p class="text-muted">{{ user.friends_count }} amigos</p>
                                    <p class="text-muted">{{ user.posts_count }} posts</p>
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>

                <div 
                    class="bg-white border rounded-lg p-4 mb-4"
                    v-for="post in posts"
                    :key="post.id"
                >
                    <FeedItem :post="post" />
                </div>
            </div>

            <div class="col-lg-3">
                <div class="position-sticky" style="top: 80px;">
                    <div class="mb-3">
                        <PeopleYouMayKnow />
                    </div>
                    <div>
                        <Trends />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'

export default {
    name: 'SearchView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },

    data() {
        return {
            query: '',
            users: [],
            posts: []
        }
    },

    methods: {
        submitForm() {
            console.log('submitForm', this.query)

            axios
                .post('search/', {
                    query: this.query
                })
                .then(response => {
                    console.log('response:', response.data)

                    this.users = response.data.users
                    this.posts = response.data.posts
                })
                .catch(error => {
                    console.log('error:', error)
                })
        }
    }
}
</script>

<style scoped>
.btn-purple {
    background-color: #6f42c1;
    color: white;
}
</style>