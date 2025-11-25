<template>
  <aside class="filters">
      <h3>Filter</h3>
<<<<<<< HEAD
      <div class="filter-item">School</div>
      <div class="filter-item">Community</div>
=======
      <div 
        class="filter-item" 
        :class="{ 'active': activeType === 'events' }"
        @click="updateType('events')"
      >
        Events
      </div>
      <div 
        class="filter-item disabled" 
        :class="{ 'active': activeType === 'communities' }"
      >
        Community
      </div>
>>>>>>> 7becf47 (Final demo preparations complete)
      
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
<<<<<<< HEAD
  }
})

const dateRange = ref([])

=======
  },
  activeType: {
    type: String,
    default: 'events'
  }
})

const emit = defineEmits(['update:activeType'])

const dateRange = ref([])

const updateType = (type) => {
  emit('update:activeType', type)
}

>>>>>>> 7becf47 (Final demo preparations complete)
watch(dateRange, (nv) => {
  if (props.filterChange) {
    props.filterChange(nv)
  }
})
</script>
<<<<<<< HEAD
=======

<style scoped>
.filters {
  background: #fff;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 3px 10px rgba(0,0,0,.06);
  height: fit-content;
  min-width: 250px;
}

.filters h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  color: #153226;
}

.filter-item {
  padding: 10px 14px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  color: #6b7c74;
  transition: all 0.2s;
}

.filter-item:hover {
  background: #f4faf4;
  color: #1b8f48;
}

.filter-item.active {
  background: #e1f3e3;
  color: #1b8f48;
  font-weight: 600;
}

.filter-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.date-filter-container {
  margin-top: 20px;
  cursor: default;
}

.date-filter-container:hover {
  background: transparent;
  color: inherit;
}

.date-filter-container label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
}
</style>
>>>>>>> 7becf47 (Final demo preparations complete)
