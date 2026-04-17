<template>
  <div class="verify-page">
    <div class="verify-box">
      <h2>Email Verification</h2>
      <p v-if="loading">Verifying your email...</p>
      <p v-else-if="success" class="success">✅ {{ message }}</p>
      <p v-else class="error">❌ {{ message }}</p>
      <button v-if="!loading" @click="$router.push('/login')">Go to Login</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../api'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const success = ref(false)
const message = ref('')

onMounted(async () => {
  const token = route.query.token

  if (!token) {
    loading.value = false
    message.value = 'Invalid verification link.'
    return
  }

  try {
    const response = await apiFetch('/api/auth/verify-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token })
    })

    const data = await response.json()

    if (response.ok) {
      success.value = true
      message.value = data.message || 'Email verified successfully! You can now log in.'
    } else {
      message.value = data.error || 'Verification failed. Link may be expired.'
    }
  } catch (error) {
    message.value = 'Unable to connect to the server.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f7f0;
}

.verify-box {
  background-color: #E3F6DB;
  border: 2px dashed #1A916D;
  border-radius: 15px;
  padding: 50px;
  text-align: center;
  max-width: 500px;
  width: 100%;
}

h2 {
  color: #16A34A;
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  margin-bottom: 30px;
}

.success { color: #1A916D; }
.error { color: #e53e3e; }

button {
  background-color: #1A916D;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 15px 40px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
}

button:hover { background-color: #157a5c; }
</style>