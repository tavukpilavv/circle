<template>
  <div class="page-wrap">
    <div v-if="event" class="event-details-container">
      <button class="back-btn" @click="$router.go(-1)">
        <i class="fas fa-arrow-left"></i> Back
      </button>

      <!-- Static Header: Title & Image -->
      <div class="event-header">
        <h1>{{ event.name }}</h1>
        <span class="community-badge">{{ event.community_name }}</span>
      </div>

      <div class="image-container">
        <img :src="event.image" :alt="event.alt" class="event-image" />
      </div>

      <!-- Tab Controls -->
      <div class="tab-controls">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'details' }"
          @click="activeTab = 'details'"
        >
          About Event
        </button>
        <button 
          v-if="isPastEvent"
          class="tab-btn" 
          :class="{ active: activeTab === 'reviews' }"
          @click="activeTab = 'reviews'"
        >
          Reviews & Ratings
        </button>
      </div>

      <!-- Content Sections -->
      <div class="content-area">
        <!-- Tab 1: About Event -->
        <div v-if="activeTab === 'details'" id="details-content" class="fade-in">
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

          <template v-if="!isPastEvent">
            <button 
              class="register-btn" 
              :class="{ 'registered': event.registered, 'is-loading': isRegistering }"
              @click="toggleRegistration"
              :disabled="isRegistering"
            >
              <span v-if="isRegistering">
                <i class="fas fa-spinner fa-spin"></i> Processing...
              </span>
              <span v-else>
                {{ event.registered ? 'Registered' : 'Register Now' }}
              </span>
            </button>
          </template>
          <button 
            v-else
            class="register-btn event-ended" 
            disabled
          >
            Event Ended
          </button>
        </div>

        <!-- Tab 2: Reviews & Ratings -->
        <div v-if="activeTab === 'reviews' && isPastEvent" id="reviews-content" class="fade-in">
          <div class="reviews-summary">
            <div class="rating-score">
              <span class="score">4.8</span>
              <div class="stars">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star-half-alt"></i>
              </div>
              <span class="count">Based on 128 reviews</span>
            </div>
            
            <div class="summary-actions">
              <div class="trustpilot-badge">
                <i class="fas fa-star" style="color: #00b67a;"></i> Trustpilot
              </div>
              <button class="write-review-btn" @click="showRatingPopup = true">
                Write a Review
              </button>
            </div>
          </div>

          <div class="reviews-list">
            <div v-for="review in reviews" :key="review.id" class="review-card">
              <div class="review-header">
                <div class="reviewer-info">
                  <div class="avatar">{{ review.user.charAt(0) }}</div>
                  <div>
                    <span class="name">{{ review.user }}</span>
                    <span class="date">{{ review.date }}</span>
                  </div>
                </div>
                <div class="review-meta">
                  <div v-if="review.isCurrentUser" class="review-actions">
                    <button class="action-btn edit-btn" title="Edit Review">
                      <i class="fas fa-pen"></i>
                    </button>
                    <button class="action-btn delete-btn" title="Delete Review" @click="deleteReview(review.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                  <div class="review-stars">
                    <i v-for="n in 5" :key="n" class="fas fa-star" :class="{ filled: n <= review.rating }"></i>
                  </div>
                </div>
              </div>
              <p class="review-text">{{ review.comment }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <h2>Event not found</h2>
      <button @click="$router.push('/events')">Go to Events</button>
    </div>
    <ConfettiOverlay v-if="showCelebration" @close="showCelebration = false" />
    <RatingPopup 
      v-if="event"
      v-model="showRatingPopup" 
      :event="event"
      @submit="handleRatingSubmit"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store } from '../store.js'
import ConfettiOverlay from '../components/ConfettiOverlay.vue'
import RatingPopup from '../components/RatingPopup.vue'
import { useToast } from "vue-toastification";

const route = useRoute()
const router = useRouter()
const toast = useToast()

const showCelebration = ref(false)
const showRatingPopup = ref(false)
const activeTab = ref('details')
const isRegistering = ref(false)

const event = computed(() => {
  const id = parseInt(route.params.id)
  return store.events.find(e => e.id === id)
})

const isPastEvent = computed(() => {
  if (!event.value?.date) return false
  const eventDate = new Date(event.value.date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return eventDate < today
})

// Fetch reviews from store
const reviews = computed(() => {
  if (!event.value) return []
  return store.getReviewsByEventId(event.value.id)
})

const toggleRegistration = async () => {
  if (!event.value) return
  
  if (!localStorage.getItem('user_token')) {
    toast.warning('Please sign in to register.')
    router.push('/login')
    return
  }

  isRegistering.value = true

  try {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))

    store.registerEvent(event.value)
    
    if (event.value.registered) {
      toast.success("Successfully registered for the event! 🎉")
      showCelebration.value = true
    } else {
      toast.info("Unregistered from event.")
    }
  } catch (error) {
    toast.error("Failed to join. Please try again.")
    console.error(error)
  } finally {
    isRegistering.value = false
  }
}

