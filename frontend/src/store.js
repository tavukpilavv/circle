import { reactive } from 'vue'
import client from './api/client'

export const store = reactive({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  communities: [],
  events: [],

  // ================= AUTH =================
  async login(credentials) {
    try {
      const response = await client.post('/auth/login', credentials);
      this.user = response.data.user;
      localStorage.setItem('user', JSON.stringify(this.user));
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Login failed' };
    }
  },

  async register(userData) {
    try {
      await client.post('/auth/register', userData);
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Registration failed' };
    }
  },

  logout() {
    this.user = null;
    localStorage.removeItem('user');
  },

  // ================= COMMUNITIES =================
  async fetchCommunities() {
    try {
      const response = await client.get('/general/communities');
      this.communities = response.data;
    } catch (error) {
      console.error('Failed to fetch communities:', error);
    }
  },

  async createClub(clubData) {
    try {
      const formData = new FormData();
      Object.keys(clubData).forEach(key => formData.append(key, clubData[key]));
      // Add user_id manually if not in clubData, though backend expects it in form or session
      if (this.user) formData.append('user_id', this.user.id);

      const response = await client.post('/general/communities/create', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      await this.fetchCommunities(); // Refresh list
      return { success: true, message: response.data.message };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Failed to create club' };
    }
  },

  async joinCommunity(communityId) {
    if (!this.user) return { success: false, message: 'Please login first' };
    try {
      await client.post(`/general/communities/${communityId}/join`, { user_id: this.user.id });
      // Optimistic update or refresh
      const target = this.communities.find(c => c.id === communityId);
      if (target) {
        target.joined = true;
        target.member_count++;
      }
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Failed to join' };
    }
  },

  // ================= EVENTS =================
  async fetchEvents() {
    try {
      const response = await client.get('/general/events');
      this.events = response.data;
    } catch (error) {
      console.error('Failed to fetch events:', error);
    }
  },

  async createEvent(eventData) {
    try {
      const formData = new FormData();
      Object.keys(eventData).forEach(key => formData.append(key, eventData[key]));
      if (this.user) formData.append('user_id', this.user.id);

      await client.post('/general/events/create', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      await this.fetchEvents();
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Failed to create event' };
    }
  },

  async registerEvent(event) {
    if (!this.user) return { success: false, message: 'Please login first' };
    try {
      await client.post(`/general/events/${event.id}/register`, { user_id: this.user.id });
      const target = this.events.find(e => e.id === event.id);
      if (target) target.registered = true;
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Failed to register' };
    }
  },

  async rateEvent(eventId, rating, feedback, isAnonymous = false) {
    if (!this.user) return { success: false, message: 'Please login first' };
    try {
      const response = await client.post(`/general/events/${eventId}/rate`, {
        user_id: this.user.id,
        rating,
        feedback,
        is_anonymous: isAnonymous
      });

      // Update local state
      const event = this.events.find(e => e.id === eventId);
      if (event) {
        event.rating = response.data.new_rating;
        // event.ratingCount++; // Backend handles this, we might need to refresh or trust response
      }
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Failed to rate' };
    }
  },

  async deleteEvent(eventId) {
    try {
      await client.delete(`/general/events/${eventId}`);
      this.events = this.events.filter(e => e.id !== eventId);
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.error || 'Failed to delete' };
    }
  }
})
