<template>
    <div class="p-4 bg-white border rounded">
        <h3 class="mb-6 text-xl">Trends</h3>

        <div class="space-y-4">
            <div 
                class="flex items-center justify-between"
                v-for="trend in trends"
                v-bind:key="trend.id"
            >
                <RouterLink :to="{name: 'trendview', params: {id: trend.hashtag}}" class="text-xs rounded-lg"><strong>#{{ trend.hashtag }}</strong></RouterLink>

                <p class="text-gray-500">{{ trend.occurences }} posts</p>

            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"

export default {
    name: 'trends',

    data() {
        return {
            trends: []
        }
    },

    mounted() {
        this.getTrends()
    },

    methods: {
        getTrends() {
            axios
                .get('posts/trends/')
                .then(response => {
                    console.log(response.data)
            
                    this.trends = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}
</script>