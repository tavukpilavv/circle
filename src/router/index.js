import { createRouter, createWebHashHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import HomeView from '../views/HomeView.vue'
import CommunitiesView from '../views/CommunitiesView.vue'
import LoginView from '../views/LoginView.vue'
import EventsView from '../views/EventsView.vue'
import ProfileView from '../views/ProfileView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView
    },
    {
        path: '/communities',
        name: 'Communities',
        component: CommunitiesView
    },
    {
        path: '/events',
        name: 'Events',
        component: EventsView
    },
    {
        path: '/events/:id',
        name: 'EventDetails',
        component: () => import('../views/EventDetailsView.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView
    },
    {
        path: '/signup',
        name: 'Signup',
        component: () => import('../views/SignupView.vue')
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfileView
    },
    {
        path: '/settings',
        name: 'Settings',
        component: SettingsView
    },
    {
        path: '/help',
        name: 'Help',
        component: () => import('../views/ContactView.vue')
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('../views/AboutView.vue')
    },
    {
        path: '/apply',
        name: 'Apply',
        component: () => import('../views/ApplyView.vue')
    },
    {
        path: '/community-applications',
        name: 'CommunityApplications',
        component: () => import('../views/CommunityApplications.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        // always scroll to top
        return { top: 0 }
    }
})

export default router
