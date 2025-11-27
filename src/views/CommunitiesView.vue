<template>
  <main class="page-wrap">
    <!-- Intro text -->
    <section class="intro">
      <p class="intro-text">
        Connect with communities and explore new groups
      </p>

      <!-- big "Search communities..." bar -->
      <div class="community-search-shell">
        <i class="fas fa-search" aria-hidden="true"></i>
        <input
          v-model="searchQuery"
          id="communitySearchInput"
          type="search"
          placeholder="Search communities..."
          aria-label="Search communities"
        />
      </div>

      <!-- filter pills -->
      <div class="filters-row">
        <div class="filters-label-space"></div>
        <div class="filters-pills">
          <button
            class="filter-pill"
            :class="{ 'is-active': activeFilter === 'all', 'primary': activeFilter === 'all' }"
            type="button"
            @click="activeFilter = 'all'"
          >
            All
          </button>
          <button
            class="filter-pill"
            :class="{ 'is-active': activeFilter === 'joined', 'primary': activeFilter === 'joined' }"
            type="button"
            @click="activeFilter = 'joined'"
          >
            Joined
          </button>
          <button
            class="filter-pill"
            :class="{ 'is-active': activeFilter === 'discover', 'primary': activeFilter === 'discover' }"
            type="button"
            @click="activeFilter = 'discover'"
          >
            Discover
          </button>
          
          <button v-if="isSuperAdmin" class="add-club-btn" @click="openModal">
            + Add Club
          </button>
        </div>

      </div>
    </section>

    <!-- Communities list -->
    <section class="community-list" id="communityList">
      <article
        v-for="community in filteredCommunities"
        :key="community.name"
        class="community-card"
      >
        <img
          class="community-image"
          :src="community.image"
          alt=""
        />

        <div class="community-main">
          <h2 class="community-name">{{ community.name }}</h2>
          <p class="community-desc">
            {{ community.description }}
          </p>
          <div class="community-meta">
            <span><i class="fas fa-user-group"></i> {{ community.members }} members</span>
          </div>
        </div>

        <button 
          class="status-pill" 
          :class="community.joined ? 'joined' : 'outline'"
          type="button"
          @click="toggleJoin(community)"
        >
          <i v-if="community.joined" class="fas fa-check"></i>
          {{ community.joined ? 'Joined' : 'Join Community' }}
        </button>
      </article>
      
      <div v-if="filteredCommunities.length === 0" class="no-results">
        No communities found matching your criteria.
      </div>
    </section>
  </main>

  <!-- ADD CLUB MODAL -->
  <div class="modal-overlay" :class="{ 'is-open': isModalOpen }" aria-hidden="true" @click.self="closeModal">
    <div class="modal-card">
      <button class="modal-close" aria-label="Close" @click="closeModal">
        <span>&times;</span>
      </button>

      <h2 class="modal-title">Create Club</h2>

      <form @submit.prevent="submitClub" class="modal-form">
        <div class="form-field">
          <label>Club Name</label>
          <input type="text" v-model="formData.name" required />
        </div>

        <div class="form-field">
          <label>Description</label>
          <textarea v-model="formData.description" rows="3" required></textarea>
        </div>

        <div class="form-field">
          <label>Image URL</label>
          <input type="text" v-model="formData.image" placeholder="https://..." />
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="closeModal">
            Cancel
          </button>
          <button type="submit" class="btn-primary">
            Create Club
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { store } from '../store.js'

const router = useRouter()
const route = useRoute()
const searchQuery = ref('')
const activeFilter = ref('all')
const isSuperAdmin = ref(false)

// Modal State
const isModalOpen = ref(false)
const formData = reactive({
  name: '',
  description: '',
  image: ''
})

const applyFilters = () => {
  if (route.query.filter === 'joined') {
    activeFilter.value = 'joined'
  } else {
    activeFilter.value = 'all'
  }
}

onMounted(() => {
  applyFilters()
  
  // Check for Super Admin role
  const role = localStorage.getItem('user_role')
  isSuperAdmin.value = role === 'super_admin'
})

watch(() => route.query.filter, () => {
  applyFilters()
})

const filteredCommunities = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  
  return store.communities.filter(community => {
    // Filter by type
    if (activeFilter.value === 'joined' && !community.joined) return false
    if (activeFilter.value === 'discover' && community.joined) return false
    
    // Filter by search
    if (q && !community.name.toLowerCase().includes(q)) return false
    
    return true
  })
})

const toggleJoin = (community) => {
  // Check if user is logged in
  if (!localStorage.getItem('user_token')) {
    alert('Please sign in first to join!')
    router.push('/login')
    return
  }
  
  // User is authenticated, proceed with toggle
  store.joinCommunity(community)
}

