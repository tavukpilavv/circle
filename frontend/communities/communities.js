document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------
  // CONFIG
  // -----------------------------
  const API = "/api/general/communities"; // Flask endpoint
  const token = localStorage.getItem("user_token");
  const role = localStorage.getItem("user_role"); // "admin" or "super_admin"

  // -----------------------------
  // DOM
  // -----------------------------
  const listEl = document.getElementById("communityList");
  const searchInput = document.getElementById("communitySearchInput");
  const filterBtns = document.querySelectorAll(".filter-pill");

  const openCreateBtn = document.getElementById("openCreateBtn");
  const modalOverlay = document.getElementById("modalOverlay");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const createForm = document.getElementById("createCommunityForm");
  const formMsg = document.getElementById("formMsg");
  const submitBtn = document.getElementById("submitBtn");
  const fileInput = document.getElementById("cImage");
  const fileHint = document.getElementById("fileHint");

  // only show add button for admins
  const isAdmin = role === "admin" || role === "super_admin";
  if (!isAdmin) {
    openCreateBtn.classList.add("is-hidden");
  }

  let communities = [];
  let activeFilter = "all";

  // -----------------------------
  // HELPERS
  // -----------------------------
  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (m) => (
      { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[m]
    ));
  }

  function validHttpUrl(url) {
    try {
      const u = new URL(url);
      return u.protocol === "http:" || u.protocol === "https:";
    } catch {
      return false;
    }
  }

  function openModal() {
    modalOverlay.classList.add("is-open");
    document.body.style.overflow = "hidden";
    formMsg.textContent = "";
  }

  function closeModal() {
    modalOverlay.classList.remove("is-open");
    document.body.style.overflow = "";
    createForm.reset();
    fileHint.textContent = "";
  }

  // -----------------------------
  // API
  // -----------------------------
  async function fetchCommunities() {
    const res = await fetch(API, { credentials: "include" });
    if (!res.ok) throw new Error("Failed to load communities");
    return res.json();
  }

  async function createCommunity(fd) {
    if (!token) throw new Error("You must login first (missing token).");

    const res = await fetch(API, {
      method: "POST",
      body: fd,
      credentials: "include",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      const txt = await res.text().catch(() => "");
      throw new Error(txt || "Failed to create community");
    }
    return res.json();
  }

  // -----------------------------
  // RENDER
  // -----------------------------
  function cardHTML(c) {
    const img = c.image_url || "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80";
    const website = (c.website_url || "").trim();
    const members = Number.isFinite(c.members_count) ? c.members_count : (c.members_count ?? 0);

    const disabled = website ? "" : "disabled";
    return `
      <article class="community-card" data-name="${escapeHtml(c.name)}" data-website="${escapeHtml(website)}">
        <img class="community-image" src="${escapeHtml(img)}" alt="" />

        <div class="community-main">
          <h2 class="community-name">${escapeHtml(c.name)}</h2>
          <p class="community-desc">${escapeHtml(c.description || "")}</p>
          <div class="community-meta">
            <span><i class="fas fa-user-group"></i> ${members} members</span>
          </div>
        </div>

        <button class="status-pill visit-btn" type="button" ${disabled}>
          Visit Website
        </button>
      </article>
    `;
  }

  function render(items) {
    if (!items.length) {
      listEl.innerHTML = `<div class="empty-state">No communities found.</div>`;
      return;
    }
    listEl.innerHTML = items.map(cardHTML).join("");
    bindVisitButtons();
  }

  function bindVisitButtons() {
    document.querySelectorAll(".visit-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const card = btn.closest(".community-card");
        const url = card?.dataset.website || "";
        if (!url) return;

        if (!validHttpUrl(url)) {
          alert("Invalid website URL.");
          return;
        }
        window.open(url, "_blank", "noopener,noreferrer");
      });
    });
  }

  // -----------------------------
  // FILTERS + SEARCH
  // -----------------------------
  function applyFilters() {
    const term = (searchInput.value || "").trim().toLowerCase();

    const filtered = communities.filter((c) => {
      const name = (c.name || "").toLowerCase();
      const website = (c.website_url || "").trim();
      const hasWebsite = !!website;

      if (term && !name.includes(term)) return false;

      if (activeFilter === "hasWebsite" && !hasWebsite) return false;
      if (activeFilter === "noWebsite" && hasWebsite) return false;

      return true;
    });

    render(filtered);
  }

  // -----------------------------
  // INIT UI EVENTS
  // -----------------------------
  if (searchInput) searchInput.addEventListener("input", applyFilters);

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      activeFilter = btn.dataset.filter || "all";
      applyFilters();
    });
  });

  if (openCreateBtn) openCreateBtn.addEventListener("click", () => {
    if (!isAdmin) return;
    openModal();
  });

  if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
  if (modalOverlay) modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      const f = e.target.files?.[0];
      fileHint.textContent = f ? `Selected: ${f.name}` : "";
    });
  }

  // -----------------------------
  // CREATE FORM SUBMIT
  // -----------------------------
  if (createForm) {
    createForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      formMsg.textContent = "";

      const fd = new FormData(createForm);

      const website = (fd.get("website_url") || "").toString().trim();
      if (!validHttpUrl(website)) {
        formMsg.textContent = "Website URL must start with http:// or https://";
        return;
      }

      const img = fd.get("image");
      if (!img || !(img instanceof File) || img.size === 0) {
        formMsg.textContent = "Please choose an image file.";
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = "Creating...";

      try {
        await createCommunity(fd);

        // reload list
        communities = await fetchCommunities();
        applyFilters();

        closeModal();
      } catch (err) {
        formMsg.textContent = err?.message || "Failed to create community";
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Create";
      }
    });
  }

  // -----------------------------
  // INIT LOAD
  // -----------------------------
  (async function init() {
    try {
      communities = await fetchCommunities();
      applyFilters();
    } catch (err) {
      console.error(err);
      listEl.innerHTML = `<div class="empty-state">Failed to load communities.</div>`;
    }
  })();
});
