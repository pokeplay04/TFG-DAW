<template>
    <div class="container">
        <div class="row">
            <!-- Left Section (Trending Posts) -->
            <div class="col-lg-9">
                <div class="bg-white border rounded p-4">
                    <h2 class="h4">Trend: #{{ $route.params.id }}</h2>
                </div>
                
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
    name: 'TrendView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },

    data() {
        return {
            posts: [],
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
        getFeed() {
            axios
                .get(`posts/?trend=${this.$route.params.id}`)
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>