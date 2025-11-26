<template>
  <div class="page-wrap">
    <div v-if="event" class="event-details-container">
      <button class="back-btn" @click="$router.go(-1)">
        <i class="fas fa-arrow-left"></i> Back
      </button>

      <div class="event-header">
        <h1>{{ event.name }}</h1>
        <span class="community-badge">{{ event.community_name }}</span>
      </div>

      <div class="event-content">
        <div class="image-container">
          <img :src="event.image" :alt="event.alt" class="event-image" />
        </div>

        <div class="info-container">
          <div class="info-card">
            <div class="info-row">
              <i class="fas fa-calendar"></i>
              <div>
                <strong>Date</strong>
                <p>{{ event.date }}</p>
              </div>
            </div>
            <div class="info-row">
              <i class="fas fa-clock"></i>
              <div>
                <strong>Time</strong>
                <p>{{ event.time }}</p>
              </div>
            </div>
            <div class="info-row">
              <i class="fas fa-map-marker-alt"></i>
              <div>
                <strong>Location</strong>
                <p>{{ event.location }}</p>
              </div>
            </div>
          </div>

          <div class="description-section">
            <h3>About this Event</h3>
            <p>{{ event.description || 'No description available.' }}</p>
          </div>

          <button 
            class="register-btn" 
            :class="{ 'registered': event.registered }"
            @click="toggleRegistration"
          >
            {{ event.registered ? 'Registered' : 'Register Now' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <h2>Event not found</h2>
      <button @click="$router.push('/events')">Go to Events</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store } from '../store.js'

const route = useRoute()
const router = useRouter()

const event = computed(() => {
  const id = parseInt(route.params.id)
  return store.events.find(e => e.id === id)
})

const toggleRegistration = () => {
  if (!event.value) return
  
  if (!localStorage.getItem('user_token')) {
    alert('Please login to register')
    router.push('/login')
    return
  }

  store.registerEvent(event.value)
}
</script>

<style scoped>
.page-wrap {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: 'Inter', sans-serif;
  color: #153226;
}

.back-btn {
  background: none;
  border: none;
  color: #6b7c74;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 0;
}

.back-btn:hover {
  color: #1b8f48;
}

.event-header {
  margin-bottom: 24px;
}

.event-header h1 {
  font-size: 32px;
  margin: 0 0 8px 0;
  color: #153226;
}

.community-badge {
  background: #e6f3e9;
  color: #1b8f48;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.event-content {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 40px;
}

.event-image {
  width: 100%;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.info-card {
  background: #ffffff;
  border: 1px solid #d8eadb;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}

.info-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-row i {
  font-size: 20px;
  color: #1b8f48;
  margin-top: 4px;
}

.info-row strong {
  display: block;
  font-size: 14px;
  color: #6b7c74;
  margin-bottom: 4px;
}

.info-row p {
  margin: 0;
  font-weight: 600;
  font-size: 16px;
}

.description-section h3 {
  font-size: 20px;
  margin-bottom: 12px;
}

.description-section p {
  line-height: 1.6;
  color: #4a5e53;
}

.register-btn {
  width: 100%;
  padding: 16px;
  background: #1b8f48;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 24px;
  transition: all 0.2s;
}

.register-btn:hover {
  background: #167a3d;
}

.register-btn.registered {
  background: #d8eadb;
  color: #1b8f48;
  cursor: pointer;
}

.not-found {
  text-align: center;
  padding: 60px;
}

@media (max-width: 768px) {
  .event-content {
    grid-template-columns: 1fr;
  }
}
</style>
