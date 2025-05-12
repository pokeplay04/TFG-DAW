<template>
    <div class="container">
        <div class="row g-4">
            <!-- Left Section -->
            <div class="col-lg-6">
                <div class="bg-white border rounded p-5">
                    <h1 class="mb-4 h4">Edit profile</h1>
                    <p class="text-muted mb-4"></p>
                    <RouterLink to="/profile/edit/password" class="text-decoration-underline">Edit password</RouterLink>
                </div>
            </div>

            <!-- Right Section -->
            <div class="col-lg-6">
                <div class="bg-white border rounded p-5">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input
                                type="text"
                                v-model="form.name"
                                class="form-control"
                                placeholder="Your full name"
                            />
                        </div>

                        <div class="mb-3">
                            <label class="form-label">E-mail</label>
                            <input
                                type="email"
                                v-model="form.email"
                                class="form-control"
                                placeholder="Your e-mail address"
                            />
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Avatar</label>
                            <input
                                type="file"
                                ref="file"
                                class="form-control"
                            />
                        </div>

                        <!-- Error messages -->
                        <div v-if="errors.length > 0" class="alert alert-danger">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>

                        <div>
                            <button class="btn btn-primary">Save changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.errors.length === 0) {
                const formData = new FormData()
                formData.append('avatar', this.$refs.file?.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-success')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                avatar: response.data.user.get_avatar
                            })

                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-danger')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>
