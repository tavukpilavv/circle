<template>
  <div class="button-wrapper">
    <button class="see-all-btn" @click="dialogVisible = true">
        See All
    </button>
  </div>    
  <el-dialog
      v-model="dialogVisible"
      :title="event?.event_name"
      width="90%"
      class="full-screen-modal"
      append-to-body
  >
      <div class="event-details">
        <img v-if="event?.image" :src="event.image" :alt="event.alt" class="event-image" />
        
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
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  event: {
    type: Object,
    default: () => ({})
  }
})

const dialogVisible = ref(false)

const registerForEvent = () => {
  // Check if user is logged in
  if (!localStorage.getItem('user_token')) {
    alert('Lütfen katılmak için önce giriş yapın!')
    dialogVisible.value = false
    router.push('/login')
    return
  }
  
  // User is authenticated, proceed with registration
  alert(`Successfully registered for ${props.event?.event_name}!`)
  dialogVisible.value = false
}
</script>

<style scoped>
.event-details {
  padding: 8px 0;
}

.event-image {
  max-width: 600px;
  max-height: 400px;
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 16px;
  margin: 0 auto 20px;
  display: block;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
}

.detail-row i {
  width: 20px;
  color: #1b8f48;
}

.detail-row strong {
  margin-right: 4px;
}

/* Modal container styling */
:global(.full-screen-modal) {
  display: flex;
  flex-direction: column;
  margin: 0 !important;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90vw !important;
  height: 90vh !important;
  max-width: 90vw !important;
  max-height: 90vh !important;
  border-radius: 16px !important;
  overflow: hidden;
}

/* Modal header styling */
:global(.full-screen-modal .el-dialog__header) {
  background: #fefbea;
  padding: 20px 24px;
  border-bottom: 1px solid #d8eadb;
}

:global(.full-screen-modal .el-dialog__title) {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #153226;
}

/* Modal body styling */
:global(.full-screen-modal .el-dialog__body) {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #fefbea;
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

/* Modal footer styling */
:global(.full-screen-modal .el-dialog__footer) {
  background: #fefbea;
  padding: 16px 24px;
  border-top: 1px solid #d8eadb;
}

/* Close button styling */
:global(.full-screen-modal .el-dialog__headerbtn) {
  top: 20px;
  right: 20px;
  width: 32px;
  height: 32px;
  font-size: 18px;
}

:global(.full-screen-modal .el-dialog__close) {
  color: #1b8f48;
  font-weight: bold;
}

:global(.full-screen-modal .el-dialog__close:hover) {
  color: #167a3d;
}

/* Button styling */
:global(.full-screen-modal .el-button--primary) {
  background-color: #1b8f48 !important;
  border-color: #1b8f48 !important;
  border-radius: 6px;
  font-weight: 600;
}

:global(.full-screen-modal .el-button--primary:hover) {
  background-color: #167a3d !important;
  border-color: #167a3d !important;
}

:global(.full-screen-modal .el-button--default) {
  border-radius: 6px;
  border-color: #d8eadb;
  color: #153226;
}


:global(.full-screen-modal .el-button--default:hover) {
  border-color: #1b8f48;
  color: #1b8f48;
}

/* Button wrapper for alignment */
.button-wrapper {
  padding: 0 20px 20px 20px;
  display: flex;
  justify-content: flex-end;
}

/* See All button styling */
.see-all-btn {
  background-color: #E6F3E9;
  color: #2E8540;
  border: none;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.see-all-btn:hover {
  background-color: #2E8540;
  color: #ffffff;
}
</style>
