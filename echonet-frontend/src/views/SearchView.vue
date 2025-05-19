<template>
    <div class="container">
        <div class="row">
            <!-- Left Section (Search and Results) -->
            <div class="col-lg-9">
                <div class="bg-white border rounded p-4">
                    <form @submit.prevent="submitForm" class="d-flex">
                        <input 
                            v-model="query" 
                            type="search" 
                            class="form-control p-4" 
                            placeholder="What are you looking for?"
                        >
                        
                        <button class="btn btn-purple ms-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                            </svg>
                        </button>
                    </form>
                </div>

                <!-- User Results -->
                <div class="row mt-4" v-if="users.length">
                    <div 
                        class="col-md-3 mb-4" 
                        v-for="user in users" 
                        :key="user.id"
                    >
                        <div class="bg-white border rounded-lg text-center p-4">
                            <img :src="user.get_avatar" class="mb-3 rounded-circle" width="100">
                            
                            <p>
                                <strong>
                                    <RouterLink :to="{name: 'profile', params:{'id': user.id}}">{{ user.name }}</RouterLink>
                                </strong>
                            </p>

                            <div class="d-flex justify-content-around">
                                <p class="text-muted">{{ user.friends_count }} friends</p>
                                <p class="text-muted">{{ user.posts_count }} posts</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Post Results -->
                <div 
                    class="bg-white border rounded-lg p-4 mb-4"
                    v-for="post in posts"
                    :key="post.id"
                >
                    <FeedItem :post="post" />
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
