<template>
  <main class="page-wrap">
    <section class="page-header">
      <h1 class="page-title">Profile Settings</h1>
      <p class="page-subtitle">Update your avatar and change your password.</p>
    </section>

    <section class="settings-grid">

      <!-- AVATAR CARD -->
      <section class="card">
        <h2 class="card-title">Profile Avatar</h2>
        <p class="card-subtitle">Choose your new avatar.</p>

        <div class="current-avatar-wrap">
          <div class="avatar-label">Current avatar</div>
          <div class="current-avatar">
            <img :src="avatarUrl(currentSeed)" alt="Current avatar" />
          </div>
        </div>

        <div class="avatar-grid">
          <button 
            v-for="seed in avatarSeeds" 
            :key="seed"
            class="avatar-option" 
            :class="{ selected: selectedSeed === seed }"
            type="button" 
            @click="selectAvatar(seed)"
          >
            <img :src="avatarUrl(seed)" />
          </button>
        </div>

        <div class="section-actions">
          <button type="button" class="btn-primary" @click="saveAvatar">Save Avatar</button>
        </div>

        <p class="helper-text" :class="avatarMessageClass">{{ avatarMessage }}</p>
      </section>

      <!-- PASSWORD CARD -->
      <section class="card">
        <h2 class="card-title">Change Password</h2>

        <form @submit.prevent="savePassword" class="password-form">
          <div class="form-field">
            <label>Current Password</label>
            <div class="input-with-icon">
              <input :type="showCurrentPass ? 'text' : 'password'" v-model="currentPassword" required />
              <button type="button" class="toggle-visibility" @click="showCurrentPass = !showCurrentPass">
                <i class="fas fa-eye"></i>
              </button>
            </div>
          </div>

          <div class="form-field">
            <label>New Password</label>
            <div class="input-with-icon">
              <input :type="showNewPass ? 'text' : 'password'" v-model="newPassword" required />
              <button type="button" class="toggle-visibility" @click="showNewPass = !showNewPass">
                <i class="fas fa-eye"></i>
              </button>
            </div>
          </div>

          <div class="form-field">
            <label>Confirm Password</label>
            <div class="input-with-icon">
              <input :type="showConfirmPass ? 'text' : 'password'" v-model="confirmPassword" required />
              <button type="button" class="toggle-visibility" @click="showConfirmPass = !showConfirmPass">
                <i class="fas fa-eye"></i>
              </button>
            </div>
          </div>

          <div class="section-actions">
            <button type="submit" class="btn-primary">Save Password</button>
          </div>

          <p class="helper-text error" v-if="passwordError">{{ passwordError }}</p>
          <p class="helper-text success" v-if="passwordSuccess">{{ passwordSuccess }}</p>
        </form>
      </section>

    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'

// ====== AVATAR LOGIC ======
const DICEBEAR_BASE = "https://api.dicebear.com/7.x/notionists/svg?seed="
const avatarSeeds = [
  'circle1', 'circle2', 'circle3', 'circle4', 'circle5', 'circle6',
  'girl1', 'circle8', 'girl3', 'circle10', 'circle11', 'circle12'
]

const currentSeed = ref('circle1')
const selectedSeed = ref('circle1')
const avatarMessage = ref('')
const avatarMessageClass = ref('')

const avatarUrl = (seed) => `${DICEBEAR_BASE}${seed}&flip=false`

const selectAvatar = (seed) => {
  selectedSeed.value = seed
  // Update preview immediately as per original behavior
  currentSeed.value = seed
  avatarMessage.value = "Avatar selected. Press Save to confirm."
  avatarMessageClass.value = ""
}

const saveAvatar = () => {
  // Save full URL to localStorage
  const url = avatarUrl(selectedSeed.value)
  localStorage.setItem('user_avatar', url)
  
  // Dispatch custom event for instant update
  window.dispatchEvent(new Event('avatar-changed'))

  avatarMessage.value = "Avatar saved successfully!"
  avatarMessageClass.value = "success"
}

// ====== PASSWORD LOGIC ======
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const showCurrentPass = ref(false)
const showNewPass = ref(false)
const showConfirmPass = ref(false)

const passwordError = ref('')
const passwordSuccess = ref('')

const savePassword = () => {
  passwordError.value = ""
  passwordSuccess.value = ""

  const newPass = newPassword.value.trim()
  const confirmPass = confirmPassword.value.trim()

  if (newPass !== confirmPass) {
    passwordError.value = "Passwords do not match."
    return
  }

  if (newPass.length < 8) {
    passwordError.value = "Password must be at least 8 characters."
    return
  }

  const hasLetter = /[A-Za-z]/.test(newPass)
  const hasDigit = /\d/.test(newPass)

  if (!hasLetter || !hasDigit) {
    passwordError.value = "Password must contain letters and numbers."
    return
  }

  passwordSuccess.value = "Password saved successfully."
  
  // Reset fields
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
}
</script>

<style scoped>
/* Design Tokens */
.page-wrap {
  --brand: #1b8f48;
  --brand-600: #167a3d;
  --brand-200: #e6f3e9;
  --page: #fefbea;
  --card: #ffffff;
  --ink: #153226;
  --muted: #6b7c74;
  --outline: #d8eadb;
  --error: #d94848;
  --success: #2b8a3e;
  --shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
}

.page-wrap {
  max-width: 1180px;
  margin: 18px auto 56px;
  padding: 0 20px 40px;
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  color: var(--ink);
}

.page-header {
  margin-bottom: 18px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
}

.page-subtitle {
  font-size: 13px;
  color: var(--muted);
  margin-top: 4px;
}

/* GRID */
.settings-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 18px;
}

.card {
  background: var(--card);
  border-radius: 18px;
  box-shadow: var(--shadow);
  padding: 18px 18px 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.card-subtitle {
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 14px;
}

/* AVATAR SECTION */
.current-avatar-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar-label {
  font-size: 12px;
  color: var(--muted);
}

.current-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid var(--brand);
  background-color: #f7fbf8;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.current-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* avatar grid */
.avatar-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin: 10px 0 12px;
}

.avatar-option {
  border-radius: 999px;
  border: 2px solid transparent;
  padding: 0;
  width: 52px;
  height: 52px;
  background-color: #f7fbf8;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-option img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-option.selected {
  border-color: var(--brand);
  background-color: #f0f8f1;
}

/* BUTTONS / TEXT */
.section-actions {
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  border-radius: 6px;
  border: none;
  background: var(--brand);
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 18px;
  cursor: pointer;
}

.helper-text {
  margin-top: 4px;
  font-size: 12px;
  color: var(--muted);
}

.helper-text.error {
  color: var(--error);
}

.helper-text.success {
  color: var(--success);
}

/* PASSWORD FORM */
.password-form {
  margin-top: 6px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 10px;
}

.form-field label {
  font-size: 12px;
  color: #777f7a;
}

.input-with-icon {
  position: relative;
}

.password-form input[type="password"],
.password-form input[type="text"] {
  border-radius: 6px;
  border: 1px solid #dadfd4;
  padding: 7px 34px 7px 9px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  background: #ffffff;
  width: 100%;
}

.password-form input:focus {
  border-color: var(--brand);
}

.toggle-visibility {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
}

.toggle-visibility i {
  font-size: 14px;
  color: #8b9390;
}

/* RESPONSIVE */
@media (max-width: 960px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .page-wrap {
    margin: 18px auto 32px;
    padding: 0 14px 30px;
  }

  .avatar-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
