<template>
  <main class="page-wrap">
    <!-- HEADER ROW -->
    <section class="events-header">
      <div>
        <h1 class="events-title">Events</h1>
        <p class="events-subtitle">
          Explore upcoming events and manage your registrations.
        </p>
      </div>

      <!-- BACKEND SHOULD ONLY RENDER THIS FOR ADMINS -->
      <button v-if="isAdmin" id="openCreateEventModal" class="primary-btn" @click="openModal('create')">
        + Create Event
      </button>
    </section>

    <!-- FILTERS -->
    <section class="events-filters">
      <div class="filters-pills">
        <button 
          class="filter-pill" 
          :class="{ 'is-active': activeFilter === 'upcoming' }" 
          @click="activeFilter = 'upcoming'"
        >Upcoming</button>
        <button 
          class="filter-pill" 
          :class="{ 'is-active': activeFilter === 'past' }" 
          @click="activeFilter = 'past'"
        >Past</button>
        <button 
          class="filter-pill" 
          :class="{ 'is-active': activeFilter === 'all' }" 
          @click="activeFilter = 'all'"
        >All</button>
      </div>
    </section>

    <!-- EVENTS LIST -->
    <section class="events-list" id="eventsList">
      <article 
        v-for="event in filteredEvents" 
        :key="event.id" 
        class="event-card"
      >
        <div class="event-date-pill">
          <span class="event-date-day">{{ getDay(event.date) }}</span>
          <span class="event-date-month">{{ getMonth(event.date) }}</span>
        </div>

        <div class="event-main">
          <h2 class="event-name">{{ event.name }}</h2>
          <p class="event-desc">{{ event.description }}</p>
          <div class="event-meta">
            <span><i class="fas fa-location-dot"></i> {{ event.location }}</span>
            <span><i class="fas fa-users"></i> {{ event.capacity }} seats</span>
            <span><i class="fas fa-users-viewfinder"></i> {{ event.club }}</span>
          </div>
        </div>

        <div class="event-actions">
          <button 
            class="event-primary-btn" 
            @click="register(event)"
          >
            {{ event.registered ? 'Registered' : 'Register' }}
          </button>

          <button v-if="isAdmin" class="event-edit-btn" type="button" @click="openModal('edit', event)">
            <i class="fas fa-pen"></i> Edit
          </button>
          
          <button v-if="isAdmin" class="event-delete-btn" type="button" @click="deleteEvent(event)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </article>
      
      <div v-if="filteredEvents.length === 0" style="text-align:center; color:var(--muted); padding:20px;">
        No events found.
      </div>
    </section>
  </main>

  <!-- CREATE / EDIT EVENT MODAL -->
  <div class="modal-overlay" :class="{ 'is-open': isModalOpen }" aria-hidden="true" @click.self="closeModal">
    <div class="modal-card">
      <button class="modal-close" aria-label="Close" @click="closeModal">
        <span>&times;</span>
      </button>

      <h2 class="modal-title">{{ modalMode === 'create' ? 'Create Event' : 'Edit Event' }}</h2>

      <div class="modal-upload-label">Upload Image</div>
      <div class="modal-upload-box">
        <div class="upload-icon">
          <i class="fas fa-upload"></i>
        </div>
        <p class="upload-text">Max 120 MB, PNG, JPEG</p>
        <label class="upload-btn">
          Browse File
          <input type="file" hidden />
        </label>
      </div>

      <form @submit.prevent="submitForm" class="modal-form">
        <h3 class="form-section-title">Main Details</h3>

        <div class="form-row">
          <div class="form-field">
            <label>Event Name</label>
            <input type="text" v-model="formData.name" required />
          </div>

          <div class="form-field">
            <label>Date</label>
            <input type="date" v-model="formData.date" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-field">
            <label>Location</label>
            <input type="text" v-model="formData.location" />
          </div>

          <div class="form-field">
            <label>Club</label>
            <select v-model="formData.club">
              <option value="">Select a club</option>
              <option v-for="club in CLUBS" :key="club" :value="club">{{ club }}</option>
            </select>
          </div>
        </div>

        <div class="form-field">
          <label>Capacity</label>
          <input type="number" v-model="formData.capacity" min="0" />
        </div>

        <div class="form-field">
          <label>Description</label>
          <textarea v-model="formData.description" rows="4"></textarea>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="closeModal">
            Cancel
          </button>
          <button type="submit" class="btn-primary">
            {{ modalMode === 'create' ? 'Submit' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </div>
  </div>
  
  <ConfettiOverlay v-if="showCelebration" @close="showCelebration = false" />
</template>
<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store } from '../store.js'
import ConfettiOverlay from '../components/ConfettiOverlay.vue'

const route = useRoute()
const router = useRouter()
const showCelebration = ref(false)

const CLUBS = [
  "Computer Science Club",
  "Engineering Society",
  "Alumni Association",
  "Career Services"
];

// Admin state
const isAdmin = ref(false);

// Filters
const activeFilter = ref('upcoming');

// Filtered events logic
const filteredEvents = computed(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  let events = store.events;

  // 1. Filter by route query "registered" if present
  if (route.query.filter === 'registered') {
    events = events.filter(e => e.registered);
  }

  // 2. Filter by active pill (upcoming/past/all)
  return events.filter(event => {
    const eventDate = new Date(event.date);
    const isPast = eventDate < today;
    
    if (activeFilter.value === 'upcoming') return !isPast;
    if (activeFilter.value === 'past') return isPast;
    return true; // all
  }).sort((a, b) => new Date(a.date) - new Date(b.date));
});

