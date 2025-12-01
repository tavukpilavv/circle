const App = {
  data() {
    return {
      eventCompleted: false,  // feedback stuff (you can turn on if needed)
      dialogVisible: false,
      rating: 0,
      textarea: ""
    };
  },

  mounted() {
    if (document.body) {
      document.body.style.opacity = "1";
    }

    if (this.eventCompleted) {
      this.showFeedbackDialog();
    }

    // init sliders + see all overlays
    this.initSliders();
    this.initSeeAll();
  },

  methods: {
    // ----- (optional) feedback dialog methods -----
    showFeedbackDialog() {
      this.$nextTick(() => {
        setTimeout(() => {
          this.dialogVisible = true;
        }, 300);
      });
    },

    cancelFeedback() {
      this.dialogVisible = false;
      this.rating = 0;
      this.textarea = "";
    },

    submitFeedback() {
      console.log("User Rating:", this.rating);
      console.log("User Feedback:", this.textarea);
      ElMessage.success("Feedback submitted successfully!");
      this.dialogVisible = false;
      this.rating = 0;
      this.textarea = "";
    },

    // ----- SLIDER LOGIC -----
    initSliders() {
      const sliders = document.querySelectorAll(".slider-shell");
      if (!sliders.length) return;

      sliders.forEach(shell => {
        const track = shell.querySelector(".slider-track");
        const cards = shell.querySelectorAll(".card");
        if (!track || !cards.length) return;

        const prevBtn = shell.querySelector(".slide-btn.left");
        const nextBtn = shell.querySelector(".slide-btn.right");

        function getStep() {
          const firstCard = cards[0];
          const styles = getComputedStyle(track);
          const gap = parseFloat(styles.gap || "0");
          const cardWidth = firstCard.getBoundingClientRect().width;
          return cardWidth + gap;
        }

        function slide(direction) {
          const step = getStep();
          track.scrollBy({
            left: direction * step,
            behavior: "smooth"
          });
        }

        if (prevBtn) prevBtn.addEventListener("click", () => slide(-1));
        if (nextBtn) nextBtn.addEventListener("click", () => slide(1));
      });
    },

    // ----- SEE ALL OVERLAY LOGIC -----
    initSeeAll() {
      const buttons = document.querySelectorAll("[data-seeall-target]");
      const overlays = document.querySelectorAll(".seeall-overlay");

      function closeOverlay(overlay) {
        overlay.classList.remove("is-open");
        overlay.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
      }

      // Close buttons + click outside
      overlays.forEach(overlay => {
        const closeBtn = overlay.querySelector(".seeall-close");
        if (closeBtn) {
          closeBtn.addEventListener("click", () => closeOverlay(overlay));
        }

        overlay.addEventListener("click", e => {
          if (e.target === overlay) {
            closeOverlay(overlay);
          }
        });
      });

      // “See All” clicks
      buttons.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          const target = btn.dataset.seeallTarget;
          const overlay = document.getElementById("seeall-" + target);
          if (!overlay) return;

          overlay.classList.add("is-open");
          overlay.setAttribute("aria-hidden", "false");
          document.body.style.overflow = "hidden"; // lock background scroll
        });
      });
    },
    
    logout() {
      localStorage.removeItem('user_token');
      window.location.href = '/';
    }
  }
};

// Start Vue
const app = Vue.createApp(App);
app.use(ElementPlus);
app.mount("#app");
