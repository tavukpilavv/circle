<template>
    <div class="page-wrap">
      <section class="club-card">
        <!-- LEFT SIDE: TEXT -->
        <div>
          <h1 class="club-left-title">Add your club to CirCle.</h1>
          <p class="club-left-sub">
            Are you running a student club or community and want your events to appear on CirCle?
            Fill out this form and send us your details. We’ll review your application and,
            once approved, your club will be visible to students on the platform.
          </p>

          <ul class="check-list">
            <li>
              <span class="check-icon"><i class="fas fa-check"></i></span>
              Reach more students who are actively looking for events.
            </li>
            <li>
              <span class="check-icon"><i class="fas fa-check"></i></span>
              Keep all your club’s activities in one clear place.
            </li>
            <li>
              <span class="check-icon"><i class="fas fa-check"></i></span>
              Make it easier for new members to discover and join you.
            </li>
          </ul>

          <div class="info-pill">
            <i class="far fa-question-circle"></i>
            Applications are reviewed manually before going live.
          </div>
        </div>

        <!-- RIGHT SIDE: FORM -->
        <div class="club-form-card">
          <form @submit.prevent="handleSubmit" novalidate>
            <div class="section-label">Club information</div>
            <div class="section-divider"></div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label" for="clubName">
                  Club / community name <span>*</span>
                </label>
                <input
                  id="clubName"
                  v-model="form.clubName"
                  class="form-input"
                  required
                />
                <div v-if="errors.clubName" class="form-error-inline">
                  {{ errors.clubName }}
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="university">University <span>*</span></label>
                <select id="university" v-model="form.university" class="form-select" required>
                  <option value="">Select university</option>
                  <option value="Ostim Technical University">OSTIM Technical University</option>
                  <option value="Other">Other</option>
                </select>
                <div v-if="errors.university" class="form-error-inline">
                  {{ errors.university }}
                </div>
              </div>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label" for="clubType">
                  Club type <span>*</span>
                </label>
                <select id="clubType" v-model="form.clubType" class="form-select" required>
                  <option value="">Select type</option>
                  <option value="official">Official university club</option>
                  <option value="community">Student community / interest group</option>
                </select>
                <div v-if="errors.clubType" class="form-error-inline">
                  {{ errors.clubType }}
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="category">
                  Category <span>*</span>
                </label>
                <select id="category" v-model="form.category" class="form-select" required>
                  <option value="">Select category</option>
                  <option value="Academic">Academic</option>
                  <option value="Technology">Technology</option>
                  <option value="Culture & Arts">Culture &amp; Arts</option>
                  <option value="Sports">Sports</option>
                  <option value="Social">Social</option>
                  <option value="Others">Others</option>
                </select>
                <div v-if="errors.category" class="form-error-inline">
                  {{ errors.category }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="description">
                Short description <span>*</span>
              </label>
              <textarea
                id="description"
                v-model="form.description"
                class="form-textarea"
                placeholder="Tell us briefly what your club is about and who it is for."
                required
              ></textarea>
              <div v-if="errors.description" class="form-error-inline">
                {{ errors.description }}
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="events">
                What kind of events do you organize?
              </label>
              <textarea
                id="events"
                v-model="form.events"
                class="form-textarea"
                placeholder="Example: weekly meetups, workshops, competitions, trips, online sessions..."
              ></textarea>
            </div>

            <div class="section-label" style="margin-top: 8px;">Contact</div>
            <div class="section-divider"></div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label" for="contactName">
                  Contact person name <span>*</span>
                </label>
                <input
                  id="contactName"
                  v-model="form.contactName"
                  class="form-input"
                  required
                />
                <div v-if="errors.contactName" class="form-error-inline">
                  {{ errors.contactName }}
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="studentNumber">
                  Student number (optional)
                </label>
                <input
                  id="studentNumber"
                  v-model="form.studentNumber"
                  class="form-input"
                  placeholder="If you are from OSTIM, you can add it."
                />
              </div>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label" for="email">
                  Contact email <span>*</span>
                </label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  class="form-input"
                  required
                />
                <div v-if="errors.email" class="form-error-inline">
                  {{ errors.email }}
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="instagram">
                  Instagram (optional)
                </label>
                <input
                  id="instagram"
                  v-model="form.instagram"
                  class="form-input"
                  placeholder="https://instagram.com/yourclub"
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="otherLink">
                Other link (optional)
              </label>
              <input
                id="otherLink"
                v-model="form.otherLink"
                class="form-input"
                placeholder="Website, Telegram, WhatsApp, Discord..."
              />
            </div>

            <div class="section-label" style="margin-top: 8px;">Verification</div>
            <div class="section-divider"></div>

            <div class="form-group">
              <label class="form-label" for="proof">
                Proof of club (optional for now)
              </label>
              <input
                id="proof"
                type="file"
                class="form-file"
                accept=".png,.jpg,.jpeg,.pdf"
                @change="handleFileChange"
              />
              <p class="form-small">
                For official clubs, you can upload a document or screenshot that shows the club is recognized by the university.
              </p>
            </div>

            <div class="form-footer-row">
              <label class="checkbox-row">
                <input type="checkbox" v-model="form.confirm" required />
                <span>
                  I confirm that I am an official representative of this club /
                  community and the information is correct.
                </span>
              </label>

              <button type="submit" class="btn-primary">
                Submit application
                <i class="fas fa-paper-plane"></i>
              </button>
            </div>

            <div v-if="showSuccess" class="form-success">
              <i class="far fa-check-circle"></i>
              Your application was sent. We’ll review it as soon as possible 💚
            </div>
          </form>
        </div>
      </section>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const form = reactive({
  clubName: '',
  university: '',
  clubType: '',
  category: '',
  description: '',
  events: '',
  contactName: '',
  studentNumber: '',
  email: '',
  instagram: '',
  otherLink: '',
  proof: null,
  confirm: false
})

const errors = reactive({})
const showSuccess = ref(false)

const handleFileChange = (event) => {
  form.proof = event.target.files[0]
}

const validate = () => {
  Object.keys(errors).forEach(key => delete errors[key])
  let isValid = true

  if (!form.clubName.trim()) {
    errors.clubName = "This field is required."
    isValid = false
  }
  if (!form.university) {
    errors.university = "Please select a university."
    isValid = false
  }
  if (!form.clubType) {
    errors.clubType = "Please choose a type."
    isValid = false
  }
  if (!form.category) {
    errors.category = "Please select a category."
    isValid = false
  }
  if (!form.description.trim()) {
    errors.description = "Please add a short description."
    isValid = false
  }
  if (!form.contactName.trim()) {
    errors.contactName = "Please enter a contact name."
    isValid = false
  }
  if (!form.email.trim() || !/^\S+@\S+\.\S+$/.test(form.email.trim())) {
    errors.email = "Please enter a valid email."
    isValid = false
  }
  if (!form.confirm) {
    alert("Please confirm that you are a representative of the club.")
    isValid = false
  }

  return isValid
}

const handleSubmit = () => {
  if (!validate()) return

  // Simulate API call
  console.log("Submitting application:", form)
  
  // Reset form
  Object.keys(form).forEach(key => {
    if (key === 'confirm') form[key] = false
    else if (key === 'proof') form[key] = null
    else form[key] = ''
  })
  
  // Reset file input manually if needed
  const fileInput = document.getElementById('proof')
  if (fileInput) fileInput.value = ''

  showSuccess.value = true
  setTimeout(() => {
    showSuccess.value = false
  }, 4000)
}
</script>

<style scoped>
/* Scoped styles ported from apply.html */
:root {
  --brand: #1b8f48;
  --brand-600: #167a3d;
  --brand-200: #e6f3e9;

  --page: #fefbea;
  --card: #ffffff;

  --ink: #153226;
  --muted: #6b7c74;
  --outline: #d8eadb;

  --shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
  --danger: #e55353;
}

.page-wrap {
  max-width: 1180px;
  margin: 24px auto 56px;
  padding: 0 20px 40px;
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}

.club-card {
  border-radius: 28px;
  background: linear-gradient(135deg, #e6f6e6, #ffe7d8);
  padding: 26px 26px 24px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1.5fr);
  gap: 24px;
  align-items: flex-start;
}

.club-left-title {
  font-size: 26px;
  font-weight: 800;
  color: #163828;
  margin-bottom: 8px;
}

.club-left-sub {
  font-size: 13px;
  color: #385445;
  margin-bottom: 16px;
  line-height: 1.6;
}

.check-list {
  list-style: none;
  display: grid;
  gap: 8px;
  margin-bottom: 16px;
  padding-left: 0;
}

.check-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #234135;
}