onMounted(() => {
  if (localStorage.getItem('user_token')) {
    const role = localStorage.getItem('user_role');
    isAdmin.value = role === 'admin' || role === 'super_admin';
  } else {
    isAdmin.value = false;
  }
  
  // Apply initial filter from route
  if (route.query.filter === 'upcoming') {
    activeFilter.value = 'upcoming';
  } else if (route.query.filter === 'registered') {
    activeFilter.value = 'all'; // Show all registered
  }
});

watch(() => route.query.filter, (newVal) => {
   if (newVal === 'upcoming') {
    activeFilter.value = 'upcoming';
  } else if (newVal === 'registered') {
    activeFilter.value = 'all';
  }
});

// Date Helpers
const getDay = (dateStr) => {
  const date = new Date(dateStr);
  return date.getDate().toString().padStart(2, '0');
}

const getMonth = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString('default', { month: 'short' }).toUpperCase();
}

// Modal Logic
const isModalOpen = ref(false);
const modalMode = ref('create'); // 'create' or 'edit'
const formData = reactive({
  id: null,
  name: '',
  date: '',
  location: '',
  club: '',
  capacity: '',
  description: ''
});

const openModal = (mode, event = null) => {
  modalMode.value = mode;
  if (mode === 'edit' && event) {
    formData.id = event.id;
    formData.name = event.name;
    formData.date = event.date;
    formData.location = event.location;
    formData.club = event.club;
    formData.capacity = event.capacity;
    formData.description = event.description;
  } else {
    // Reset form
    formData.id = null;
    formData.name = '';
    formData.date = '';
    formData.location = '';
    formData.club = '';
    formData.capacity = '';
    formData.description = '';
  }
  isModalOpen.value = true;
  document.body.style.overflow = 'hidden';
}

const closeModal = () => {
  isModalOpen.value = false;
  document.body.style.overflow = '';
}

const submitForm = () => {
  if (modalMode.value === 'create') {
    store.createEvent({
      name: formData.name,
      date: formData.date,
      location: formData.location,
      club: formData.club,
      capacity: formData.capacity,
      description: formData.description,
      // Default image for now
      image: 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=800&q=80'
    });
  } else {
    store.updateEvent({
      id: formData.id,
      name: formData.name,
      date: formData.date,
      location: formData.location,
      club: formData.club,
      capacity: formData.capacity,
      description: formData.description
    });
  }
  closeModal();
}

const deleteEvent = (event) => {
  if (confirm('Are you sure you want to delete this event?')) {
    store.deleteEvent(event.id);
  }
}

const register = (event) => {
  // Check if user is logged in
  if (!localStorage.getItem('user_token')) {
    alert('Please sign in to register.')
    router.push('/login')
    return
  }
  
  // User is authenticated, proceed with registration
  store.registerEvent(event);
  
  // If registration was successful (it toggles, so check if it's now true)
  // Note: store.registerEvent modifies the object in place.
  if (event.registered) {
    showCelebration.value = true;
  }
}
</script>

<style scoped>
/* ========= PAGE WRAP ========= */

.page-wrap {
  max-width: 1180px;
  margin: 18px auto 56px;
  padding: 0 20px 40px;
}

/* ========= HEADER + FILTERS ========= */

.events-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.events-title {
  font-size: 22px;
  font-weight: 700;
}

.events-subtitle {
  font-size: 13px;
  color: var(--muted);
  margin-top: 4px;
}

/* create button */

.primary-btn {
  border: none;
  border-radius: 6px;
  background: var(--brand);
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 18px;
  cursor: pointer;
}

.events-filters {
  margin-bottom: 16px;
}

.filters-pills {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.filter-pill {
  border-radius: 20px;
  border: 1px solid var(--outline);
  background: #f7fbf8;
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 500;
  color: #345243;
  cursor: pointer;
}

.filter-pill.is-active {
  border-color: var(--brand);
  background: #e1f3e3;
}

/* ========= EVENT CARDS ========= */

.events-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.event-card {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr) auto; /* Extremely reduced first column */
  align-items: center;
  background: var(--card);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 6px 10px; /* Minimal padding */
}

/* date pill */

