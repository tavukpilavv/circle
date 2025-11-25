<template>
  <aside class="filters">
      <h3>Filter</h3>
      <div class="filter-item">School</div>
      <div class="filter-item">Community</div>
      
      <div class="filter-item date-filter-container">
          <label for="event-date">Date</label>
          <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="-"
              start-placeholder="Start"
              end-placeholder="End"
              size="default"
              style="max-width:200px"
          />                        
      </div>
  </aside> 
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  filterChange: {
    type: Function
  }
})

const dateRange = ref([])

watch(dateRange, (nv) => {
  if (props.filterChange) {
    props.filterChange(nv)
  }
})
</script>
