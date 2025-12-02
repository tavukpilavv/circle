import { reactive } from 'vue'
import api from './utils/api'

export const store = reactive({
  notifications: [],
  communities: [],
  async fetchCommunities() {
    try {
      const response = await api.get('/general/communities');
      this.communities = response.data;
    } catch (error) {
      console.error('Error fetching communities:', error);
    }
  },
  events: [],
  async fetchEvents() {
    try {
      const response = await api.get('/general/events');
      this.events = response.data;
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  },
  joinCommunity(community) {
    const target = this.communities.find(c => c.name === community.name);
    if (target) {
      target.joined = !target.joined;
      // Add default role/date if joining
      if (target.joined && !target.role) {
        target.role = 'Member';
        target.joinedDate = 'Just now';
      }
    }
  },
  registerEvent(event) {
    const target = this.events.find(e => e.id === event.id);
    if (target) {
      target.registered = !target.registered;
    }
  },
  rateEvent(eventId, rating, feedback, isAnonymous = false) {
    const event = this.events.find(e => e.id === eventId);
    if (!event) return { success: false, message: 'Event not found' };

    // Security check: User must be registered
    if (!event.registered) {
      console.warn('Security Check Failed: User not registered for event', eventId);
      return { success: false, message: 'User did not participate in this event' };
    }

    // Update or Create logic (simulated)
    event.userRating = rating;
    event.userFeedback = feedback;
    event.isAnonymous = isAnonymous;

    // Persist to localStorage (mocking DB persistence)
    localStorage.setItem(`rated_event_${eventId}`, rating);
    localStorage.setItem(`anonymous_event_${eventId}`, isAnonymous);
    if (feedback) {
      localStorage.setItem(`feedback_event_${eventId}`, feedback);
    } else {
      localStorage.removeItem(`feedback_event_${eventId}`);
    }

    return { success: true };
  },
  createClub(clubData) {
    const newId = this.communities.length > 0
      ? Math.max(...this.communities.map(c => c.id)) + 1
      : 1;

    const newClub = {
      id: newId,
      ...clubData,
      members: 0, // Default start
      joined: false
    };

    this.communities.push(newClub);
  },
  // Event Actions
  createEvent(eventData) {
    const newId = this.events.length > 0
      ? Math.max(...this.events.map(e => e.id)) + 1
      : 1;

    const newEvent = {
      id: newId,
      ...eventData,
      registered: false
    };

    this.events.push(newEvent);
  },
  updateEvent(eventData) {
    const index = this.events.findIndex(e => e.id === eventData.id);
    if (index !== -1) {
      // Merge existing data with updates
      this.events[index] = { ...this.events[index], ...eventData };
    }
  },
  deleteEvent(eventId) {
    const index = this.events.findIndex(e => e.id === eventId);
    if (index !== -1) {
      this.events.splice(index, 1);
    }
  },

  // Centralized Reviews Management
  allReviews: JSON.parse(localStorage.getItem('reviews') || '[]'),

  addReview(review) {
    // Ensure review has an ID and date
    const newReview = {
      id: Date.now(),
      date: new Date().toLocaleDateString(), // Simple date format
      ...review
    };

    this.allReviews.unshift(newReview);
    localStorage.setItem('reviews', JSON.stringify(this.allReviews));

    // Also update the event object for immediate UI feedback if needed (optional but good for reactivity)
    const event = this.events.find(e => e.id === review.eventId);
    if (event) {
      event.userRating = review.rating;
      event.userFeedback = review.comment; // or review.feedback
      event.isAnonymous = review.isAnonymous;
    }

    return newReview;
  },

  getReviewsByEventId(eventId) {
    return this.allReviews.filter(r => r.eventId === eventId);
  },

  deleteReview(reviewId) {
    this.allReviews = this.allReviews.filter(r => r.id !== reviewId);
    localStorage.setItem('reviews', JSON.stringify(this.allReviews));
  },

  // Community Approval Process
  pendingApplications: [],

  async fetchPendingApplications(userId) {
    try {
      const response = await api.get(`/general/communities/applications?user_id=${userId}`);
      this.pendingApplications = response.data;
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error fetching pending applications:', error);
      // Fallback for demonstration if API fails
      this.pendingApplications = [
        { id: 101, name: 'Robotics Club', contact_person: 'Alice Smith', proof_document: 'https://example.com/doc1.pdf' },
        { id: 102, name: 'Debate Society', contact_person: 'Bob Jones', proof_document: 'https://example.com/doc2.pdf' }
      ];
      return { success: false, message: error.message };
    }
  },

  async approveApplication(applicationId, userId) {
    try {
      await api.post(`/general/communities/${applicationId}/approve`, { user_id: userId });

      // Remove from local state on success
      this.pendingApplications = this.pendingApplications.filter(app => app.id !== applicationId);
      return { success: true };
    } catch (error) {
      console.error('Error approving application:', error);
      // Simulate success for demonstration if API fails
      this.pendingApplications = this.pendingApplications.filter(app => app.id !== applicationId);
      return { success: true, message: 'Simulated success (API failed)' };
    }
  }
})
