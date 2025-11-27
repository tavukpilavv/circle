// aboutus.js
document.addEventListener("DOMContentLoaded", () => {
  const statEls = document.querySelectorAll(".about-stat-number");

  // OPTIONAL:
  // If other pages set window.circleStats, we use those live values:
  // window.circleStats = { universities: 3, clubs: 20, users: 230, events: 75 }
  if (window.circleStats && typeof window.circleStats === "object") {
    statEls.forEach((el) => {
      const key = el.dataset.statKey;
      if (key && window.circleStats[key] != null) {
        el.dataset.target = String(window.circleStats[key]);
      }
    });
  }

  function animateStat(el, target) {
    const duration = 1100; // ms
    const startTime = performance.now();
    const start = 0;

    function frame(now) {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
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
    statEls.forEach((el) => {
      const target = parseInt(el.dataset.target || "0", 10);
      animateStat(el, target);
    });
  }

  // Animate when stats grid enters viewport
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
    // Fallback: animate immediately
    startStatsAnimation();
  }
});
