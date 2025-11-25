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
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { store } from '../store.js'

const router = useRouter()
const route = useRoute()
const searchQuery = ref('')
const activeFilter = ref('all')

const applyFilters = () => {
  if (route.query.filter === 'joined') {
    activeFilter.value = 'joined'
  } else {
    activeFilter.value = 'all'
  }
}

onMounted(() => {
  applyFilters()
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
<<<<<<< HEAD
    alert('Lütfen katılmak için önce giriş yapın!')
=======
    alert('Please sign in first to join!')
>>>>>>> 7becf47 (Final demo preparations complete)
    router.push('/login')
    return
  }
  
  // User is authenticated, proceed with toggle
  store.joinCommunity(community)
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
