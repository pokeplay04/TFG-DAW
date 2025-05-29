<template>
  <div class="mb-4 border-bottom pb-3">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <div class="d-flex align-items-center">
        <img
          :src="comment.created_by.get_avatar"
          class="rounded-circle me-3"
          alt="Avatar"
          width="40"
          height="40"
        />
        <strong>
          <RouterLink :to="{ name: 'profile', params: { id: comment.created_by.id } }" class="text-dark text-decoration-none">
            {{ comment.created_by.display_name }}
          </RouterLink>
        </strong>
      </div>
      <small class="text-muted">{{ comment.created_at_formatted }} ago</small>
    </div>

    <p class="mb-0">{{ comment.body }}</p>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
  props: {
    comment: Object
  },
  components: { RouterLink }
}
</script>