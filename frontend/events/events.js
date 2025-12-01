/* ============================================
   0) CLUB NAMES (SYNCED WITH COMMUNITIES PAGE)
   ============================================ */
const CLUBS = [
  "Computer Science Club",
  "Engineering Society",
  "Alumni Association",
  "Career Services"
];

/* ============================================
   0.5) USER CACHE & API
   ============================================ */
let currentUserCache = null;

async function fetchCurrentUser() {
  if (currentUserCache) return currentUserCache;

  try {
    const response = await fetch("/api/users/me", {
      method: "GET",
      credentials: "include", // in case you use cookies/session
      headers: {
        "Accept": "application/json"
      }
    });

    if (!response.ok) {
      console.error("Failed to fetch /api/users/me", response.status);
      return null;
    }

    const data = await response.json();
    currentUserCache = data;
    return data;
  } catch (err) {
    console.error("Error calling /api/users/me:", err);
    return null;
  }
}

/* ============================================
   1) ADMIN VISIBILITY (create / edit / modal)
   ============================================ */
function initAdminVisibility() {
  const role = document.body.dataset.role;
  const isAdmin = role === "admin";

  const createBtn = document.getElementById("openCreateEventModal");
  const editBtns = document.querySelectorAll(".event-edit-btn");
  const modal = document.getElementById("eventModal");

  if (!isAdmin) {
    if (createBtn) createBtn.style.display = "none";
    editBtns.forEach((btn) => (btn.style.display = "none"));

    if (modal) {
      modal.dataset.adminOnly = "true";
    }
  }
}

/* ============================================
   1.5) POPULATE CLUB DROPDOWN
   ============================================ */
function populateClubDropdown() {
  const select = document.getElementById("eventClubField");
  if (!select) return;

  // clear existing
  select.innerHTML = "";

  // default placeholder
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Select a club";
  select.appendChild(placeholder);

  // add known clubs (from communities)
  CLUBS.forEach((club) => {
    const opt = document.createElement("option");
    opt.value = club;
    opt.textContent = club;
    select.appendChild(opt);
  });
}

/* ============================================
   1.6) SET DEFAULT CLUB FOR CREATE (BACKEND DATA)
   ============================================ */
async function setDefaultClubForCreate(clubField) {
  if (!clubField) return;

  // always enable first, we may disable after
  clubField.disabled = false;

  const user = await fetchCurrentUser();
  if (!user || !Array.isArray(user.managed_clubs)) {
    // no user or structure → keep dropdown editable with placeholder
    clubField.value = "";
    return;
  }

  const managed = user.managed_clubs;
  if (managed.length === 1) {
    const clubName = managed[0].club_name;

    // ensure this club exists in dropdown options; if not, add it
    let option = Array.from(clubField.options).find(
      (opt) => opt.value === clubName
    );
    if (!option) {
      option = document.createElement("option");
      option.value = clubName;
      option.textContent = clubName;
      clubField.appendChild(option);
    }

    clubField.value = clubName;
    // lock it so president doesn't change it
    clubField.disabled = true;
  } else {
    // user manages multiple clubs → keep editable
    clubField.value = "";
    clubField.disabled = false;
  }
}

/* ============================================
   2) CREATE / EDIT EVENT MODAL (ADMIN ONLY)
   ============================================ */
