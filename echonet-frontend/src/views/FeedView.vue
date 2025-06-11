<template>
  <div class="container-fluid">
    <div class="row g-4">
      <!-- Columna principal: Feed -->
      <div class="col-lg-9">

        <div class="bg-white border rounded mb-3 p-3">
          <FeedForm :user="null" :posts="posts" />
        </div>

        <!-- Scrollable feed container -->
        <div>
          <div 
            class="bg-white border rounded p-3 mb-3"
            v-for="post in posts"
            :key="post.id"
          >
            <FeedItem :post="post" @deletePost="deletePost" />
          </div>
        </div>
      </div>

      <!-- Sidebar: Componentes sticky -->
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
