<script setup>
import { ref, onMounted, nextTick } from 'vue';


// 1. REAKTİF VERİLER
const stats = ref({
  universities: 0,
  clubs: 0,
  users: 0,
  events: 0
});

// 2. ANİMASYON FONKSİYONLARI
function animateStat(el, target) {
  const duration = 1500;
  const startTime = performance.now();
  const start = 0;

  function frame(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.floor(start + (target - start) * eased);
    el.textContent = value.toString();
    if (progress < 1) {
      requestAnimationFrame(frame);
    } else {
      el.textContent = target.toString();
    }
  }
  requestAnimationFrame(frame);
}

function startStatsAnimation() {
  const statEls = document.querySelectorAll(".about-stat-number");
  statEls.forEach((el) => {
    const target = parseInt(el.dataset.target || "0", 10);
    animateStat(el, target);
  });
}

// 3. VERİ ÇEKME
onMounted(async () => {
  try {
    const response = await fetch('/api/general/stats');
    const data = await response.json();

    if (data) {
      stats.value = {
        universities: data.universities,
        clubs: data.clubs,
        users: data.students,
        events: data.events
      };
    }
  } catch (error) {
    console.error("Veri çekilemedi:", error);
    stats.value = { universities: 0, clubs: 0, users: 0, events: 0 };
  }

  await nextTick();

  const statsGrid = document.querySelector(".about-stats-grid");
  if ("IntersectionObserver" in window && statsGrid) {
    let done = false;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !done) {
            done = true;
            startStatsAnimation();
            observer.disconnect();
          }
        });
      },
      { threshold: 0.4 }
    );
    observer.observe(statsGrid);
  } else {
    startStatsAnimation();
  }
});
</script>

<template>
  <div class="about-us-container">
    <main class="page-wrap">
      <section class="about-hero">
        <div class="about-hero-card">
          <div class="about-hero-pill"><span class="pill-dot"></span> Campus event hub</div>
          <h1 class="about-hero-title">All your campus life in one circle.</h1>
          <p class="about-hero-text">CirCle connects students, clubs, and events in a simple, colorful space.</p>
          
          <div class="about-hero-tags">
             <button class="about-tag">Real events</button>
             <button class="about-tag">Real communities</button>
             <button class="about-tag">Zero FOMO</button>
          </div>
        </div>
      </section>

      <section class="about-stats-section">
        <div class="about-stats-header">
          <h2>CirCle at a glance</h2>
          <p>A quick snapshot of the platform.</p>
        </div>

        <div class="about-stats-grid">
          <article class="about-stat-card">
            <div class="about-stat-icon about-stat-icon-uni">
               <i class="fa-solid fa-building-columns"></i>
            </div>
            <div class="about-stat-number" :data-target="stats.universities">0</div>
            <div class="about-stat-label">Universities</div>
            <div class="about-stat-sub">Pilot campus + upcoming partners.</div>
          </article>

          <article class="about-stat-card">
            <div class="about-stat-icon about-stat-icon-clubs">
               <i class="fa-solid fa-users-line"></i>
            </div>
            <div class="about-stat-number" :data-target="stats.clubs">0</div>
            <div class="about-stat-label">Student clubs</div>
            <div class="about-stat-sub">Publishing and managing events.</div>
          </article>

          <article class="about-stat-card">
            <div class="about-stat-icon about-stat-icon-users">
               <i class="fa-solid fa-user-graduate"></i>
            </div>
            <div class="about-stat-number" :data-target="stats.users">0</div>
            <div class="about-stat-label">Active students</div>
            <div class="about-stat-sub">Exploring events and saving favorites.</div>
          </article>

          <article class="about-stat-card">
            <div class="about-stat-icon about-stat-icon-events">
               <i class="fa-solid fa-calendar-star"></i>
            </div>
            <div class="about-stat-number" :data-target="stats.events">0</div>
            <div class="about-stat-label">Published events</div>
            <div class="about-stat-sub">Workshops, meetups, and activities.</div>
          </article>
        </div>
      </section>

      <section class="about-features-section">
         <div class="about-stats-header"><h2>Why CirCle?</h2></div>
         <div class="about-features-grid">
           <article class="about-feature-card">
             <div class="feature-icon green"><i class="fa-solid fa-compass"></i></div>
             <div class="feature-title">One place to discover</div>
             <p class="feature-text">All official campus events collected into one clear timeline.</p>
           </article>
           <article class="about-feature-card">
             <div class="feature-icon purple"><i class="fa-solid fa-bullhorn"></i></div>
             <div class="feature-title">Clubs reach the right people</div>
             <p class="feature-text">Clubs share once, students see instantly.</p>
           </article>
           <article class="about-feature-card">
             <div class="feature-icon blue"><i class="fa-solid fa-laptop-code"></i></div>
             <div class="feature-title">Made for the browser</div>
             <p class="feature-text">Works on any device. No installs, just open and join.</p>
           </article>
         </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
