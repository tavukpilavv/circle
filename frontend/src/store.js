import { reactive } from "vue"
import { apiFetch } from "./api"

export const store = reactive({
  communities: [],
  events: [],
  notifications: [],
  // Kullanıcı bilgisi (Admin kontrolü ve hoşgeldin mesajı için)
  user: JSON.parse(localStorage.getItem('user_info') || '{}'),
  userRole: (localStorage.getItem("user_role") || "").toLowerCase(),
  userId: Number(localStorage.getItem("user_id") || 0),

  refreshAuth() {
    this.userRole = (localStorage.getItem("user_role") || "").toLowerCase()
    this.userId = Number(localStorage.getItem("user_id") || 0)
    this.user = JSON.parse(localStorage.getItem("user_info") || "{}")
  },

  async loadCommunitiesFromBackend() {
    try {
      const res = await apiFetch("/api/general/communities", { method: "GET" })
      if (!res.ok) return

      const data = await res.json().catch(() => [])
      this.communities = (Array.isArray(data) ? data : []).map((c) => ({
        id: c.id,
        name: c.name,
        description: c.description || "",
        members: c.members_count ?? 0,
        image: c.image_url || "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=800&q=80",
        website_url: c.website_url || c.external_link || "",
        admin_id: c.admin_id ?? null

      }))
    } catch (e) {
      console.error("loadCommunitiesFromBackend failed:", e)
    }
  },
  async rejectApplication(id) {
    try {
      const res = await apiFetch(`/api/general/communities/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user_token")}`
        }
      });

      const data = await res.json().catch(() => ({}));
      return { success: res.ok, ...data };
    } catch (e) {
      return { success: false, message: e.message };
    }
  },
  // --- KAYIT OLMA (REGISTER) ---
  async registerEvent(event) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) {
        alert("Lütfen önce giriş yapın.")
        return false
      }

      const eventId = event.id ? event.id : event

      const res = await apiFetch(`/api/general/events/${eventId}/register`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      })

      const data = await res.json()

      if (!res.ok) {
        if (res.status === 400 && (data.message === "Zaten kayıtlısınız" || (data.message || "").includes("registered"))) {
          if (typeof event === 'object') event.registered = true
          return true
        }
        throw new Error(data.message || data.error || "Kayıt başarısız oldu")
      }

      if (typeof event === 'object') {
        event.registered = true
      }

      return true
    } catch (e) {
      console.error("Register error:", e)
      alert(e.message || "Bir hata oluştu")
      throw e
    }
  },

  // --- KAYIT İPTALİ (UNREGISTER) ---
  async unregisterEvent(event) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) throw new Error("Giriş yapmalısınız")

      const eventId = event.id ? event.id : event

      const res = await apiFetch(`/api/general/events/${eventId}/unregister`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.error || "Kayıt iptali başarısız")
      }

      if (typeof event === 'object') {
        event.registered = false
      }
      return true
    } catch (e) {
      console.error("Unregister error:", e)
      return false
    }
  },

  // --- RATING (PUANLAMA) ---
  async addReview({ eventId, rating, comment, isAnonymous }) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) throw new Error("Giriş yapmalısınız")

      const payload = {
        rating: rating,
        feedback: comment,
        is_anonymous: isAnonymous
      }

      const res = await apiFetch(`/api/general/events/${eventId}/rate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      })

      const data = await res.json()
      if (!res.ok) throw new Error(data.error || "Hata oluştu")

      const eventToUpdate = this.events.find(e => e.id === eventId)
      if (eventToUpdate && data.new_rating !== undefined) {
        eventToUpdate.rating = data.new_rating
      }
      return true
    } catch (e) {
      console.error("addReview failed:", e)
      throw e
    }
  },

  // --- YORUMLARI GETİR ---
  async fetchReviews(eventId) {
    try {
      const res = await apiFetch(`/api/general/events/${eventId}/reviews`)
      if (res.ok) return await res.json()
    } catch (e) { console.error(e) }
    return []
  },

  // ✅ YENİ: PARTICIPANTS GETİR
  async fetchParticipants(eventId) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) throw new Error("Missing token. Please login.")

      const res = await apiFetch(`/api/general/events/${eventId}/participants`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.msg || data.error || `Request failed (${res.status})`)
      }

      const data = await res.json().catch(() => [])
      return Array.isArray(data) ? data : []
    } catch (e) {
      console.error("fetchParticipants failed:", e)
      throw e
    }
  },

  // --- DİĞER STANDART FONKSİYONLAR ---
  async createCommunityMultipart(payload) { return this._genericPost("/api/general/communities", payload, true) },
  async createCommunityLegacyJson(payload) { return this._genericPost("/api/general/communities/create", payload, false) },

  async _genericPost(url, body, isFormData) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) { alert("Please login"); return false }
      const options = {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: isFormData ? body : JSON.stringify(body)
      }
      if (!isFormData) options.headers["Content-Type"] = "application/json"

      const res = await apiFetch(url, options)
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        alert(data.error || "İşlem başarısız")
        return false
      }
      await this.loadCommunitiesFromBackend()
      return true
    } catch (e) { console.error(e); return false }
  },
  async loadEvents() {
    try {
      const res = await apiFetch("/api/general/events");
      if (!res.ok) return;

      const data = await res.json().catch(() => []);
      this.events = Array.isArray(data) ? data : [];
    } catch (err) {
      console.error("loadEvents failed:", err);
    }
  },
  async deleteEvent(id) {
    try {
      const { deleteEvent } = await import("./api")
      await deleteEvent(id)
      this.events = this.events.filter(e => e.id !== id)
      return true
    } catch (e) { console.error(e); return false }
  },

  async deleteCommunity(id) {
    try {
      const { deleteCommunity } = await import("./api")
      await deleteCommunity(id)
      this.communities = this.communities.filter(c => c.id !== id)
      return true
    } catch (e) { console.error(e); return false }
  },

  async updateEvent(id, fd) {
    try {
      const { updateEvent } = await import("./api")
      await updateEvent(id, fd)

      const res = await apiFetch("/api/general/events")
      if (res.ok) this.events = await res.json()
      return true
    } catch (e) { console.error(e); return false }
  },

  getReviewsByEventId(id) { return [] },
  canEditCommunity(community) {
    if (!community) return false

    if (this.userRole === "super_admin" || this.userRole === "superadmin")
      return true

    if (this.userRole === "admin" && community.admin_id === this.userId)
      return true

    return false
  },
  canEditEvent(event) {
    if (!event) return false

    // Super admin can edit everything
    if (this.userRole === "super_admin" || this.userRole === "superadmin")
      return true

    // If communities not loaded yet, we can't know ownership safely.
    // communities App.vue’de admin ise preload ediliyor
    const comm = this.communities.find(c => c.id === event.community_id)
    if (!comm) return false

    return this.userRole === "admin" && comm.admin_id === this.userId
  }
})