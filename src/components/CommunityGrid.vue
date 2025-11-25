<template>
  <section class="community-grid" v-if="communities.length > 0">
      <CommunityCard v-for="community in communities" :community="community" :key="community.id" />
  </section>
  <div v-else>
      <el-alert title="No Communities Available" type="warning" />
  </div>
</template>

<script setup>
import CommunityCard from './CommunityCard.vue'

const props = defineProps({
  communities: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.community-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
