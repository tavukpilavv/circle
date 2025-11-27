<template>
  <footer class="app-footer">
    <div class="footer-content">
      <!-- Brand Column -->
      <div class="footer-col brand-col">
        <router-link to="/" class="footer-logo">CirCle</router-link>
        <p class="footer-tagline">
          Connecting students, building communities, and creating memories.
        </p>
        <div class="social-links">
          <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
          <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
        </div>
      </div>

      <!-- Quick Links Removed -->

      <!-- Support / Company -->
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><router-link to="/about">About Us</router-link></li>
          <li><router-link to="/apply">Apply</router-link></li>
          <li><router-link to="/contact">Help & Support</router-link></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; {{ new Date().getFullYear() }} CirCle. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background-color: #fefbea;
  border-top: 1px solid #e6f3e9;
  padding: 20px 20px 12px; /* Ultra compact padding */
  margin-top: auto;
  text-align: center;
}

.footer-content {
  max-width: 600px;
  margin: 0 auto 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px; /* Tighter gap */
}

.footer-logo {
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 18px; /* Smaller logo */
  color: #1b8f48;
  text-decoration: none;
  margin: 0;
}

.footer-tagline {
  display: none;
}

/* Links Row */
.footer-col {
  display: flex;
  justify-content: center;
}

.footer-col h4 {
  display: none;
}

.footer-col ul {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px; /* Tighter link spacing */
  padding: 0;
  margin: 0;
  list-style: none;
}

.footer-col li {
  margin: 0;
}

.footer-col a {
  text-decoration: none;
  color: #556b5f;
  font-size: 12px; /* Smaller font */
  font-weight: 600;
  transition: color 0.2s;
}

.footer-col a:hover {
  color: #1b8f48;
}

/* Social Icons */
.social-links {
  display: flex;
  gap: 12px;
  margin-top: 0;
}

.social-links a {
  color: #1b8f48;
  font-size: 14px; /* Smaller icons */
  opacity: 0.8;
  transition: all 0.2s;
}

.social-links a:hover {
  opacity: 1;
  transform: translateY(-1px);
}

.footer-bottom {
  font-size: 10px; /* Tiny copyright */
  color: #8ca59a;
  margin: 0 auto;
  padding-top: 8px;
  border-top: none; /* Remove separator for compactness */
}

@media (max-width: 600px) {
  .footer-col ul {
    gap: 12px;
  }
}
</style>
