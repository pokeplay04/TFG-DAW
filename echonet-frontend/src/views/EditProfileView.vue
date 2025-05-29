<template>
    <div class="container">
        <div class="row g-4">
            <!-- Left Section -->
            <div class="col-lg-6">
                <div class="bg-white border rounded p-5">
                    <h1 class="mb-4 h4">Editar perfil</h1>
                    <p class="text-muted mb-4"></p>
                </div>
            </div>

            <!-- Right Section -->
            <div class="col-lg-6">
                <div class="bg-white border rounded p-5">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label class="form-label">Nombre</label>
                            <input
                                type="text"
                                v-model="form.name"
                                class="form-control"
                                placeholder="Your full name"
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
                            <button class="btn btn-primary">Guardar cambios</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "@/utils/axios"

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
                name: this.userStore.user.name
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []


            if (this.form.name === '') {
                this.errors.push('Falta el nombre')
            }

            if (this.errors.length === 0) {
                const formData = new FormData()
                formData.append('avatar', this.$refs.file?.files[0])
                formData.append('display_name', this.form.name)

                axios
                    .post('editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            this.toastStore.showToast(5000, 'La información ha sido guardada', 'bg-success')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                avatar: response.data.user.get_avatar
                            })

                            // this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Por favor, inténtalo de nuevo`, 'bg-danger')
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
