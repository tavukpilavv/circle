<template>
  <section class="announcements">
      <el-carousel height="400px">
          <el-carousel-item v-for="item in 10" :key="item" style="text-align:center">
              <el-image :src="getImage('image' + item + '.jpg')" fit="cover" style="width: 100%; height: 100%; display: block;" />
          </el-carousel-item>
      </el-carousel>                
  </section>
</template>

<script setup>
import { ref } from 'vue'

// Helper to resolve image URLs from the project root "images" folder
const getImage = (fileName) => new URL(`../../images/${fileName}`, import.meta.url).href

const items = ref([])
</script>

<style scoped>
/* Mobile: Add side padding to the banner */
@media (max-width: 768px) {
  .announcements {
    padding-left: 16px;
    padding-right: 16px;
  }
}

/* Fix carousel indicators position */
:deep(.el-carousel__indicators--horizontal) {
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 5px;
}

:deep(.el-carousel__indicator--horizontal .el-carousel__button) {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.7);
  opacity: 1;
}

:deep(.el-carousel__indicator.is-active .el-carousel__button) {
  background-color: #ffffff;
}
</style>
