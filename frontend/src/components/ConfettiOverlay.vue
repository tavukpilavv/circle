<template>
  <div class="confetti-overlay" aria-hidden="true">
    <div 
      v-for="n in 50" 
      :key="n" 
      class="confetti"
      :style="getConfettiStyle(n)"
    ></div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['close'])

const COLORS = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#FFA500', '#1b8f48'];

const getConfettiStyle = (n) => {
  const left = Math.random() * 100 + '%';
  const animDelay = Math.random() * 2 + 's';
  const animDuration = (Math.random() * 2 + 2) + 's';
  const color = COLORS[Math.floor(Math.random() * COLORS.length)];
  
  return {
    left: left,
    animationDelay: animDelay,
    animationDuration: animDuration,
    backgroundColor: color
  };
}

let timer;

onMounted(() => {
  timer = setTimeout(() => {
    emit('close');
  }, 3500);
})

onUnmounted(() => {
  clearTimeout(timer);
})
</script>

<style scoped>
.confetti-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none; /* Let clicks pass through if needed, but usually we want to block */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.confetti {
  position: absolute;
  top: -20px;
  width: 10px;
  height: 10px;
  opacity: 0.8;
  animation: fall linear forwards;
}

@keyframes fall {
  0% {
    transform: translateY(-20px) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(720deg);
    opacity: 0;
  }
}
</style>
