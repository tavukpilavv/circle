<template>
  <section class="announcements">
      <el-carousel height="250px">
          <el-carousel-item v-for="item in 10" :key="item" style="text-align:center">
              <el-image :src="getImage('image' + item + '.jpg')" fit="cover" />
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
