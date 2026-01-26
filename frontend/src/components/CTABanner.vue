<template>
  <div class="cta-banner">
    <div class="cta-content">
      <h2>Want to be part of the community?</h2>
      <p>Click the button below to apply and start organizing your own events.</p>
      <router-link to="/apply" class="cta-button">
        Apply Now <i class="fas fa-arrow-right"></i>
      </router-link>
    </div>
  </div>
</template>

<script setup>
// No script logic needed for now
</script>

<style scoped>
.cta-banner {
  background: linear-gradient(135deg, #153226 0%, #2E8540 100%);
  border-radius: 16px;
  padding: 60px 40px;
  margin: 40px 0;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(21, 50, 38, 0.15);
}

/* Optional: Subtle pattern overlay or accent element */
.cta-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.05) 0%, transparent 60%);
  pointer-events: none;
}

.cta-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  margin: 0 auto;
}

h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
  font-family: 'Roboto', sans-serif; /* Ensuring font consistency */
}

p {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 32px;
  line-height: 1.6;
  font-weight: 300;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background-color: #FF654A; /* Theme orange/red */
  color: white;
  padding: 14px 32px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 101, 74, 0.3);
}

.cta-button:hover {
  background-color: #ff7e66;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 101, 74, 0.4);
}

.cta-button i {
  transition: transform 0.3s ease;
}

.cta-button:hover i {
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .cta-banner {
    padding: 40px 20px;
    margin: 30px 0;
  }

  h2 {
    font-size: 24px;
  }

  p {
    font-size: 16px;
  }
}
</style>