const handleRatingSubmit = (data) => {
  if (!event.value) return

  store.addReview({
    eventId: event.value.id,
    user: data.isAnonymous ? 'Incognito User' : 'You', // In real app, get from user store
    rating: data.rating,
    comment: data.feedback,
    isCurrentUser: true, // Mark as current user's review
    isAnonymous: data.isAnonymous
  })
  
  showRatingPopup.value = false
}

const deleteReview = (id) => {
  if (confirm('Are you sure you want to delete your review?')) {
    store.deleteReview(id)
  }
}
</script>

<style scoped>
.page-wrap {
  max-width: 800px; /* Narrower for better reading experience */
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
  text-align: center; /* Center header info */
}

.event-header h1 {
  font-size: 32px;
  margin: 0 0 12px 0;
  color: #153226;
}

.community-badge {
  background: #e6f3e9;
  color: #1b8f48;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  display: inline-block;
}

.image-container {
  margin-bottom: 32px;
}

.event-image {
  width: 100%;
  height: 300px; /* Fixed height for consistency */
  object-fit: cover;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* Tab Controls */
.tab-controls {
  display: flex;
  justify-content: center;
  gap: 40px;
  border-bottom: 2px solid #eef2f0;
  margin-bottom: 32px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 16px 8px;
  font-size: 16px;
  font-weight: 600;
  color: #6b7c74;
  cursor: pointer;
  position: relative;
  transition: color 0.3s;
}

.tab-btn:hover {
  color: #153226;
}

.tab-btn.active {
  color: #1b8f48;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #1b8f48;
  border-radius: 2px;
}

/* Content Area */
.content-area {
  min-height: 300px;
}

.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Details Tab Styles */
.info-card {
  background: #ffffff;
  border: 1px solid #d8eadb;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Horizontal layout for info */
  gap: 24px;
}

.info-row {
  display: flex;
  flex-direction: column; /* Stack icon and text */
  align-items: center;
  text-align: center;
  gap: 12px;
  margin-bottom: 0;
}

.info-row i {
  font-size: 24px;
  color: #1b8f48;
  background: #e6f3e9;
  padding: 12px;
  border-radius: 50%;
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
  font-size: 22px;
  margin-bottom: 16px;
  color: #153226;
}

.description-section p {
  line-height: 1.8;
  color: #4a5e53;
  font-size: 16px;
}

.register-btn {
  width: 100%;
  padding: 18px;
  background: #1b8f48;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 40px;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(27, 143, 72, 0.2);
}

.register-btn:hover {
  background: #167a3d;
  transform: translateY(-2px);
}

.register-btn.registered {
  background: #d8eadb;
  color: #1b8f48;
  box-shadow: none;
  cursor: default;
}

.register-btn.event-ended {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
  box-shadow: none;
}

/* Reviews Tab Styles */
.reviews-summary {
  background: #f8fcf9;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #eef2f0;
}

.rating-score {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rating-score .score {
  font-size: 36px;
  font-weight: 800;
  color: #153226;
  line-height: 1;
}

.rating-score .stars {
  color: #fbbf24;
  font-size: 14px;
}

.rating-score .count {
  font-size: 14px;
  color: #6b7c74;
}

.summary-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.trustpilot-badge {
  font-weight: 600;
  color: #153226;
  display: flex;
  align-items: center;
  gap: 8px;
}

.write-review-btn {
  background: #1b8f48;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.write-review-btn:hover {
  background: #167a3d;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-card {
  background: white;
  border: 1px solid #eef2f0;
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.2s;
}

.review-card:hover {
  border-color: #d8eadb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  background: #e6f3e9;
  color: #1b8f48;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.reviewer-info .name {
  display: block;
  font-weight: 600;
  color: #153226;
}

.reviewer-info .date {
  font-size: 12px;
  color: #9ca3af;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.review-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  font-size: 14px;
  color: #9ca3af;
  transition: color 0.2s;
}

.action-btn:hover {
  color: #153226;
}

.delete-btn:hover {
  color: #ef4444; /* Red color for delete */
}

.review-stars {
  color: #e5e7eb;
  font-size: 14px;
}

.review-stars .filled {
  color: #fbbf24;
}

.review-text {
  color: #4a5e53;
  line-height: 1.6;
  margin: 0;
}

.not-found {
  text-align: center;
  padding: 60px;
}

@media (max-width: 768px) {
  .info-card {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .info-row {
    flex-direction: row;
    text-align: left;
  }
  
  .event-image {
    height: 200px;
  }
}
</style>
