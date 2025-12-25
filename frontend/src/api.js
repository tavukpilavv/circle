
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/+$/, "");

const TOKEN_KEY = "user_token";

/* =========================
   TOKEN
   ========================= */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

/* =========================
   CORE FETCH
   ========================= */
export async function apiFetch(path, options = {}) {
  if (!path.startsWith("/")) path = "/" + path;

  const finalOptions = {
    credentials: "include",
    ...options,
  };

  const headers = { ...(options.headers || {}) };

  const token = getToken();
  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }


  if (finalOptions.body && !(finalOptions.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  finalOptions.headers = headers;

  return fetch(API_BASE_URL + path, finalOptions);
}

/* =========================
   RESPONSE HELPERS
   ========================= */
async function parseResponse(res) {
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json().catch(() => null);
  }
  return res.text().catch(() => "");
}

async function handle(res) {
  const data = await parseResponse(res);
  if (!res.ok) {
    const msg =
      (data && typeof data === "object" && (data.error || data.message)) ||
      (typeof data === "string" && data) ||
      `Request failed (${res.status})`;
    throw new Error(msg);
  }
  return data;
}

/* =========================
   GENERIC REQUESTS
   ========================= */
export async function get(path) {
  const res = await apiFetch(path, { method: "GET" });
  return handle(res);
}

export async function postJson(path, bodyObj) {
  const res = await apiFetch(path, {
    method: "POST",
    body: JSON.stringify(bodyObj ?? {}),
  });
  return handle(res);
}

export async function postForm(path, formData) {
  const res = await apiFetch(path, {
    method: "POST",
    body: formData,
  });
  return handle(res);
}


export async function del(path) {
  const res = await apiFetch(path, { method: "DELETE" });
  return handle(res);
}

export async function putForm(path, formData) {
  const res = await apiFetch(path, {
    method: "PUT",
    body: formData,
  });
  return handle(res);
}

/* =========================
   EVENTS (General Blueprint)
   ========================= */

export async function getEvents(q = "") {
  const qs = q ? `?q=${encodeURIComponent(q)}` : "";
  return get(`/api/general/events${qs}`);
}

export async function createEvent(formData) {
  return postForm("/api/general/events/create", formData);
}

export async function updateEvent(eventId, formData){
  return putForm(`/api/general/events/${eventId}`, formData);
}


export async function registerEvent(eventId) {
  return post(`/api/general/events/${eventId}/register`);
}

export async function unregisterEvent(eventId) {
  return post(`/api/general/events/${eventId}/unregister`);
}



export async function rateEvent(eventId, payload) {
  return postJson(`/api/general/events/${eventId}/rate`, payload);
}


export async function getEventReviews(eventId) {
  return get(`/api/general/events/${eventId}/reviews`);
}

export async function deleteReview(reviewId) {
  return del(`/api/general/reviews/${reviewId}`);
}


export async function deleteEvent(eventId) {
  return del(`/api/general/events/${eventId}`);
}

/* =========================
   COMMUNITIES (General Blueprint)
   ========================= */

export async function getCommunities() {
  return get("/api/general/communities");
}


export async function getCommunityOptions() {
  return get("/api/general/communities/options");
}


export async function createCommunity(formData) {
  return postForm("/api/general/communities", formData);
}

export async function deleteCommunity(id) {
  return del(`/api/general/communities/${id}`);
}

/* =========================
   SMALL FIX: POST shortcut
   (used above by registerEvent)
   ========================= */
async function post(path) {
  const res = await apiFetch(path, { method: "POST" });
  return handle(res);
}
