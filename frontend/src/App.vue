<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script setup>
import { onMounted, watch } from "vue"
import { useRoute } from "vue-router"
import MainLayout from "./layouts/MainLayout.vue"
import { store } from "./store.js"

const route = useRoute()

const syncAuth = async () => {
  store.refreshAuth()


  if (
    store.userRole === "admin" ||
    store.userRole === "super_admin" ||
    store.userRole === "superadmin"
  ) {
    await store.loadCommunitiesFromBackend()
  }
}

// İlk yüklemede
onMounted(syncAuth)

// Login/logout sonrası yönlendirmelerde / sayfa geçişlerinde
watch(
  () => route.fullPath,
  () => {
    syncAuth()
  }
)
</script>

<style>
/* Hide scrollbar globally while maintaining scroll functionality */

/* Webkit browsers (Chrome, Safari, Edge) */
::-webkit-scrollbar {
  display: none;
}

/* Firefox */
html, body {
  scrollbar-width: none;
}

/* IE and legacy Edge */
html, body {
  -ms-overflow-style: none;
}

/* Element Plus Dialog Styling */
.el-dialog {
  background-color: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
  border-radius: 16px !important;
}

.el-dialog__header {
  background-color: #ffffff !important;
}

.el-dialog__body {
  background-color: #ffffff !important;
}

/* Global Layout Container - Single Source of Truth */
.standard-layout-container {
  max-width: 1280px !important;
  width: 100% !important;
  margin: 0 auto !important;
  padding-left: 24px !important;
  padding-right: 24px !important;
  box-sizing: border-box !important;
}
</style>
