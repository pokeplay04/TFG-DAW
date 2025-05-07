<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="p-4 bg-white border rounded">
                    <h1 class="mb-4 h4">Sign up</h1>

                    <p class="mb-4 text-muted">
                    </p>

                    <p class="fw-bold">
                        ¿Ya tienes una cuenta? 
                        <RouterLink :to="{ name: 'login' }" class="text-decoration-underline">Click here</RouterLink> to log in!
                    </p>
                </div>
            </div>

            <div class="col-md-6 mb-4">
                <div class="p-4 bg-white border rounded">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input type="text" v-model="form.name" placeholder="Your full name" class="form-control">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">E-mail</label>
                            <input type="email" v-model="form.email" placeholder="Your e-mail address" class="form-control">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" v-model="form.password1" placeholder="Your password" class="form-control">
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Repeat password</label>
                            <input type="password" v-model="form.password2" placeholder="Repeat your password" class="form-control">
                        </div>

                        <template v-if="errors.length > 0">
                            <div class="alert alert-danger">
                                <p v-for="error in errors" :key="error">{{ error }}</p>
                            </div>
                        </template>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Sign up</button>
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

export default {
    setup() {
        const toastStore = useToastStore()
        return { toastStore }
    },

    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: ''
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

            if (this.form.password1 === '') {
                this.errors.push('Your password is missing')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link.', 'bg-emerald-500')

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data) {
                                this.errors.push(data[key][0].message)
                            }

                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
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
