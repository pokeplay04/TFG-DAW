<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-9">
                <div 
                    class="bg-white border rounded p-4 mb-3"
                    v-for="notification in notifications"
                    :key="notification.id"
                    v-if="notifications.length"
                >
                    {{ notification.body }}

                    <button class="btn btn-link p-0 ms-2" @click="readNotification(notification)">Read more</button>
                </div>

                <div 
                    class="bg-white border rounded p-4"
                    v-else
                >
                    You don't have any unread notifications!
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

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
                .get('/api/notifications/')
                .then(response => {
                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        async readNotification(notification) {
            await axios
                .post(`/api/notifications/read/${notification.id}/`)
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