:root { --brand: #372D2D; --brand-600: #241D1D; --brand-200: #EBE8E8; --page: #ffffff; --ink: #153226; }
.about-us-container { font-family: "Inter", sans-serif; background: #ffffff; color: #153226; min-height: 100vh; }

.page-wrap { max-width: 1180px; margin: 0 auto 56px; padding: 0 20px 40px; }
.about-hero { margin-top: 24px; margin-bottom: 26px; }
.about-hero-card { padding: 32px 0 24px; background: #ffffff; }
.about-hero-pill { display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 999px; background: #ffffff; border: 1px solid #e5e7eb; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #111111; margin-bottom: 16px; }
.pill-dot { width: 8px; height: 8px; border-radius: 999px; border: 2px solid #111111; background-color: #ffffff; }
.about-hero-title { font-size: 36px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 12px; color: #111111; }
.about-hero-text { font-size: 16px; line-height: 1.6; color: #374151; max-width: 560px; }
.about-hero-tags { margin-top: 24px; display: flex; flex-wrap: wrap; gap: 10px; }
.about-tag { border: 1px solid #e5e7eb; border-radius: 999px; padding: 8px 16px; font-size: 13px; font-weight: 600; background-color: #ffffff; color: #111111; cursor: pointer; }
.about-stats-section { margin-bottom: 30px; }
.about-stats-header { display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px; }
.about-stats-header h2 { font-size: 18px; font-weight: 750; }
.about-stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
.about-stat-card { border-radius: 18px; background-color: #ffffff; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06); padding: 14px 14px 12px; position: relative; overflow: hidden; }
.about-stat-icon { width: 34px; height: 34px; border-radius: 12px; display: grid; place-items: center; color: #ffffff; margin-bottom: 8px; font-size: 16px; }
.about-stat-icon-uni { background: linear-gradient(135deg, #1b8f48, #7fd292); }
.about-stat-icon-clubs { background: linear-gradient(135deg, #7d3ff2, #f391da); }
.about-stat-icon-users { background: linear-gradient(135deg, #f08c00, #ffd26d); }
.about-stat-icon-events { background: linear-gradient(135deg, #1a6fd6, #76c2ff); }
.about-stat-number { font-size: 22px; font-weight: 800; color: #167a3d; margin-bottom: 2px; }
.about-stat-label { font-size: 12px; font-weight: 600; margin-bottom: 3px; }
.about-stat-sub { font-size: 11px; color: #6b7c74; line-height: 1.4; }
.about-features-section { margin-top: 24px; }
.about-features-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 6px; }
.about-feature-card { border-radius: 18px; background-color: #ffffff; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06); padding: 14px 14px 12px; }
.feature-icon { width: 34px; height: 34px; border-radius: 12px; display: grid; place-items: center; font-size: 16px; margin-bottom: 8px; }
.feature-icon.green { background: #e6f6e6; color: #167a3d; }
.feature-icon.purple { background: #f2e6ff; color: #7d3ff2; }
.feature-icon.blue { background: #e2f0ff; color: #1a6fd6; }
.feature-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.feature-text { font-size: 12px; color: #6b7c74; line-height: 1.5; }
</style>
