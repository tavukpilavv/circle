<template>
  <div class="page-wrap">
    <!-- PROFILE BANNER -->
    <section class="profile-banner">
      <div class="profile-left">
        <!-- Dynamic Avatar using Element Plus -->
        <el-avatar 
          :size="100" 
          :src="userAvatar" 
          class="avatar-shadow"
          role="presentation" 
        />

        <div class="identity">
          <div class="name-row">
            <div class="name" :class="{ 'is-admin': user.role === 'admin' || user.role === 'super_admin' }">
              {{ user.name }}
            </div>
            
            <!-- Verified Icon for Admin -->
            <el-icon v-if="user.role === 'admin' || user.role === 'super_admin'" class="verified-icon" :size="20" color="#409EFF">
              <CircleCheckFilled />
            </el-icon>

            <!-- Admin Badge -->
            <el-tag 
              v-if="user.role === 'admin' || user.role === 'super_admin'" 
              :type="user.role === 'super_admin' ? 'warning' : 'success'" 
              size="small" 
              effect="dark" 
              round
            >
              {{ user.role === 'super_admin' ? 'Super Admin' : 'Admin' }}
            </el-tag>
          </div>
          <div class="sub">{{ user.sub }}</div>
        </div>
      </div>

      <div class="profile-right">
        <router-link to="/settings" style="text-decoration: none;">
          <button class="ghost-gear" aria-label="Settings">
            <i class="fas fa-gear"></i>
          </button>
        </router-link>
        <button class="logout" aria-label="Log Out" @click="logout">
          Log Out
          <i class="fas fa-arrow-right-from-bracket"></i>
        </button>
      </div>
    </section>

    <!-- TABS UNDER PROFILE -->
    <section class="dual-tabs">
      <button 
        class="tabbtn" 
        :class="activePanel === 'events' ? 'solid' : 'outline'" 
        @click="activePanel = 'events'"
        :aria-pressed="activePanel === 'events'"
      >My Events</button>
      <button 
        class="tabbtn" 
        :class="activePanel === 'communities' ? 'solid' : 'outline'" 
        @click="activePanel = 'communities'"
        :aria-pressed="activePanel === 'communities'"
      >My Communities</button>
    </section>

    <div v-show="activePanel === 'events'" class="panel is-active">
      <!-- UPCOMING EVENTS -->
      <section class="section-head">
        <h3>Upcoming Events</h3>
        <router-link to="/events?filter=upcoming" class="see-all">
          See All <i class="fas fa-caret-right"></i>
        </router-link>
      </section>

      <section class="slider-shell" aria-label="Upcoming Events">
        <button class="slide-btn left" type="button" @click="slide('upcoming', -1)">
          <i class="fas fa-chevron-left"></i>
        </button>

        <div class="slider-track" ref="upcomingTrack">
          <article class="card event-card" v-for="event in upcomingEvents" :key="event.id">
            <img :src="event.image" class="event-cover" alt="" />
            <div class="event-body">
              <h4>{{ event.name }}</h4>
              <p>{{ event.date }}</p>
            </div>
            <router-link :to="'/events/' + event.id" class="view-pill">View</router-link>
          </article>
          <div v-if="upcomingEvents.length === 0" class="no-data-msg">
            No upcoming events found.
          </div>
        </div>

        <button class="slide-btn right" type="button" @click="slide('upcoming', 1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </section>

      <!-- NEAREST ACTIVITIES -->
      <section class="section-head">
        <h3>Nearest Activities</h3>
        <router-link to="/events?filter=registered" class="see-all">
          See All <i class="fas fa-caret-right"></i>
        </router-link>
      </section>

      <section class="slider-shell" aria-label="Nearest Activities">
        <button class="slide-btn left" type="button" @click="slide('activities', -1)">
          <i class="fas fa-chevron-left"></i>
        </button>

        <div class="slider-track" ref="activitiesTrack">
          <!-- Dynamic activities from store -->
          <article 
            class="card activity-card" 
            v-for="event in registeredEvents" 
            :key="event.id"
          >
            <img :src="event.image" class="event-cover" alt="" />
            <div class="activity-content">
              <h4>{{ event.name }}</h4>
              <p>{{ event.date }} • {{ event.location }}</p>
            </div>
          </article>
          <div v-if="registeredEvents.length === 0" class="no-data-msg">
            No upcoming activities.
          </div>
        </div>

        <button class="slide-btn right" type="button" @click="slide('activities', 1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </section>
    </div>

    <div v-show="activePanel === 'communities'" class="panel is-active">
      <section class="section-head">
        <h3>Joined Communities</h3>
        <span class="community-count">{{ joinedCommunities.length }} communities</span>
      </section>

      <section class="community-grid" aria-label="Joined communities">
        <article 
          class="community-card" 
          v-for="community in joinedCommunities" 
          :key="community.id"
        >
          <img class="community-cover"
            :src="community.image"
            alt="Community cover image">
          <div class="community-body">
            <h4>{{ community.name }}</h4>
            <p>{{ community.description }}</p>
            <div class="community-meta">
              <span class="community-chip">{{ community.role || 'Member' }}</span>
              <span>Joined {{ community.joinedDate || 'recently' }}</span>
            </div>
          </div>
        </article>
        
        <div v-if="joinedCommunities.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-users"></i>
          </div>
          <h3>No communities yet</h3>
          <p>Join a community to connect with others and see their events here.</p>
          <router-link to="/communities" class="empty-btn">
            Browse Communities
          </router-link>
        </div>
      </section>
    </div>

    <!-- SEE ALL OVERLAYS -->
    <div class="seeall-overlay" :class="{ 'is-open': seeAllTarget === 'events' }" @click.self="closeSeeAll">
      <div class="seeall-inner">
        <div class="seeall-header">
          <h2>All Upcoming Events</h2>
          <button class="seeall-close" type="button" aria-label="Close" @click="closeSeeAll">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="seeall-grid">
           <article class="card event-card" v-for="n in 8" :key="n"><button class="view-pill">View</button></article>
        </div>
      </div>
    </div>

    <div class="seeall-overlay" :class="{ 'is-open': seeAllTarget === 'activities' }" @click.self="closeSeeAll">
      <div class="seeall-inner">
        <div class="seeall-header">
          <h2>All Nearest Activities</h2>
          <button class="seeall-close" type="button" aria-label="Close" @click="closeSeeAll">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="seeall-grid">
          <article class="card activity-card" v-for="n in 8" :key="n"></article>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import { CircleCheckFilled } from '@element-plus/icons-vue'

