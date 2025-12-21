import { reactive } from "vue"
import { apiFetch } from "./api"

export const store = reactive({
  communities: [],
  events: [],
  notifications: [],

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
        image:
          c.image_url ||
          "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=800&q=80",
        website_url: c.website_url || c.external_link || ""
      }))
    } catch (e) {
      console.error("loadCommunitiesFromBackend failed:", e)
    }
  },


  async createCommunityMultipart({ name, description, website_url, imageFile }) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) {
        alert("Please login first.")
        return false
      }

      if (!imageFile) {
        alert("Please select an image file.")
        return false
      }

      const fd = new FormData()
      fd.append("name", name || "")
      fd.append("description", description || "")
      fd.append("website_url", website_url || "")
      fd.append("image", imageFile)

      const res = await apiFetch("/api/general/communities", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: fd
      })

      const data = await res.json().catch(() => ({}))
      if (!res.ok || data.error) {
        alert(data.error || "Failed to create community")
        return false
      }

      await this.loadCommunitiesFromBackend()
      return true
    } catch (e) {
      console.error("createCommunityMultipart failed:", e)
      alert("Failed to create community")
      return false
    }
  },

  async createCommunityLegacyJson({ name, description, image_url, website_url }) {
    try {
      const token = localStorage.getItem("user_token")
      if (!token) {
        alert("Please login first.")
        return false
      }

      const payload = {
        clubName: name,
        description: description,
        shortDescription: description,
        clubImage: image_url || null,
        website_url: website_url || ""
      }

      const res = await apiFetch("/api/general/communities/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      })

      const data = await res.json().catch(() => ({}))
      if (!res.ok || data.error) {
        alert(data.error || "Failed to create community")
        return false
      }

      await this.loadCommunitiesFromBackend()
      return true
    } catch (e) {
      console.error("createCommunityLegacyJson failed:", e)
      alert("Failed to create community")
      return false
    }
  },

  async deleteEvent(eventId) {
    try {
      const { deleteEvent } = await import("./api")
      await deleteEvent(eventId)

      // Update local state
      this.events = this.events.filter(e => e.id !== eventId)
      return true
    } catch (e) {
      console.error("Failed to delete event:", e)
      alert(e.message || "Failed to delete event")
      return false
    }
  },

  async deleteCommunity(id) {
    try {
      const { deleteCommunity } = await import("./api")
      await deleteCommunity(id)

      this.communities = this.communities.filter(c => c.id !== id)
      return true
    } catch (e) {
      console.error("Failed to delete community:", e)
      alert(e.message || "Failed to delete community")
      return false
    }
  }
})
