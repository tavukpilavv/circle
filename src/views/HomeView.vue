<template>
  <Announcements/>
  <div class="content-wrapper container">
      <Filters 
        :filterChange="onFilterChange" 
        v-model:activeType="activeType"
      />
      
      <EventGrid 
        v-if="activeType === 'events'" 
        :events="events" 
        :seeAll="seeAll" 
      />
      
      <CommunityGrid 
        v-else 
        :communities="store.communities" 
      />
  </div>
  <!-- Global event detail dialog -->
  <el-dialog 
    v-model="dialogVisible" 
    width="90%" 
    style="max-width: 800px; border-radius: 16px; overflow: hidden;"
    :show-close="true"
    :close-on-click-modal="true"
    :close-on-press-escape="true"
    :lock-scroll="true"
    class="event-detail-modal"
  >
    <template #header="{ close, titleId, titleClass }">
      <div class="my-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h4 :id="titleId" :class="titleClass" style="margin: 0; font-size: 20px; font-weight: 700; color: #153226;">{{ selectedEvent?.event_name }}</h4>
      </div>
    </template>
    <div class="dialog-content-wrapper">
      
      <div class="dialog-image-container">
        <img 
          :src="selectedEvent.image" 
          :alt="selectedEvent.alt" 
          class="dialog-image"
        />
      </div>

      <div class="dialog-text-container">
        
        <div class="detail-row">
          <i class="fas fa-calendar"></i> 
          <strong>Date:</strong> {{ selectedEvent.date }} at {{ selectedEvent.time }}
        </div>
        
        <div class="detail-row">
          <i class="fas fa-location-dot"></i> 
          <strong>Location:</strong> {{ selectedEvent.location }}
        </div>
        
        <div class="detail-row">
          <i class="fas fa-users"></i> 
          <strong>Community:</strong> {{ selectedEvent.community_name }}
        </div>

        <p style="color: #6b7c74; line-height: 1.6; margin: 20px 0; font-size: 15px;">
          Join us for this exciting event! Don't miss out on this opportunity to connect with the community and participate in engaging activities.
        </p>

        <button 
          @click="dialogVisible = false"
          style="background: #1b8f48; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: 600; margin-top: 10px; width: 100%;"
        >
          Close
        </button>
      </div>

    </div>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import moment from 'moment'
import { store } from '../store.js'
import Announcements from '../components/Announcements.vue'
import Filters from '../components/Filters.vue'
import EventGrid from '../components/EventGrid.vue'
import CommunityGrid from '../components/CommunityGrid.vue'

// Reactive state for selected event and dialog visibility
const selectedEvent = ref(null)
const dialogVisible = ref(false)
const activeType = ref('events')

const events = ref([])

const getUpcomingEvents = () => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return store.events.filter(e => new Date(e.date) >= today)
    .sort((a, b) => new Date(a.date) - new Date(b.date));
}

const getAllEvents = () => {
  return [...store.events].sort((a, b) => new Date(a.date) - new Date(b.date));
}

// Initialize with all events
events.value = getAllEvents();

const seeAll = (event) => {
  // Open the global dialog with the clicked event's details
  selectedEvent.value = event
  dialogVisible.value = true
}

const onFilterChange = (val) => {
  if (!val) {
    // Reset to default (Upcoming)
    events.value = getUpcomingEvents();
  } else {
    let startDate = moment(val[0]).format("YYYY-MM-DD")
    let endDate = moment(val[1]).format("YYYY-MM-DD")
    let newList = store.events.filter(item => {
      return item.date >= startDate && item.date <= endDate
    }).sort((a, b) => new Date(a.date) - new Date(b.date));
    events.value = newList;
  }
}
</script>

<style scoped>
/* Dialog content layout - side by side */
.dialog-content-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

/* Image container on the left */
.dialog-image-container {
  width: 40%;
  flex-shrink: 0;
}

.dialog-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}

/* Text container on the right */
.dialog-text-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  font-size: 16px;
  line-height: 1.6;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-row i {
  color: #1b8f48;
  width: 20px;
}

.detail-row strong {
  margin-right: 8px;
}

/* Responsive: stack vertically on smaller screens */
@media (max-width: 768px) {
  .dialog-content-wrapper {
    flex-direction: column;
  }
  
  .dialog-image-container {
    width: 100%;
  }
}

/* Carousel indicator buttons - make them thicker and more visible */
:deep(.el-carousel__button) {
  width: 40px !important;
  height: 8px !important;
  border-radius: 4px !important;
  opacity: 0.8 !important;
  background-color: #ffffff !important;
}

:deep(.el-carousel__indicator.is-active .el-carousel__button) {
  opacity: 1 !important;
  background-color: #1b8f48 !important;
}

/* Responsive: smaller indicators on mobile */
@media (max-width: 768px) {
  :deep(.el-carousel__button) {
    width: 12px !important;
    height: 6px !important;
    border-radius: 3px !important;
  }
}
</style>
