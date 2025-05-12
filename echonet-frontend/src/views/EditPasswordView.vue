<template>
    <div class="container">
        <div class="row g-4">
            <!-- Left Section -->
            <div class="col-lg-6">
                <div class="bg-white border rounded p-5">
                    <h1 class="mb-4 h4">Edit password</h1>
                    <p class="text-muted mb-4"></p>
                </div>
            </div>

            <!-- Right Section -->
            <div class="col-lg-6">
                <div class="bg-white border rounded p-5">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label class="form-label">Old password</label>
                            <input
                                type="password"
                                v-model="form.old_password"
                                class="form-control"
                                placeholder="Your old password"
                            />
                        </div>

                        <div class="mb-3">
                            <label class="form-label">New password</label>
                            <input
                                type="password"
                                v-model="form.new_password1"
                                class="form-control"
                                placeholder="Your new password"
                            />
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Repeat password</label>
                            <input
                                type="password"
                                v-model="form.new_password2"
                                class="form-control"
                                placeholder="Repeat password"
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
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length === 0) {
                const formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)

                axios
                    .post('/api/editpassword/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-success')
                            this.$router.push(`/profile/${this.userStore.user.id}`)
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }
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