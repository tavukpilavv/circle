// communities.js

document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".community-card");
  const searchInput = document.getElementById("communitySearchInput");
  const filterButtons = document.querySelectorAll(".filter-pill");

  /* =========================
     JOIN / LEAVE TOGGLE
     ========================= */
  function initJoinButtons() {
    cards.forEach((card) => {
      const button = card.querySelector(".status-pill");
      if (!button) return;

      // Determine initial state
      let joined;
      if (card.dataset.joined === "true") {
        joined = true;
      } else if (card.dataset.joined === "false") {
        joined = false;
      } else {
        const txt = button.textContent.toLowerCase();
        joined = txt.includes("joined");
      }

      function render() {
        card.dataset.joined = joined ? "true" : "false";

        if (joined) {
          // Joined state
          button.classList.add("joined");
          button.classList.remove("outline");
          button.innerHTML = '<i class="fas fa-check"></i> Joined';
        } else {
          // Not joined state
          button.classList.add("outline");
          button.classList.remove("joined");
          button.textContent = "Join Community";
        }
      }

      // Set initial state
      render();

      // Click → toggle
      button.addEventListener("click", async () => {
        joined = !joined;
        render();

        // OPTIONAL: connect to backend (uncomment + adjust)
        /*
        const communityId = card.dataset.id; // make sure data-id exists on card
        try {
          await fetch(`/api/communities/${communityId}/${joined ? "join" : "leave"}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include"
          });
        } catch (err) {
          console.error("Failed to update join state:", err);
          // If you want to revert UI on error:
          // joined = !joined;
          // render();
        }
        */
        applyFilters(); // keep filters correct after toggling
      });
    });
  }

  /* =========================
     FILTER + SEARCH
     ========================= */
  function applyFilters() {
    if (!cards.length) return;

    const term = (searchInput?.value || "").trim().toLowerCase();
    const activeFilterBtn = document.querySelector(".filter-pill.is-active");
    const filter = activeFilterBtn?.dataset.filter || "all"; // all | joined | discover

    cards.forEach((card) => {
      const name = (card.dataset.name || "").toLowerCase();
      const joined = card.dataset.joined === "true";

      let visible = true;

      // search by name
      if (term && !name.includes(term)) {
        visible = false;
      }

      // filter by joined status
      if (filter === "joined" && !joined) {
        visible = false;
      }
      if (filter === "discover" && joined) {
        visible = false;
      }

      card.style.display = visible ? "grid" : "none";
    });
  }

  function initSearch() {
    if (!searchInput) return;
    searchInput.addEventListener("input", applyFilters);
  }

  function initFilterPills() {
    if (!filterButtons.length) return;
    filterButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterButtons.forEach((b) => b.classList.remove("is-active"));
        btn.classList.add("is-active");
        applyFilters();
      });
    });
  }

  /* =========================
     INIT
     ========================= */
  initJoinButtons();
  initSearch();
  initFilterPills();
  applyFilters();
});