// Modal Methods
const openModal = () => {
  formData.name = ''
  formData.description = ''
  formData.image = ''
  isModalOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  isModalOpen.value = false
  document.body.style.overflow = ''
}

const submitClub = () => {
  // Use default image if none provided
  const image = formData.image || 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=800&q=80'
  
  store.createClub({
    name: formData.name,
    description: formData.description,
    image: image
  })
  
  closeModal()
}
</script>

<style scoped>
/* Design Tokens (scoped to this component) */
.page-wrap {
  --brand: #1b8f48;
  --brand-600: #167a3d;
  --brand-200: #e6f3e9;
  --page: #fefbea;
  --panel: #e6f6e6;
  --card: #ffffff;
  --card-soft: #e1f0e3;
  --ink: #153226;
  --muted: #6b7c74;
  --outline: #d8eadb;
  --pill: #bfe7c9;
  --accent-orange: #f08c00;
  --r-md: 10px;
  --r-lg: 14px;
  --shadow: 0 3px 10px rgba(0,0,0,.06);
}

.page-wrap {
  max-width: 1180px;
  margin: 18px auto 56px;
  padding: 0 20px 40px;
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color: var(--ink);
}

/* Intro + Search */
.intro-text {
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 10px;
}

.community-search-shell {
  width: 100%;
  height: 46px;
  border-radius: 999px;
  background: #f7fbf8;
  border: 1px solid var(--outline);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  margin-bottom: 10px;
}

.community-search-shell i {
  font-size: 15px;
  color: #6d8677;
}

.community-search-shell input {
  border: none;
  outline: none;
  flex: 1;
  font-size: 14px;
  background: transparent;
  color: #294033;
}

.community-search-shell input::placeholder {
  color: #a5b9ab;
}

/* Filters */
.filters-row {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  margin-bottom: 18px;
}

.filters-pills {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.filter-pill {
  border-radius: 6px;
  border: 1px solid var(--outline);
  background: #f4faf4;
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 500;
  color: #345243;
  cursor: pointer;
}

.filter-pill.is-active {
  border-color: #b4dbc0;
  background: #e1f3e3;
}

.filter-pill.primary {
  border: none;
  background: var(--brand);
  color: #fff;
}

/* Add Club Button */
.add-club-btn {
  margin-left: 10px;
  border: none;
  border-radius: 6px;
  background: var(--brand);
  color: #ffffff;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 14px;
  cursor: pointer;
}

/* Community List */
.community-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.community-card {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr) auto;
  align-items: stretch;
  background: var(--card);
  border-radius: 16px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.community-image {
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.community-main {
  padding: 12px 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.community-name {
  font-size: 15px;
  font-weight: 700;
  color: #1e3527;
  margin: 0;
}

.community-desc {
  font-size: 13px;
  color: var(--muted);
  margin: 0;
}

.community-meta {
  margin-top: 4px;
  font-size: 12px;
  color: #556b5f;
}

.community-meta i {
  margin-right: 6px;
}

/* Status Pill */
.status-pill {
  align-self: center;
  margin-right: 18px;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
  white-space: nowrap;
}

.status-pill.joined {
  background: #e5f7e7;
  color: #1e8b47;
  border-color: #bce5c4;
}

.status-pill.joined i {
  margin-right: 6px;
}

.status-pill.outline {
  background: #fff;
  border-color: var(--brand);
  color: var(--brand);
}

.no-results {
  text-align: center;
  padding: 40px;
  color: var(--muted);
  font-style: italic;
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

.modal-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
}

.modal-form {
  font-size: 12px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 10px;
}

.form-field label {
  font-size: 11px;
  color: #777f7a;
}

.modal-form input,
.modal-form textarea {
  border-radius: 4px;
  border: 1px solid #dadfd4;
  padding: 6px 8px;
  font-size: 12px;
  font-family: inherit;
  outline: none;
  background: #ffffff;
}

.modal-form input:focus,
.modal-form textarea:focus {
  border-color: var(--brand);
}

.modal-actions {
  margin-top: 14px;
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
@media (max-width: 960px) {
  .community-card {
    grid-template-columns: 180px minmax(0, 1fr);
    grid-template-rows: auto auto;
  }
  
  .status-pill {
    grid-column: 1 / -1;
    margin: 0 0 10px 18px;
    align-self: flex-start;
  }
}

@media (max-width: 640px) {
  .page-wrap {
    margin: 18px auto 32px;
    padding: 0 14px 30px;
  }
  
  .community-card {
    grid-template-columns: 1fr;
  }
  
  .community-image {
    height: 140px;
  }
  
  .status-pill {
    margin-left: 18px;
  }
}
</style>
