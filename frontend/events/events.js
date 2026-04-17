/* =========================
   CirCle - Events (Create Event)
   Dynamic community dropdown from DB
   Admin: 1 community only (locked)
   Super Admin: all communities
   ========================= */

const API = {
  COMMUNITY_OPTIONS: "/api/general/communities/options",
  CREATE_EVENT: "/api/general/events/create",
};

// If your token key is different, change it here.
function getToken() {
  return localStorage.getItem("user_token");
}

function $(id) {
  return document.getElementById(id);
}

async function apiFetch(url, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };

  if (token) headers.Authorization = `Bearer ${token}`;

  return fetch(url, {
    credentials: "include",
    ...options,
    headers,
  });
}

/* =========================
   MODAL OPEN/CLOSE
   ========================= */
function openModal() {
  const modal = $("eventModal");
  if (!modal) return;

  modal.style.display = "flex";
  modal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  const modal = $("eventModal");
  if (!modal) return;

  modal.style.display = "none";
  modal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

/* =========================
   COMMUNITY DROPDOWN
   ========================= */
async function fetchCommunityOptions() {
  const res = await apiFetch(API.COMMUNITY_OPTIONS, { method: "GET" });

  if (!res.ok) {
    // Most common: not logged in -> 401/422
    const txt = await res.text().catch(() => "");
    throw new Error(`Failed to load communities (${res.status}). ${txt}`);
  }

  return res.json();
}

function populateCommunityDropdown(list) {
  const select = $("eventCommunityField");
  if (!select) return;

  // Clear options
  select.innerHTML = "";

  // Placeholder (only useful for super_admin)
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Select a community";
  select.appendChild(placeholder);

  list.forEach((c) => {
    const opt = document.createElement("option");
    opt.value = String(c.id); // ✅ Use ID
    opt.textContent = c.name;
    select.appendChild(opt);
  });

  // Admin scenario: only one community returned
  if (list.length === 1) {
    select.value = String(list[0].id);
    select.disabled = true; // lock it
  } else {
    select.disabled = false;
    select.value = ""; // force selection for super_admin
  }
}

/* =========================
   SUBMIT CREATE EVENT
   ========================= */
async function handleCreateEventSubmit(e) {
  e.preventDefault();

  const communityId = $("eventCommunityField")?.value;
  if (!communityId) {
    alert("Please select a community.");
    return;
  }

  const name = $("eventNameField")?.value?.trim() || "";
  if (!name) {
    alert("Event name is required.");
    return;
  }

  const fd = new FormData();

  // Backend accepts title from: name/eventName/title.
  fd.append("name", name);
  fd.append("date", $("eventDateField")?.value || "");
  fd.append("time", $("eventTimeField")?.value || ""); // if you have a time input
  fd.append("location", $("eventLocationField")?.value || "");
  fd.append("capacity", $("eventCapacityField")?.value || "");
  fd.append("description", $("eventDescriptionField")?.value || "");

  // ✅ REQUIRED: community_id (NOT club name)
  fd.append("community_id", communityId);

  // ✅ Optional event image file
  const file = $("eventImageInput")?.files?.[0];
  if (file) {
    // backend reads request.files.get("file") or request.files.get("image")
    fd.append("image", file);
  }

  const submitBtn = $("submitEventBtn");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.style.opacity = "0.7";
  }

  try {
    const res = await apiFetch(API.CREATE_EVENT, {
      method: "POST",
      body: fd,
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.error || `Create event failed (${res.status})`);
    }

    alert("Event created successfully!");
    closeModal();

    // Optional: reload or refresh events list if you render it dynamically
    // location.reload();

  } catch (err) {
    alert(err.message || "Failed to create event");
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.style.opacity = "1";
    }
  }
}

/* =========================
   INIT
   ========================= */
document.addEventListener("DOMContentLoaded", () => {
  const openBtn = $("openCreateEventModal");
  const closeBtn = $("closeEventModal");
  const cancelBtn = $("cancelEventBtn");
  const modal = $("eventModal");
  const form = $("eventForm");

  // Open create modal -> load communities -> open
  if (openBtn) {
    openBtn.addEventListener("click", async () => {
      try {
        // Reset form UI
        form?.reset();
        if ($("eventImageInput")) $("eventImageInput").value = "";

        // Load dropdown options from backend
        const list = await fetchCommunityOptions();
        populateCommunityDropdown(list);

        openModal();
      } catch (err) {
        alert(err.message || "Could not load communities. Please login again.");
      }
    });
  }

  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (cancelBtn) cancelBtn.addEventListener("click", closeModal);

  // Click outside modal content closes it
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeModal();
    });
  }

  // Submit create event
  if (form) {
    form.addEventListener("submit", handleCreateEventSubmit);
  }
});
