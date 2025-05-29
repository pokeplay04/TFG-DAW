<template>
  <div class="container py-4">
    <div class="row">
      <div class="col-lg-9">
        <!-- Lista de notificaciones -->
        <div 
          class="mb-3 p-4 border rounded"
          v-for="notification in notifications"
          :key="notification.id"
          v-if="notifications.length"
          style="background-color: #290642; color: white; border-color: #B346DB;"
        >
          {{ notification.body }}
          <button
            class="btn btn-sm ms-2"
            @click="readNotification(notification)"
            style="color: #15CE00; background: transparent; border: none;"
          >
            Leer más
          </button>
        </div>

        <!-- Sin notificaciones -->
        <div
          class="p-4 border rounded"
          v-else
          style="background-color: #290642; color: white; border-color: #B346DB;"
        >
          ¡No tienes ninguna notificación por leer!
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios"

export default {
    name: 'notifications',

    data() {
        return {
            notifications: []
        }
    },

    mounted() {
        this.getNotifications()
    },

    methods: {
        getNotifications() {
            axios
                .get('notifications/')
                .then(response => {
                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        async readNotification(notification) {
            await axios
                .post(`notifications/read/${notification.id}/`)
                .then(response => {
                    if (notification.type_of_notification === 'post_like' || notification.type_of_notification === 'post_comment') {
                        this.$router.push({ name: 'postview', params: { id: notification.post_id } })
                    } else {
                        this.$router.push({ name: 'friends', params: { id: notification.created_for_id } })
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}
</script>
