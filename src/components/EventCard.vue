<template>
  <div class="event-card" v-if="event">
      <div class="card-image-wrapper">
        <img :src="event.image" :alt="event.alt">
      </div>
      <div class="card-content">
          <div class="card-info">

            <h4 class="event-name">{{event.name}}</h4>
            <div class="event-detail location">
                <i class="fas fa-map-marker-alt"></i>
                <span>{{event.location}}</span>
            </div>
            <div class="event-detail time">
                <i class="fas fa-clock"></i>
                <span>{{event.time || '00:00'}}</span>
            </div>
          </div>
          <div class="card-actions">
            <EventDialog :event="event" />
          </div>
      </div>
  </div>
</template>

<script setup>
import EventDialog from './EventDialog.vue'

const props = defineProps({
  event: {
    type: Object
  },
  seeAll: {
    type: Function
  }
})
</script>

<style scoped>
/* Scoped styles can be used here if needed, but we are relying on global style.css for consistency */
/* However, for component-specific structure, we can add some here */

.card-content {
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
}

.card-actions {
  margin-top: auto;
}

.event-name {
  font-size: 14px;
  font-weight: 700;
  color: #555;
  margin: 0 0 8px 0; /* Added small bottom margin for spacing between title and details */
}

.community-name {
  margin-bottom: 16px;
  font-size: 14px; /* Optional: make it look like a label */
  color: #666; /* Optional: make it subtle */
  margin-top: 0;
}
</style>
