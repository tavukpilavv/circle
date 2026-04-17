<template>
  <button class="see-all-btn" @click="navigateToDetails">
      See All
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  event: {
    type: Object,
    default: () => ({})
  }
})

const navigateToDetails = () => {
  if (props.event?.id) {
    router.push(`/events/${props.event.id}`)
  }
}
</script>

<style scoped>
.see-all-btn {
  background-color: var(--brand);
  color: #ffffff;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(36, 29, 29, 0.2);
}

.see-all-btn:hover {
  background-color: var(--brand-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(36, 29, 29, 0.3);
}
</style>