.event-date-pill {
  width: 36px; /* Micro pill */
  height: 36px;
  border-radius: 6px;
  background: #f3f6e9;
  border: 1px solid #d7dfc2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  font-weight: 700;
  color: #31402b;
}

.event-date-day {
  font-size: 13px;
  line-height: 1;
}

.event-date-month {
  font-size: 7px;
  letter-spacing: 0.5px;
  line-height: 1;
}

/* middle */

.event-main {
  display: flex;
  flex-direction: column;
  gap: 0;
  justify-content: center;
}

.event-name {
  font-size: 13px; /* Small title */
  font-weight: 700;
  line-height: 1.2;
}

.event-desc {
  font-size: 10px; /* Tiny desc */
  color: var(--muted);
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.event-meta {
  margin-top: 1px;
  font-size: 9px; /* Micro meta */
  color: #556b5f;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.event-meta i {
  margin-right: 2px;
}

/* right */

.event-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  margin-left: 6px;
  justify-content: center;
}

.event-primary-btn {
  border-radius: 20px;
  border: none;
  background: var(--brand);
  color: #ffffff;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 16px;
  cursor: pointer;
}

.event-primary-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.event-edit-btn {
  border-radius: 20px;
  border: 1px solid var(--outline);
  background: #f7fbf8;
  color: #34493a;
  font-size: 12px;
  padding: 4px 10px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.event-delete-btn {
  border-radius: 20px;
  border: 1px solid #fee2e2;
  background: #fff5f5;
  color: #dc2626;
  font-size: 12px;
  padding: 4px 10px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

/* ========= MODAL ========= */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-overlay.is-open {
  display: flex;
}

.modal-card {
  width: 420px;
  max-width: 95%;
  background: #fefbea;
  border-radius: 18px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2);
  padding: 20px 22px 18px;
  position: relative;
}

/* close button */

.modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 30px;
  height: 30px;
  border-radius: 999px;
  border: 1px solid #ffcc7a;
  background: #fff4e1;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.modal-close span {
  font-size: 18px;
  line-height: 1;
  color: #f08c00;
}

/* titles */

.modal-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 4px;
}

.modal-upload-label {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 6px;
}

/* upload box */

.modal-upload-box {
  border-radius: 10px;
  border: 1px dashed #cfd5c9;
  background: #f8faef;
  padding: 24px 16px 18px;
  text-align: center;
  margin-bottom: 16px;
}

.upload-icon {
  font-size: 22px;
  color: #707b82;
  margin-bottom: 8px;
}

.upload-text {
  font-size: 12px;
  color: #909aa0;
  margin-bottom: 10px;
}

.upload-btn {
  display: inline-block;
  border-radius: 20px;
  background: #3b4450;
  color: white;
  font-size: 12px;
  padding: 7px 22px;
  cursor: pointer;
}

/* form */

.modal-form {
  font-size: 12px;
}

.form-section-title {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 8px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 8px;
}

.form-field label {
  font-size: 11px;
  color: #777f7a;
}

/* inputs + select */

.modal-form input,
.modal-form textarea,
.modal-form select {
  border-radius: 4px;
  border: 1px solid #dadfd4;
  padding: 6px 8px;
  font-size: 12px;
  font-family: inherit;
  outline: none;
  background: #ffffff;
}

.modal-form input:focus,
.modal-form textarea:focus,
.modal-form select:focus {
  border-color: var(--brand);
}

/* buttons */

.modal-actions {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.btn-secondary,
.btn-primary {
  font-size: 13px;
  font-weight: 600;
  border-radius: 4px;
  border: none;
  padding: 8px 18px;
  cursor: pointer;
  flex: 1;
}

.btn-secondary {
  background: #e4e4e0;
  color: #333;
}

.btn-primary {
  background: var(--brand);
  color: #ffffff;
}

/* Responsive */
@media (max-width: 1200px) {
  .events-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .event-card {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .event-main {
    flex: 1;
    margin: 10px 0;
  }
  
  .event-card {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    gap: 10px;
    height: auto; /* Allow height to fit content */
    padding: 16px;
  }
  
  .event-date-pill {
    grid-column: 1;
    grid-row: 1;
    margin-right: 0;
  }
  
  .event-main {
    grid-column: 2;
    grid-row: 1;
    margin: 0;
  }
  
  .event-actions {
    grid-column: 1 / -1;
    grid-row: 2;
    flex-direction: row;
    justify-content: flex-end;
    width: 100%;
    margin-left: 0;
    margin-top: 10px;
    gap: 8px;
  }
}

@media (max-width: 768px) {
  .events-list {
    grid-template-columns: 1fr;
  }

  .nav-inner {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .nav-center {
    order: 3;
  }

  .nav-right {
    order: 2;
    justify-content: flex-start;
  }
}

@media (max-width: 640px) {
  .page-wrap {
    margin: 18px auto 32px;
    padding: 0 14px 30px;
  }

  .event-date-pill {
    margin-bottom: 10px;
  }
}
</style>
