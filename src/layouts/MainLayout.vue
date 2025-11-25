<template>
  <div class="layout-wrapper">
    <!-- TOP GREEN STRIP -->
    <div class="top-bar"></div>

    <!-- NAVBAR -->
    <header class="navbar">
      <div class="nav-inner">
        <div class="nav-left">
          <router-link to="/" class="logo">CirCle</router-link>

          <nav class="tabs" aria-label="Primary navigation">
            <router-link to="/communities" class="tab" active-class="is-active">Communities</router-link>
            <router-link to="/events" class="tab" active-class="is-active">Events</router-link>
          </nav>
        </div>

        <div class="nav-center">
          <form class="global-search" role="search" aria-label="Search for an Event">
            <input type="search" placeholder="Search for an Event" aria-label="Search for an Event" />
          </form>
        </div>

        <div class="nav-right">
          <router-link v-if="isLoggedIn" to="/profile" class="icon-btn-link">
            <el-avatar :size="40" :src="userAvatar" />
          </router-link>
          <router-link v-else to="/login" class="sign-in-btn">
            Sign in
          </router-link>
        </div>
      </div>
    </header>

    <div class="nav-bottom-line"></div>

    <!-- MAIN CONTENT -->
    <main class="page-content">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)
const userAvatar = ref('')

const loadAvatar = () => {
  const stored = localStorage.getItem('user_avatar')
  if (stored) {
    userAvatar.value = stored
  } else {
    // Default avatar if none set
    userAvatar.value = "https://api.dicebear.com/7.x/notionists/svg?seed=circle1&flip=false"
  }
}

const checkLogin = () => {
  if (localStorage.getItem('user_token')) {
    isLoggedIn.value = true
  } else {
    isLoggedIn.value = false
  }
}

onMounted(() => {
  checkLogin()
  loadAvatar()
  window.addEventListener('avatar-changed', loadAvatar)
  window.addEventListener('auth-changed', () => {
    checkLogin()
    loadAvatar()
  })
})

onUnmounted(() => {
  window.removeEventListener('avatar-changed', loadAvatar)
  window.removeEventListener('auth-changed', checkLogin)
})

const toggleAuth = () => {
  // Logout logic
  localStorage.removeItem('user_token')
  isLoggedIn.value = false
  router.push('/')
}
</script>

<style>
/* ========= BRAND TOKENS ========= */
:root {
  --brand: #1b8f48;
  --brand-600: #167a3d;
  --brand-200: #e6f3e9;

  --page: #fefbea;
  --card: #ffffff;

  --ink: #153226;
  --muted: #6b7c74;
  --outline: #d8eadb;

  --shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
}

/* ========= RESET ========= */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  background: var(--page);
  color: var(--ink);
}

.layout-wrapper {
  min-height: 100vh;
  background: var(--page);
}

.page-content {
  background: var(--page);
}

/* ========= TOP STRIP + NAVBAR ========= */

.top-bar {
  width: 100%;
  height: 14px;
  background: var(--brand);
}

.navbar {
  background: var(--page);
}

.nav-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 14px 20px 12px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
}

.nav-bottom-line {
  height: 2px;
  background: var(--brand);
  opacity: 0.6;
}

/* left: logo + tabs */

.nav-left {
  display: flex;
  align-items: center;
}

.logo {
  margin-right: 48px;
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 40px;
  letter-spacing: -1px;
  color: var(--brand);
  text-decoration: none;
}

.tabs {
  display: flex;
  gap: 28px;
}

.tab {
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  color: #333;
  padding-bottom: 6px;
}

.tab.is-active {
  border-bottom: 2px solid var(--brand);
}

/* center: search bar */

.nav-center {
  display: flex;
  justify-content: center;
}

.global-search {
  width: 40vw;
  max-width: 500px;
  min-width: 320px;
  height: 44px;
  padding: 0 18px;
  border-radius: 26px;
  background: var(--brand-200);
  display: flex;
  align-items: center;
}

.global-search input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: #2b4c3d;
}

.global-search input::placeholder {
  color: #8ca59a;
}

/* right: avatar / sign in */

.nav-right {
  display: flex;
  justify-content: flex-end;
}

.icon-btn-link {
  text-decoration: none;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: none;
  background: var(--brand-200);
  display: grid;
  place-items: center;
  cursor: pointer;
}

.icon-btn i {
  color: #1f5c3f;
}

.sign-in-btn {
  display: inline-flex;
  align-items: center;
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 600;
  color: #FF654A;
  cursor: pointer;
  padding: 8px 20px;
  white-space: nowrap;
  transition: opacity 0.2s;
  text-decoration: none;
}

.sign-in-btn:hover {
  opacity: 0.8;
}

/* ========= RESPONSIVE ========= */

@media (max-width: 768px) {
  /* 1. Aggressively Hide Search */
  .nav-center,
  .global-search,
  .search-bar,
  header form,
  header input {
    display: none !important;
  }

  /* 2. Unhide & Style Tabs */
  .nav-left .tabs {
    display: flex !important;
    gap: 12px; /* Consistent gap between links */
    margin-left: 12px; /* Consistent gap between Logo and Tabs */
    overflow: visible;
  }

  .nav-left .tab {
    display: block !important;
    font-size: 13px; /* Readable size */
    padding-bottom: 4px;
    white-space: nowrap;
    margin-right: 0 !important;
  }

  /* 3. Force Horizontal Layout */
  .nav-inner {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important; /* Logo+Tabs Left, Icon Right */
    align-items: center !important;
    padding: 12px 16px;
    gap: 0;
  }

  .nav-left {
    display: flex !important;
    align-items: center !important;
    width: auto !important;
    flex: 1; /* Allow growing to push icon if needed, but space-between handles it */
  }

  .nav-right {
    display: flex !important;
    justify-content: flex-end !important;
    width: auto !important;
    margin-left: 12px; /* Gap between Events and Icon */
  }

  .logo {
    margin-right: 0 !important;
    font-size: 18px; /* Balanced logo size */
  }

  /* 4. Shrink Icon (User Avatar) */
  .icon-btn {
    width: 32px;
    height: 32px;
  }
  
  .icon-btn :deep(.el-avatar) {
    --el-avatar-size: 32px !important;
  }

  /* 5. Sign In Button (Text Mode) */
  .sign-in-btn {
    font-size: 12px !important;
    width: auto !important;
    height: auto !important;
    padding: 6px 10px !important;
    border-radius: 4px !important;
    background-color: transparent !important;
    color: #FF654A !important;
    display: inline-flex !important;
    text-decoration: none !important;
  }

  .sign-in-btn::after {
    display: none !important;
  }
}
</style>
