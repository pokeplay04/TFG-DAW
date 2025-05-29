<script setup>
import { useToastStore } from '@/stores/toast'

const store = useToastStore()
</script>

<template>
    <div
        v-if="store.isVisible"
        class="toast show position-fixed bottom-0 end-0 m-4 text-white"
        :class="store.classes"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        style="z-index: 1055; min-width: 250px;"
    >
        <div class="toast-body">
            {{ store.message }}
        </div>
    </div>
</template>