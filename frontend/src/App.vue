<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script setup>
import MainLayout from './layouts/MainLayout.vue'
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
  background-color: #fefbea !important;
  border: 3px dashed #1b8f48 !important;
  box-shadow: none !important;
}

.el-dialog__header {
  background-color: #fefbea !important;
}

.el-dialog__body {
  background-color: #fefbea !important;
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
