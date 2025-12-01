<template>
  <el-dialog
    v-model="visible"
    title="Give Feedback!"
    width="800px"
    class="rating-dialog"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="true"
    append-to-body
    lock-scroll
    modal
    @close="handleClose"
  >
    <div class="feedback-container">
      <!-- Left Column: Input -->
      <div class="input-column">
        <div class="rating-section">
          <h3 class="rating-title">
            Your rating
            <i class="fas fa-question-circle rating-icon" title="Rate your experience"></i>
          </h3>
          <el-rate 
            v-model="rating" 
            size="large" 
            :colors="['#fcc419', '#fcc419', '#fcc419']" 
          />
        </div>
        
        <div class="thoughts-section">
          <p class="thoughts-question">Do you have any thoughts you'd like to share?</p>
          <textarea
            v-model="feedbackText"
            placeholder="Tell us about your experience..."
            class="feedback-textarea"
            rows="5"
          ></textarea>
          
          <div class="anonymous-option">
            <label class="checkbox-label">
              <input type="checkbox" v-model="isAnonymous" />
              <span class="checkbox-text">Hide my name (Post Anonymously)</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Right Column: Live Preview -->
      <div class="preview-column">
        <h3 class="preview-title">Live Preview</h3>
        <div class="review-card preview-card">
          <div class="review-header">
            <div class="reviewer-info">
              <div class="avatar">{{ previewAvatar }}</div>
              <div>
                <span class="name">{{ previewName }}</span>
                <span class="date">Just now</span>
              </div>
            </div>
            <div class="review-stars">
              <i v-for="n in 5" :key="n" class="fas fa-star" :class="{ filled: n <= rating }"></i>
            </div>
          </div>
          <p class="review-text">{{ feedbackText || 'Your review text will appear here...' }}</p>
        </div>
      </div>
    </div>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button type="primary" @click="submitFeedback" :disabled="rating === 0">
          Submit
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  event: {
    type: Object,
    required: true
  },
  modelValue: {
    type: Boolean,
    default: false
  },
  initialRating: {
    type: Number,
    default: 0
  },
  initialFeedback: {
    type: String,
    default: ''
  },
  initialAnonymous: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'close', 'submit'])

const visible = ref(props.modelValue)
const rating = ref(props.initialRating)
const feedbackText = ref(props.initialFeedback)
const isAnonymous = ref(props.initialAnonymous)

// Computed properties for Live Preview
const previewName = computed(() => {
  return isAnonymous.value ? 'Incognito User' : 'You' // Or fetch real user name if available
})

const previewAvatar = computed(() => {
  return isAnonymous.value ? '?' : 'Y' // Or real user initial
})

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const handleClose = () => {
  emit('close')
}

const submitFeedback = () => {
  if (rating.value > 0) {
    emit('submit', { 
      rating: rating.value, 
      feedback: feedbackText.value,
      isAnonymous: isAnonymous.value
    })
  }
}
</script>

<style>
/* Global styles for the dialog to match user's CSS */
.rating-dialog {
  border-radius: 12px !important;
  overflow: hidden !important;
  margin: 0 auto !important;
  margin-top: 10vh !important;
  width: 800px !important; /* Increased width for split layout */
  max-width: 95vw !important;
  border: 2px dashed #1b8f48 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  background-color: #FDFDEE !important;
  z-index: 9999 !important;
}

.rating-dialog .el-dialog__header {
  background-color: #FDFDEE !important;
  padding: 20px 20px 10px !important;
  border-bottom: 1px solid #dfe9dd;
  position: relative !important;
  margin-right: 0 !important;
}

.rating-dialog .el-dialog__headerbtn {
  background-color: #f08c00 !important;
  border-radius: 4px !important;
  width: 24px !important;
  height: 24px !important;
  top: 20px !important;
  right: 20px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.rating-dialog .el-dialog__close {
  color: #fff !important;
  font-size: 14px !important;
  font-weight: bold !important;
}

.rating-dialog .el-dialog__body {
  background-color: #FDFDEE !important;
  padding: 24px !important; 
  overflow: visible !important;
  min-height: 300px !important;
  height: auto !important;
  display: block !important;
}

.rating-dialog .el-dialog__footer {
  background-color: #FDFDEE !important;
  display: flex !important;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px 20px !important;
  border-top: 1px solid #dfe9dd;
}

/* Button styles */
.rating-dialog .el-button {
  padding: 8px 20px !important;
  border-radius: 6px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
}

.rating-dialog .el-button:not(.el-button--primary) {
  background-color: #f5f5f5 !important;
  border-color: #e0e0e0 !important;
  color: #153226 !important;
}

.rating-dialog .el-button--primary {
  background-color: #1b8f48 !important;
  border-color: #1b8f48 !important;
  color: #fff !important;
}

.rating-dialog .el-button--primary:hover {
  background-color: #167a3d !important;
  border-color: #167a3d !important;
}

.rating-dialog .el-overlay {
  background-color: rgba(234, 246, 232, 0.8) !important;
  backdrop-filter: blur(2px) !important;
}
</style>

<style scoped>
.feedback-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.input-column {
  display: flex;
  flex-direction: column;
}

.preview-column {
  background: #f8fcf9;
  border-radius: 12px;
  padding: 20px;
  border: 1px dashed #d8eadb;
}

.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7c74;
  margin: 0 0 16px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rating-section {
  margin-bottom: 24px;
}

.rating-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #153226;
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 16px;
  font-weight: 500;
}

.rating-icon {
  color: #6b7c74;
  font-size: 14px;
  cursor: help;
}

/* Rating stars custom style */
:deep(.el-rate) {
  display: flex;
  gap: 8px;
  align-items: center;
}

:deep(.el-rate .el-rate__item) {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 6px 8px;
  width: auto;
  height: auto;
  min-width: 36px;
  min-height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-rate .el-rate__item .el-rate__icon) {
  font-size: 20px;
  margin-right: 0;
}

.thoughts-section {
  margin-top: 0;
}

.thoughts-question {
  color: #153226;
  margin-bottom: 12px;
  font-weight: 400;
  font-size: 14px;
}

.feedback-textarea {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  background-color: #fff;
  color: #153226;
  box-sizing: border-box;
  resize: vertical;
  line-height: 1.5;
}

.feedback-textarea:focus {
  outline: none;
  border-color: #1b8f48;
  box-shadow: 0 0 0 2px rgba(27, 143, 72, 0.1);
}

.anonymous-option {
  margin-top: 16px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.checkbox-text {
  font-size: 14px;
  color: #153226;
}

input[type="checkbox"] {
  accent-color: #1b8f48;
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* Review Card Styles (Reused) */
.review-card {
  background: white;
  border: 1px solid #eef2f0;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  background: #e6f3e9;
  color: #1b8f48;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.reviewer-info .name {
  display: block;
  font-weight: 600;
  color: #153226;
}

.reviewer-info .date {
  font-size: 12px;
  color: #9ca3af;
}

.review-stars {
  color: #e5e7eb;
  font-size: 14px;
}

.review-stars .filled {
  color: #fbbf24;
}

.review-text {
  color: #4a5e53;
  line-height: 1.6;
  margin: 0;
  word-break: break-word;
}

@media (max-width: 768px) {
  .feedback-container {
    grid-template-columns: 1fr;
  }
}
</style>
