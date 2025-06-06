<template>
  <div class="p-4 bg-white border rounded">
    <h3 class="mb-4 h5">Personas que podrías conocer</h3>
    <div class="d-grid gap-3">
      <div 
        class="d-flex justify-content-between align-items-center"
        v-for="user in users"
        :key="user.id"
      >
        <div class="d-flex align-items-center gap-2">
          <img 
            :src="user.get_avatar"
            class="rounded-circle"
            style="width: 40px; height: 40px; object-fit: cover;"
          >

          <RouterLink 
            :to="{ name: 'profile', params: { id: user.id } }"
            class="mb-0 small text-decoration-none fw-bold text-dark"
          >
            {{ user.display_name }}
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
    <script>
    import axios from "@/utils/axios"
    
    export default {
        data() {
            return {
                users: []
            }
        },
    
        mounted() {
            this.getFriendSuggestions()
        },
    
        methods: {
            getFriendSuggestions() {
                axios
                    .get('friends/suggested/')
                    .then(response => {
                        console.log(response.data)
    
                        this.users = response.data
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
    </script>