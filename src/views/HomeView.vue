<template>
  <Announcements/>
  <div class="content-wrapper">
      <Filters :filterChange="onFilterChange"/>
      <EventGrid :events="events" :seeAll ="seeAll" />
  </div>
  <!-- Global event detail dialog -->
  <el-dialog v-model="dialogVisible" width="90%" :title="selectedEvent?.event_name">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
      
      <div style="width: 45%;">
        <img 
          :src="selectedEvent.image" 
          :alt="selectedEvent.alt" 
          style="width: 100%; display: block; border-radius: 12px; object-fit: cover; border: 2px solid #1b8f48;"
        />
      </div>

      <div style="width: 50%; text-align: left;">
        <h2 style="margin-top: 0; color: #153226; font-size: 24px; margin-bottom: 16px;">{{ selectedEvent.event_name }}</h2>
        
        <div style="margin-bottom: 12px; color: #1b8f48; font-weight: bold; font-size: 16px;">
          📅 {{ selectedEvent.date }} at {{ selectedEvent.time }}
        </div>
        
        <div style="margin-bottom: 12px; color: #1b8f48; font-weight: bold; font-size: 16px;">
          📍 {{ selectedEvent.location }}
        </div>
        
        <div style="margin-bottom: 12px; color: #1b8f48; font-weight: bold; font-size: 16px;">
          👥 {{ selectedEvent.community_name }}
        </div>

        <p style="color: #6b7c74; line-height: 1.6; margin: 20px 0;">
          Join us for this exciting event! Don't miss out on this opportunity to connect with the community and participate in engaging activities.
        </p>

        <button 
          @click="dialogVisible = false"
          style="background: #1b8f48; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: 600; margin-top: 10px;"
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

// Reactive state for selected event and dialog visibility
const selectedEvent = ref(null)
const dialogVisible = ref(false)

const events = ref([])

const getUpcomingEvents = () => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return store.events.filter(e => new Date(e.date) >= today)
    .sort((a, b) => new Date(a.date) - new Date(b.date));
}

// Initialize with upcoming events
events.value = getUpcomingEvents();

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
</style>