function initEventModal() {
  const role = document.body.dataset.role;
  const isAdmin = role === "admin";
  if (!isAdmin) return;

  const modal = document.getElementById("eventModal");
  const openBtn = document.getElementById("openCreateEventModal");
  const closeBtn = document.getElementById("closeEventModal");
  const cancelBtn = document.getElementById("cancelEventBtn");
  const form = document.getElementById("eventForm");
  const titleEl = document.getElementById("eventModalTitle");
  const submitBtn = document.getElementById("submitEventBtn");

  const idField = document.getElementById("eventIdField");
  const nameField = document.getElementById("eventNameField");
  const dateField = document.getElementById("eventDateField");
  const locationField = document.getElementById("eventLocationField");
  const capacityField = document.getElementById("eventCapacityField");
  const descField = document.getElementById("eventDescriptionField");
  const clubField = document.getElementById("eventClubField");

  if (!modal || !form) return;

  // populate dropdown options once
  populateClubDropdown();

  function openModal(mode, data) {
    if (mode === "edit" && data) {
      titleEl.textContent = "Edit Event";
      submitBtn.textContent = "Save Changes";

      idField.value = data.id || "";
      nameField.value = data.name || "";
      dateField.value = data.date || "";
      locationField.value = data.location || "";
      capacityField.value = data.capacity || "";
      descField.value = data.description || "";

      // make sure it's enabled for edit (admin may change if allowed)
      clubField.disabled = false;

      // ensure option exists, then set
      if (data.club) {
        let opt = Array.from(clubField.options).find(
          (o) => o.value === data.club
        );
        if (!opt) {
          opt = document.createElement("option");
          opt.value = data.club;
          opt.textContent = data.club;
          clubField.appendChild(opt);
        }
        clubField.value = data.club;
      } else {
        clubField.value = "";
      }
    } else {
      titleEl.textContent = "Create Event";
      submitBtn.textContent = "Submit";
      form.reset();
      idField.value = "";

      // for create: set default from backend (president's club if unique)
      setDefaultClubForCreate(clubField);
    }

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  // open create
  if (openBtn) {
    openBtn.addEventListener("click", () => openModal("create"));
  }

  // close
  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (cancelBtn) cancelBtn.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  // open edit
  document.querySelectorAll(".event-edit-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".event-card");
      if (!card) return;

      const data = {
        id: card.dataset.id,
        name: card.dataset.name,
        date: card.dataset.date,
        location: card.dataset.location,
        capacity: card.dataset.capacity,
        description: card.dataset.description,
        club: card.dataset.club || ""
      };

      openModal("edit", data);
    });
  });

  // submit – later you connect to backend
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = Object.fromEntries(new FormData(form).entries());
    console.log("Event form submitted (send this to backend):", formData);

    // TODO: send formData to your API with fetch()
    // fetch('/api/events', { method: 'POST', body: JSON.stringify(formData), ... })

    closeModal();
  });
}

/* ============================================
   3) FILTERS: UPCOMING / PAST / ALL
   ============================================ */
function initEventFilters() {
  const filterButtons = document.querySelectorAll(".filter-pill");
  const cards = document.querySelectorAll(".event-card");
  if (!filterButtons.length || !cards.length) return;

  function parseDate(dateStr) {
    if (!dateStr) return null;
    const [y, m, d] = dateStr.split("-").map(Number);
    if (!y || !m || !d) return null;
    return new Date(y, m - 1, d);
  }

  const today = (() => {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), now.getDate());
  })();

  let activeFilter = "upcoming";

  function applyFilter() {
    cards.forEach((card) => {
      const dateStr = card.dataset.date;
      const cardDate = parseDate(dateStr);

      let isPast = false;
      let isUpcoming = true;

      if (cardDate) {
        if (cardDate < today) {
          isPast = true;
          isUpcoming = false;
        } else {
          isPast = false;
          isUpcoming = true;
        }
      }

      let visible = true;

      if (activeFilter === "upcoming" && !isUpcoming) visible = false;
      if (activeFilter === "past" && !isPast) visible = false;
      // "all" => always visible

      card.style.display = visible ? "grid" : "none";
    });
  }

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterButtons.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");

      activeFilter = btn.dataset.filter || "all";
      applyFilter();
    });
  });

  applyFilter();
}

/* ============================================
   4) REGISTER BUTTONS
   ============================================ */
function initRegisterButtons() {
  const registerBtns = document.querySelectorAll(".event-primary-btn");

  registerBtns.forEach((btn) => {
    // If already registered (static HTML might say so), disable it
    if (btn.textContent.trim().toLowerCase() === "registered") {
      btn.disabled = true;
    }

    btn.addEventListener("click", () => {
      btn.textContent = "Registered";
      btn.disabled = true;
      // Optional: Add a class if you want specific styling for registered state
      // btn.classList.add("is-registered");
    });
  });
}

/* ============================================
   INIT
   ============================================ */
document.addEventListener("DOMContentLoaded", () => {
  initAdminVisibility();
  initEventModal();
  initEventFilters();
  initRegisterButtons();
});
