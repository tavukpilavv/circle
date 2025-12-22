<template>
  <div class="login-page">
    <main>
        
        <div class="signin-container">
            
            <div class="signin-box">
                  <!-- No close icon needed for this page, or redirect to login -->
                  <svg class="close-icon" width="47" height="47" viewBox="0 0 47 47" fill="none" xmlns="http://www.w3.org/2000/svg" @click="$router.push('/login')">
                  <path d="M18.6042 18.604L28.3959 28.3957" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M28.3959 18.604L18.6042 28.3957" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M33.2917 5.875H13.7083C9.3821 5.875 5.875 9.3821 5.875 13.7083V33.2917C5.875 37.6179 9.3821 41.125 13.7083 41.125H33.2917C37.6179 41.125 41.125 37.6179 41.125 33.2917V13.7083C41.125 9.3821 37.6179 5.875 33.2917 5.875Z" stroke="var(--Accents-Orange, #FF8D28)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                
                <h2 class="title" style="font-size: 32px;">RESET PASSWORD</h2> 
                
                <p class="description">
                    Create a new password for your account.
                </p>
                
                <form id="reset-form" @submit.prevent="handleResetConfirm">
                    
                    <div class="input-group password-group">
                        <input :type="showPassword ? 'text' : 'password'" placeholder="New Password" v-model="password" required minlength="6">
                        <button type="button" class="password-toggle-btn" @click="showPassword = !showPassword">
                            <i class="fas" :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
                        </button>
                    </div>

                    <div class="input-group password-group">
                        <input :type="showConfirmPassword ? 'text' : 'password'" placeholder="Confirm New Password" v-model="confirmPassword" required minlength="6">
                        <button type="button" class="password-toggle-btn" @click="showConfirmPassword = !showConfirmPassword">
                            <i class="fas" :class="showConfirmPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
                        </button>
                    </div>

                    <button type="submit" class="signin-button" :disabled="isSubmitting">
                        {{ isSubmitting ? 'Updating...' : 'Update Password' }}
                    </button>

                    <div class="back-link">
                        <router-link to="/login">Back to Sign In</router-link>
                    </div>
                </form>
            </div>
        </div>
        
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiFetch } from '../api'

const router = useRouter()
const route = useRoute()

const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isSubmitting = ref(false)
const token = ref('')

onMounted(() => {
    // Get token from URL query params
    token.value = route.query.token || '';
    if (!token.value) {
        alert("Invalid or missing reset token.");
        router.push('/login');
    }
})

const handleResetConfirm = async () => {
  if (password.value !== confirmPassword.value) {
      alert("Passwords do not match!");
      return;
  }
  
  if (!token.value) {
      alert("Missing reset token.");
      return;
  }

  isSubmitting.value = true;

  try {
    // Send request to Backend
    const response = await apiFetch('/api/auth/reset-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        token: token.value,
        new_password: password.value
      })
    });

    const data = await response.json();

    if (response.ok) {
        alert('Password has been successfully reset! Please login with your new password.');
        router.push('/login');
    } else {
        alert(data.error || 'Failed to reset password. Link may be expired.');
    }
  } catch (error) {
    console.error('Reset password error:', error);
    alert('Unable to connect to the server.');
  } finally {
      isSubmitting.value = false;
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.login-page {
    --color-bg-main: #f0f7f0;
    --color-text-dark: #000000;
    --color-text-link: #FF9E4A;
    --color-green-dark: #1A916D;
    
    font-family: 'Roboto', sans-serif;
    color: #333;
    min-height: 100vh;
}

main {
    padding-top: 40px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.signin-container {
    flex-grow: 1;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 80px 20px 20px;
    width: 100%;
}

.signin-box {
    background-color: #E3F6DB;
    border-radius: 15px;
    padding: 40px 50px;
    width: 100%;
    max-width: 740px;
    min-height: 500px;
    
    text-align: center;
    position: relative;
    border: 2px dashed #1A916D;
    box-sizing: border-box;
}

.close-icon {
    position: absolute;
    top: 15px;
    right: 20px;
    width: 47px;
    height: 47px;
    cursor: pointer;
    opacity: 0.7;
    transition: opacity 0.2s, transform 0.2s;
    color: var(--color-green-dark);
}

.title {
    color: #16A34A;     
    font-size: 36px;   
    font-weight: 800;  
    margin-bottom: 20px; 
    font-family: 'Roboto', sans-serif;
}

.description {
    color: #555;
    font-size: 16px;
    margin-bottom: 30px;
    line-height: 1.5;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}

.input-group {
    margin-bottom: 20px;
    width: 100%;
    /* display: flex; center not needed for password-group relative */
}

.input-group input {
    width: 100%;
    max-width: 642px;
    height : 69px;
    padding: 15px 20px;
    border: 1px solid #FFFFFF;
    border-radius: 8px;
    font-size: 15px;
    outline: none;
    transition: border-color 0.3s;
    box-sizing: border-box;
}

.input-group input:focus {
    border-color: var(--color-green-dark);
}

.password-group {
    position: relative;
    max-width: 642px;
    margin: 0 auto 20px;
}

.password-toggle-btn {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 20px;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.signin-button {
    width: 100%;
    max-width: 637px;
    height: 76.18px;
    background-color: #1A916D;
    border-radius: 16px;
    font-size: 24px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    color: white;
    border: none;
    cursor: pointer;
    margin: 10px auto 0;
    transition: background-color 0.3s;
}

.signin-button:hover:not(:disabled) {
    background-color:#157a5c;
}

.signin-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.back-link {
    margin-top: 25px;
    font-size: 16px;
}

.back-link a {
    color: #FF9E4A;
    font-weight: 700;
    text-decoration: underline;
}

@media (max-width: 768px) {
    .signin-box {
        padding: 30px 20px;
        min-height: auto;
    }

    .title {
        font-size: 26px !important;
    }

    .input-group input {
        height: 55px;
        font-size: 14px;
    }

    .signin-button {
        height: 60px;
        font-size: 20px;
    }
}
</style>