const router = useRouter()
const activePanel = ref('events')
const seeAllTarget = ref(null)
const upcomingTrack = ref(null)
const activitiesTrack = ref(null)

// Reactive source for avatar
const storedAvatar = ref('')

// User data from localStorage
const user = reactive({
  name: 'Guest',
  role: 'user',
  sub: 'Student'
})

const loadUserData = () => {
  const token = localStorage.getItem('user_token')
  if (token) {
    user.name = localStorage.getItem('user_name') || 'User'
    user.role = localStorage.getItem('user_role') || 'user'
    
    const major = localStorage.getItem('user_major') || 'Student'
    const gradYear = localStorage.getItem('user_grad_year')
    
    if (gradYear) {
      user.sub = `${major} • Class of ${gradYear}`
    } else {
      user.sub = major
    }
  }
}

const joinedCommunities = computed(() => {
  return store.communities.filter(c => c.joined)
})

const registeredEvents = computed(() => {
  return store.events.filter(e => e.registered)
})

const upcomingEvents = computed(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return store.events.filter(e => {
    const eventDate = new Date(e.date);
    return eventDate >= today;
  }).sort((a, b) => new Date(a.date) - new Date(b.date));
})

// Computed property for User Avatar
const userAvatar = computed(() => {
  if (storedAvatar.value) {
    return storedAvatar.value
  }
  // Default Letter Avatar using DiceBear Initials
  return `https://api.dicebear.com/7.x/initials/svg?seed=${user.name}&backgroundColor=1b8f48&textColor=ffffff`
})