.check-icon {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: #ffffffc8;
  border: 1px solid #cfe5d5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #167a3d;
  flex-shrink: 0;
}

.info-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #ffffffd0;
  font-size: 11px;
  color: #6b7c74;
}

.info-pill i {
  font-size: 12px;
  color: #167a3d;
}

.club-form-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
}

.section-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #4b6657;
  margin-bottom: 6px;
}

.section-divider {
  height: 1px;
  background: #edf3ee;
  margin-bottom: 10px;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.form-group {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-label {
  font-size: 12px;
  font-weight: 600;
  color: #234135;
}

.form-label span {
  color: #e55353;
}

.form-input,
.form-select,
.form-textarea,
.form-file {
  border-radius: 10px;
  border: 1px solid #d8eadb;
  padding: 8px 10px;
  font-size: 13px;
  background: #fdfdf9;
  outline: none;
  width: 100%;
}

.form-select {
  cursor: pointer;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-small {
  font-size: 11px;
  color: #6b7c74;
}

.form-footer-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  justify-content: space-between;
  margin-top: 8px;
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #385445;
}

.checkbox-row input {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  border: 1px solid #d8eadb;
}

.btn-primary {
  border: none;
  border-radius: 999px;
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 600;
  background: #1b8f48;
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.btn-primary i {
  font-size: 13px;
}

.btn-primary:active {
  transform: translateY(1px);
  filter: brightness(0.96);
}

.form-success {
  margin-top: 8px;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  color: #145c32;
  background-color: #e0f5e5;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.form-success i {
  font-size: 13px;
}

.form-error-inline {
  font-size: 11px;
  color: #e55353;
}

@media (max-width: 960px) {
  .club-card {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .page-wrap {
    padding: 0 14px 32px;
  }

  .club-card {
    padding: 20px 16px 18px;
    border-radius: 22px;
  }

  .club-left-title {
    font-size: 22px;
  }

  .form-grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
