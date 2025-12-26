import { createApp } from 'vue'
import { inject } from '@vercel/analytics'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import '../style.css' // Import global styles
import './assets/main.css' // Import custom Element Plus overrides
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

// Initialize Vercel Analytics
inject()

/* ======================
   PRELOAD DATA BEFORE APP MOUNTS
   ====================== */
async function preload() {
  try {
    await store.loadCommunitiesFromBackend();
    if (store.loadEvents) {
      await store.loadEvents();        // ✅ This prevents carousel disappearing
    }
  } catch (err) {
    console.error("Preload failed:", err);
  }
}

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
app.use(ElementPlus)

const options = {
    transition: "Vue-Toastification__bounce",
    maxToasts: 20,
    newestOnTop: true,
    position: "top-center",
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: false,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: "button",
    icon: true,
    rtl: false
};

app.use(Toast, options);

app.mount('#app')