const loadAvatar = () => {
  storedAvatar.value = localStorage.getItem('user_avatar') || ''
}

onMounted(() => {
  loadUserData()
  loadAvatar()
  window.addEventListener('avatar-changed', loadAvatar)
})

onUnmounted(() => {
  window.removeEventListener('avatar-changed', loadAvatar)
})

const logout = () => {
  localStorage.removeItem('user_token')
  localStorage.removeItem('user_role')
  localStorage.removeItem('user_avatar')
  window.location.href = '/'
}

const openSeeAll = (target) => {
  seeAllTarget.value = target
  document.body.style.overflow = 'hidden'
}

const closeSeeAll = () => {
  seeAllTarget.value = null
  document.body.style.overflow = ''
}

const slide = (trackName, direction) => {
  const track = trackName === 'upcoming' ? upcomingTrack.value : activitiesTrack.value
  if (!track) return

  const cards = track.querySelectorAll('.card')
  if (!cards.length) return

  const firstCard = cards[0]
  const styles = getComputedStyle(track)
  const gap = parseFloat(styles.gap || "0")
  const cardWidth = firstCard.getBoundingClientRect().width
  const step = cardWidth + gap

  track.scrollBy({
    left: direction * step,
    behavior: "smooth"
  })
}
</script>

<style scoped>
/* =========================
   DESIGN TOKENS
   ========================= */
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
  --shadow: 0 3px 10px rgba(0, 0, 0, .06);
}

/* =========================
   PAGE LAYOUT
   ========================= */
.page-wrap {
  max-width: 1180px;
  margin: 18px auto 56px;
  padding: 0 20px;
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color: var(--ink);
}

/* profile banner */
.profile-banner {
  background: var(--panel);
  border-radius: var(--r-lg);
  padding: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.profile-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-shadow {
  box-shadow: var(--shadow);
  border: 4px solid #ffffff;
  background: #fff;
}

.identity .name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.identity .name {
  font-size: 20px;
  font-weight: 700;
}

.identity .name.is-admin {
  color: var(--brand);
  font-weight: 800;
}

.verified-icon {
  display: flex;
  align-items: center;
}

.identity .sub {
  margin-top: 4px;
  font-size: 12px;
  font-weight: 500;
  color: #4e6d5c;
}

.profile-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.ghost-gear {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: var(--brand-200);
  display: grid;
  place-items: center;
  color: var(--brand-600);
  cursor: pointer;
  transition: all 0.2s;
}

.ghost-gear:hover {
  background: var(--brand);
  color: #ffffff;
}

.logout {
  border: none;
  background: transparent;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #284738;
  cursor: pointer;
}

/* tabs row */
.dual-tabs {
  margin: 18px 0 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.tabbtn {
  height: 40px;
  border-radius: var(--r-md);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.tabbtn.solid {
  background: var(--brand);
  color: #fff;
  border: none;
}

.tabbtn.outline {
  background: transparent;
  border: 2px solid var(--brand);
  color: var(--brand);
}



.community-count {
  font-size: 14px;
  font-weight: 600;
  color: var(--muted);
}

.community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.community-card {
  background: var(--card);
  border-radius: var(--r-lg);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 16px;
}

.community-cover {
  width: 100%;
  height: 140px;
  border-radius: var(--r-md);
  object-fit: cover;
  object-position: center;
}

.community-body h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--ink);
}

.community-body p {
  margin: 8px 0 0;
  font-size: 14px;
  color: var(--muted);
  line-height: 1.5;
}

.community-meta {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--muted);
  gap: 12px;
}

.community-chip {
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--brand-200);
  color: var(--brand);
  font-weight: 600;
  font-size: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* section headers */
.section-head {
  margin-top: 4px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-head h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}

.see-all {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-orange);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

/* =========================
   SLIDER (4 visible cards)
   ========================= */
.slider-shell {
  position: relative;
  margin-bottom: 30px;
}

.slider-track {
  display: flex;
  gap: 20px;
  overflow: hidden;
  scroll-behavior: smooth;
  padding: 4px 0 6px;
}

