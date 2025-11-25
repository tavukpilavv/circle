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
</style>
