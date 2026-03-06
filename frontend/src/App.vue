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

/* Element Plus Dialog - Yellow background with green dashed border */
.el-dialog {
  background-color: #ffffff !important;
  border: 3px dashed #1b8f48 !important;
  box-shadow: none !important;
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