/* 4 visible on wide screens */
.card {
  flex: 0 0 calc((100% - 3 * 20px) / 4);
  border-radius: var(--r-lg);
  background: var(--card);
  box-shadow: var(--shadow);
  height: 170px;
  position: relative;
}

/* Upcoming events look */
.event-card {
  background: var(--card);
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.event-cover {
  width: 100%;
  height: 90px;
  border-radius: var(--r-md);
  object-fit: cover;
  margin-bottom: 8px;
}

.event-body h4 {
  font-size: 13px;
  margin: 0;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--ink);
}

.event-body p {
  font-size: 12px;
  color: var(--muted);
  margin: 2px 0 0;
}

.view-pill {
  position: absolute;
  right: 16px;
  bottom: 16px;
  border: none;
  border-radius: 999px;
  background: var(--pill);
  color: #285847;
  padding: 0 18px;
  height: 30px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Nearest activities look */
.activity-card {
  background: var(--card-soft);
  height: 220px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.activity-content h4 {
  margin: 0 0 4px;
  font-size: 15px;
  font-weight: 700;
  color: #1e3527;
}

.activity-content p {
  margin: 0;
  font-size: 12px;
  color: #556b5f;
}

.no-data-msg {
  padding: 20px;
  color: var(--muted);
  font-style: italic;
  width: 100%;
  text-align: center;
}

/* Empty State Enhanced */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  background: var(--card-soft);
  border-radius: var(--r-lg);
  border: 1px dashed var(--outline);
}

.empty-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #fff;
  display: grid;
  place-items: center;
  font-size: 24px;
  color: var(--brand);
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 8px;
}

.empty-state p {
  font-size: 14px;
  color: var(--muted);
  margin: 0 0 20px;
  max-width: 300px;
  line-height: 1.5;
}

.empty-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  background: var(--brand);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border-radius: 999px;
  text-decoration: none;
  transition: all 0.2s;
}

.empty-btn:hover {
  background: var(--brand-600);
  transform: translateY(-1px);
}

/* Arrows */
.slide-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: none;
  background: var(--brand);
  color: #fff;
  cursor: pointer;
  display: grid;
  place-items: center;
  font-size: 16px;
  z-index: 5;
}

.slide-btn.left {
  left: -10px;
}

.slide-btn.right {
  right: -10px;
}

/* =========================
   SEE ALL OVERLAY
   ========================= */
.seeall-overlay {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, .35);
  z-index: 1000;
}

.seeall-overlay.is-open {
  display: flex;
}

.seeall-inner {
  background: var(--page);
  /* same as page background */
  max-width: 1000px;
  width: 90%;
  max-height: 80vh;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, .2);
  padding: 20px 22px 24px;
  overflow: auto;
}

.seeall-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.seeall-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
}

.seeall-close {
  border: none;
  background: #f5e8e8;
  border-radius: 999px;
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.seeall-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 18px;
}

/* Make cards in overlay a bit taller */
.seeall-grid .card {
  flex: 0 0 auto;
  height: 190px;
}

/* =========================
   RESPONSIVE
   ========================= */
@media (max-width: 960px) {
  .card {
    flex: 0 0 calc((100% - 20px) / 2);
  }
}

@media (max-width: 768px) {
  .profile-banner {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 20px;
  }

  .profile-left {
    flex-direction: column;
    text-align: center;
  }

  .identity .name-row {
    justify-content: center;
  }
  
  .profile-right {
    width: 100%;
    justify-content: center;
  }

  .dual-tabs {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .community-grid {
    grid-template-columns: repeat(auto-fill, minmax(100%, 1fr));
  }
}

@media (max-width: 600px) {
  .page-wrap {
    padding: 0 16px;
    margin-top: 10px;
  }

  .card {
    flex: 0 0 100%;
  }

  .slide-btn {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }

  .slide-btn.left {
    left: -6px;
  }

  .slide-btn.right {
    right: -6px;
  }

  .seeall-inner {
    width: 94%;
    max-height: 85vh;
    padding: 16px;
  }
  
  .seeall-grid {
    grid-template-columns: 1fr;
  }
}
</style>
