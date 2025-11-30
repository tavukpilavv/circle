import { reactive } from 'vue'

export const store = reactive({
  communities: [
    {
      id: 1,
      name: 'BİLTEK – AYBU Science and Technology Community',
      description: 'Focused on innovation, coding workshops, and technology projects.',
      members: 450,
      joined: false,
      image: 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 2,
      name: 'ASEC AYBU',
      description: 'Cybersecurity, software development, and game development community.',
      members: 320,
      joined: false,
      image: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 3,
      name: 'Psychology Community',
      description: 'Mental health awareness, psychology seminars, and student gatherings.',
      members: 285,
      joined: false,
      image: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 4,
      name: 'AYBU Aviation and Space Club (AYBUHUK)',
      description: 'Designing rockets, drones, and exploring aerospace engineering.',
      members: 410,
      joined: false,
      image: 'https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 5,
      name: 'AYBU Music Community',
      description: 'Live concerts, instrument workshops, and bringing rhythm to campus.',
      members: 560,
      joined: false,
      image: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 6,
      name: 'AYBU Theater Club',
      description: 'Performing arts, acting classes, and stage plays.',
      members: 230,
      joined: false,
      image: 'https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?auto=format&fit=crop&w=800&q=80'
    }
  ],
  events: [
    {
      id: 1,
      image: new URL('../images/image1.jpg', import.meta.url).href,
      alt: "Ceramic Painting Workshop Poster",
      name: "Ceramic Painting Workshop",
      community_name: "BİLTEK – AYBU Science and Technology Community",
      organizer: "AYBU",
      location: "Cleopatra Ayrancı Atelier",
      time: "14:00",
      date: "2025-11-01",
      time: "14:00",
      date: "2025-11-01",
      registered: false,
      rating: 4.8,
      ratingCount: 124
    },
    {
      id: 2,
      image: new URL('../images/image2.jpg', import.meta.url).href,
      alt: "Game Jam 2025 Poster",
      name: "Game Jam 2025",
      community_name: "ASEC AYBU",
      organizer: "AYBU",
      location: "AYBU Campus",
      time: "TBA",
      date: "2025-11-07",
      time: "TBA",
      date: "2025-11-07",
      registered: false,
      rating: 4.5,
      ratingCount: 89
    },
    {
      id: 3,
      image: new URL('../images/image3.jpg', import.meta.url).href,
      alt: "Psychological First Aid Poster",
      name: "Psychological First Aid",
      community_name: "Psychology Community",
      organizer: "Hacettepe",
      location: "Coffee Up Beşevler",
      time: "12:00",
      date: "2025-11-29",
      time: "12:00",
      date: "2025-11-29",
      registered: false,
      rating: 4.9,
      ratingCount: 56
    },
    {
      id: 4,
      image: new URL('../images/image5.jpg', import.meta.url).href,
      alt: "MAN Türkiye R&D and Career Panel Poster",
      name: "MAN Türkiye R&D & Career Panel",
      community_name: "AYBU Aviation and Space Club (AYBUHUK)",
      organizer: "AYBU",
      location: "A-212",
      time: "11:00",
      date: "2025-11-06",
      time: "11:00",
      date: "2025-11-06",
      registered: false,
      rating: 4.2,
      ratingCount: 34
    },
    {
      id: 5,
      image: new URL('../images/image6.jpg', import.meta.url).href,
      alt: "Stage is Yours Poster",
      name: "Stage is Yours!",
      community_name: "AYBU Music Community",
      organizer: "Bilkent",
      location: "AYBU – Online Video Submission",
      time: "TBA",
      date: "2025-11-02",
      time: "TBA",
      date: "2025-11-02",
      registered: false,
      rating: 4.7,
      ratingCount: 210
    },
    {
      id: 6,
      image: new URL('../images/image4.jpg', import.meta.url).href,
      alt: "Theatre Club Coffee Meetup Poster",
      name: "Coffee Meetup",
      community_name: "AYBU Theater Club",
      organizer: "ODTÜ",
      location: "Coffee Up, Bahçelievler – Azerbaijan St. No:23",
      time: "14:00",
      date: "2025-10-12",
      time: "14:00",
      date: "2025-10-12",
      registered: true,
      rating: 4.6,
      ratingCount: 45
    },
    {
      id: 7,
      image: new URL('../images/image7.jpg', import.meta.url).href,
      alt: "MS Office Computer Course Poster",
      name: "MS Office Course",
      community_name: "Strategic Management Club",
      organizer: "Gazi Üni",
      location: "Etlik Milli İrade Campus",
      time: "10:00-12:00",
      date: "2025-12-05",
      time: "10:00-12:00",
      date: "2025-12-05",
      registered: false,
      rating: 4.3,
      ratingCount: 12
    },
    {
      id: 8,
      image: new URL('../images/image8.jpg', import.meta.url).href,
      alt: "Bariatric Surgery Dietetics Seminar Poster",
      name: "Bariatric Surgery Dietetics",
      community_name: "AYBU SAYBEK",
      organizer: "AYBU",
      location: "Esenboğa Campus – A Block Conference Hall",
      time: "12:30-13:30",
      date: "2025-11-24",
      time: "12:30-13:30",
      date: "2025-11-24",
      registered: false,
      rating: 4.8,
      ratingCount: 67
    },
    {
      id: 9,
      image: new URL('../images/image9.jpg', import.meta.url).href,
      alt: "Art Workshop Poster",
      name: "Art Workshop",
      community_name: "AYBU Art Community",
      organizer: "Bilkent",
      location: "Coffee & Tea Shop Cafe",
      time: "14:00-17:00",
      date: "2025-11-29",
      time: "14:00-17:00",
      date: "2025-11-29",
      registered: false,
      rating: 4.9,
      ratingCount: 156
    },
    {
      id: 10,
      image: new URL('../images/image10.jpg', import.meta.url).href,
      alt: "ÜNİDES Project Announcement Poster",
      name: "ÜNİDES – Growing Together",
      community_name: "Gençlik ve Spor Bakanlığı Project",
      organizer: "ODTÜ",
      location: "AYBU – Application Link in Bio",
      time: "TBA",
      date: "2025-11-15",
      time: "TBA",
      date: "2025-11-15",
      registered: false,
      rating: 4.4,
      ratingCount: 28
    },
    {
      id: 11,
      image: new URL('../images/image11.jpg', import.meta.url).href,
      alt: "TBMM Visit Poster",
      name: "TBMM Visit – Youth in Politics",
      community_name: "İstiklal Club",
      organizer: "Hacettepe",
      location: "Grand National Assembly of Türkiye",
      time: "16:00",
      date: "2025-11-18",
      time: "16:00",
      date: "2025-11-18",
      registered: false,
      rating: 4.7,
      ratingCount: 92
    },
    {
      id: 12,
      image: new URL('../images/image12.jpg', import.meta.url).href,
      alt: "Mete Gazoz Talk Poster",
      name: "Mete Gazoz – Olympic Champion Talk",
      community_name: "AYBU",
      organizer: "AYBU",
      location: "Milli İrade Campus – Conference Hall",
      time: "14:00",
      date: "2025-12-02",
      time: "14:00",
      date: "2025-12-02",
      registered: false,
      rating: 5.0,
      ratingCount: 312
    }
  ],
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
  }
})
