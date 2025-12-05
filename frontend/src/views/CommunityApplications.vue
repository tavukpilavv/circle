<template>
  <div class="community-applications">
    <div class="header">
      <h1>Community Applications</h1>
      <p>Manage pending community creation requests.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="applications.length === 0" class="empty-state">
      <el-empty description="No pending applications found" />
    </div>

    <div v-else class="applications-list">
      <el-card v-for="app in applications" :key="app.id" class="application-card" shadow="hover">
        <div class="card-content">
          <div class="info-section">
            <h3>{{ app.name }}</h3>
            <p class="contact"><strong>Contact Person:</strong> {{ app.contact_person }}</p>
            <a :href="app.proof_document" target="_blank" class="document-link">
              <el-icon><Document /></el-icon> View Proof Document
            </a>
          </div>
          <div class="actions-section">
            <el-button type="success" @click="approveApp(app.id)" :loading="approvingId === app.id">
              Approve
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { store } from '../store.js'
import { ElMessage } from 'element-plus'
import { Document } from '@element-plus/icons-vue'

const loading = ref(true)
const approvingId = ref(null)

// Get current user ID (mocked for now as 1 if not in localStorage)
const currentUserId = localStorage.getItem('user_id') || 1

const applications = computed(() => store.pendingApplications)

const fetchApplications = async () => {
  loading.value = true
  await store.fetchPendingApplications(currentUserId)
  loading.value = false
}

const approveApp = async (id) => {
  approvingId.value = id
  const result = await store.approveApplication(id, currentUserId)
  
  if (result.success) {
    ElMessage.success('Application approved successfully')
  } else {
    ElMessage.error('Failed to approve application: ' + (result.message || 'Unknown error'))
  }
  approvingId.value = null
}

onMounted(() => {
  fetchApplications()
})
</script>

<style scoped>
.community-applications {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  margin-bottom: 30px;
  text-align: center;
}

.header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.header p {
  color: #666;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.application-card {
  border-radius: 12px;
  transition: transform 0.2s;
}

.application-card:hover {
  transform: translateY(-2px);
}

.card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.info-section h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.contact {
  margin: 0 0 10px 0;
  color: #606266;
}

.document-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}

.document-link:hover {
  text-decoration: underline;
}

.actions-section {
  margin-left: 20px;
}

@media (max-width: 600px) {
  .card-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .actions-section {
    margin-left: 0;
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
