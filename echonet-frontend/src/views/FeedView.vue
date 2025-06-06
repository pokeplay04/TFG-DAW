<template>
    <div class="container">
        <div class="row g-4">
            <!-- Main content area (3/4 columns) -->
            <div class="col-lg-9">
                <!-- Feed form -->
                <div class="bg-white border rounded mb-3 p-3">
                    <FeedForm 
                        :user="null" 
                        :posts="posts"
                    />
                </div>

                <!-- Posts -->
                <div 
                    class="bg-white border rounded p-3 mb-3"
                    v-for="post in posts"
                    :key="post.id"
                >
                    <FeedItem :post="post" @deletePost="deletePost" />
                </div>
            </div>

            <!-- Sidebar (1/4 columns) -->
            <div class="col-lg-3">
                <div>
                    <SongList search_type="track" />
                </div>
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
import axios from "@/utils/axios"
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import FeedForm from '../components/FeedForm.vue'
import SongList from '../components/SongList.vue'

export default {
    name: 'FeedView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        FeedForm,
        SongList
    },

    data() {
        return {
            posts: [],
            body: '',
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('posts/')
                .then(response => {
                    this.posts = response.data
                })
                .catch(error => {
                    console.error('Error fetching feed:', error)
                })
        },

        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
    }
}
</script>
