<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="p-4 bg-white border rounded">
                    <h1 class="mb-4 h4">Log in</h1>

                    <p class="mb-4 text-muted">
                    </p>

                    <p class="fw-bold">
                        ¿No tienes una cuenta? 
                        <RouterLink :to="{ name: 'signup' }" class="text-decoration-underline">Clica aquí</RouterLink> para crearte una!
                    </p>
                </div>
            </div>

            <div class="col-md-6 mb-4">
                <div class="p-4 bg-white border rounded">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" v-model="form.email" placeholder="Your e-mail address" class="form-control">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" v-model="form.password" placeholder="Your password" class="form-control">
                        </div>

                        <template v-if="errors.length > 0">
                            <div class="alert alert-danger">
                                <p v-for="error in errors" :key="error">{{ error }}</p>
                            </div>
                        </template>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Log in</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },

    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                try {
                    const response = await axios.post('login/', this.form)
                    this.userStore.setToken(response.data)
                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access

                    const userResponse = await axios.get('me/')
                    this.userStore.setUserInfo(userResponse.data)
                    this.$router.push('/feed')

                } catch (error) {
                    console.log('error', error)
                    this.errors.push('The email or password is incorrect! Or the user is not activated!')
                }
            }
        }
    }
}
</script>
