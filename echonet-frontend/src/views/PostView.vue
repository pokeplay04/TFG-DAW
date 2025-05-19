<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-9 mb-4">
                <div v-if="post.id" class="p-3 bg-white border rounded mb-4">
                    <FeedItem :post="post" />
                </div>

                <div
                    v-for="comment in post.comments"
                    :key="comment.id"
                    class="p-3 bg-white border rounded mb-3 ms-4"
                >
                    <CommentItem :comment="comment" />
                </div>

                <div class="bg-white border rounded">
                    <form @submit.prevent="submitForm" method="post">
                        <div class="p-3">
                            <textarea v-model="body" class="form-control" rows="4" placeholder="What do you think?"></textarea>
                        </div>
                        <div class="p-3 border-top">
                            <button type="submit" class="btn btn-primary">Comment</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Right sidebar -->
            <div class="col-lg-3 mb-4">
                <PeopleYouMayKnow />
                <Trends class="mt-4" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import CommentItem from '../components/CommentItem.vue'

export default {
    name: 'PostView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        CommentItem
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`posts/${this.$route.params.id}/`)
                .then(response => {
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            axios
                .post(`posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>
