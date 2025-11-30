<template>
  <button class="see-all-btn" @click="dialogVisible = true">
      See All
  </button>
  <el-dialog
      v-model="dialogVisible"
      :title="event?.event_name"
      width="90%"
      class="event-detail-modal"
      append-to-body
  >
      <div class="event-details">
        <img v-if="event?.image" :src="event.image" :alt="event.alt" class="event-image" />
        
        <div class="info-column">
          <div class="detail-row">
            <i class="fas fa-users"></i>
            <strong>Community:</strong> {{ event?.community_name }}
          </div>
          
          <div class="detail-row">
            <i class="fas fa-map-marker-alt"></i>
            <strong>Location:</strong> {{ event?.location }}
          </div>
          
          <div class="detail-row">
            <i class="fas fa-calendar"></i>
            <strong>Date:</strong> {{ event?.date }}
          </div>
          
          <div class="detail-row">
            <i class="fas fa-clock"></i>
            <strong>Time:</strong> {{ event?.time }}
          </div>

          <p class="event-description">
            Join us for this exciting event! Don't miss out on this opportunity to connect with the community and participate in engaging activities.
          </p>
        </div>
      </div>
      
      <template #footer>
      <div class="dialog-footer">
          <el-button @click="dialogVisible = false">Close</el-button>
          <el-button type="primary" @click="registerForEvent">
          Register
          </el-button>
      </div>
      </template>
  </el-dialog>
  <ConfettiOverlay v-if="showCelebration" @close="showCelebration = false" />
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ConfettiOverlay from './ConfettiOverlay.vue'

const router = useRouter()

const props = defineProps({
  event: {
    type: Object,
    default: () => ({})
  }
})

const dialogVisible = ref(false)
const showCelebration = ref(false)

const registerForEvent = () => {
  // Check if user is logged in
  if (!localStorage.getItem('user_token')) {
    alert('Please sign in to register.')
    dialogVisible.value = false
    router.push('/login')
    return
  }
  
  // User is authenticated, proceed with registration
  // In a real app we would call store.registerEvent(props.event)
  // For now we just show the celebration
  showCelebration.value = true
  dialogVisible.value = false
}
</script>

<style scoped>
.event-details {
  padding: 8px 0;
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.event-image {
  flex: 0 0 45%;
  width: 45%;
  height: auto;
  object-fit: cover;
  border-radius: 12px;
  margin: 0;
  display: block;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
}

.info-column {
  flex: 1;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 15px;
  color: #153226;
}

.detail-row i {
  width: 20px;
  color: #1b8f48;
  text-align: center;
}

.detail-row strong {
  margin-right: 4px;
  color: #000;
}

.event-description {
  margin-top: 20px;
  font-size: 14px;
  line-height: 1.6;
  color: #6b7c74;
}

@media (max-width: 768px) {
  .event-details {
    flex-direction: column;
  }
  
  .event-image {
    width: 100%;
    flex: none;
    margin-bottom: 20px;
  }
}

/* Modal container styling */
:global(.event-detail-modal) {
  border-radius: 16px !important;
  overflow: hidden;
  max-width: 800px !important;
  width: 90% !important;
  margin-top: 8vh !important;
}

/* Modal header styling */
:global(.event-detail-modal .el-dialog__header) {
  background: #fefbea;
  padding: 20px 24px;
  border-bottom: none;
}

:global(.event-detail-modal .el-dialog__title) {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #153226;
}

/* Modal body styling */
:global(.event-detail-modal .el-dialog__body) {
  padding: 24px;
  background: #fefbea;
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

/* Modal footer styling */
:global(.event-detail-modal .el-dialog__footer) {
  background: #fefbea;
  padding: 16px 24px;
  border-top: none;
}

/* Close button styling */
:global(.event-detail-modal .el-dialog__headerbtn) {
  top: 20px;
  right: 20px;
}

:global(.event-detail-modal .el-dialog__close) {
  color: #6b7c74;
  font-size: 18px;
}

:global(.event-detail-modal .el-dialog__close:hover) {
  color: #1b8f48;
}

/* Button styling */
:global(.event-detail-modal .el-button--primary) {
  background-color: #1b8f48 !important;
  border-color: #1b8f48 !important;
  border-radius: 8px;
  font-weight: 600;
  padding: 10px 20px;
}

:global(.event-detail-modal .el-button--primary:hover) {
  background-color: #167a3d !important;
  border-color: #167a3d !important;
}

:global(.event-detail-modal .el-button--default) {
  border-radius: 8px;
  border-color: #dcdfe6;
  color: #606266;
}

:global(.event-detail-modal .el-button--default:hover) {
  border-color: #c6e2d9;
  color: #1b8f48;
  background-color: #f0f9eb;
}

/* See All button styling */
.see-all-btn {
  background-color: #2E8540;
  color: #ffffff;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(46, 133, 64, 0.2);
}

.see-all-btn:hover {
  background-color: #167a3d;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(46, 133, 64, 0.3);
}
</style>
