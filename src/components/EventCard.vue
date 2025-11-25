<template>
  <div class="event-card" v-if="event">
      <img :src="event.image" :alt="event.alt">
      <div class="card-content">
          <h4 class="event-name">&nbsp;{{event.event_name}}</h4>
          <p class="community-name">&nbsp;{{event.community_name}}</p>
          <div class="event-detail location">
              <i class="fas fa-map-marker-alt"></i>
              <span>{{event.location}}</span>
          </div>
          <div class="event-detail time">
              <i class="fas fa-clock"></i>
              <span>{{event.date}}</span>
          </div>
      </div>
      <EventDialog :event="event" />                        
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
