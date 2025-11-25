document.addEventListener("DOMContentLoaded", () => {
  // ====== AVATAR LOGIC ======
  const avatarOptions = document.querySelectorAll(".avatar-option");
  const currentAvatarImg = document.getElementById("currentAvatarImg");
  const navbarProfileIcon = document.getElementById("navbarProfileIcon");
  const selectedAvatarInput = document.getElementById("selectedAvatarInput");
  const avatarForm = document.getElementById("avatarForm");
  const avatarMessage = document.getElementById("avatarMessage");

  const DICEBEAR_BASE =
    "https://api.dicebear.com/7.x/notionists/svg?seed=";

  function avatarUrl(seed) {
    return `${DICEBEAR_BASE}${seed}&flip=false`;
  }

  // When the user selects an avatar (preview only)
  avatarOptions.forEach((btn) => {
    btn.addEventListener("click", () => {
      const seed = btn.getAttribute("data-avatar-seed");
      if (!seed) return;

      // Remove old selected
      avatarOptions.forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");

      // Update preview avatar only
      currentAvatarImg.src = avatarUrl(seed);

      // Update hidden input so saving works
      selectedAvatarInput.value = seed;

      // Message
      if (avatarMessage) {
        avatarMessage.textContent = "Avatar selected. Press Save to confirm.";
        avatarMessage.classList.remove("error");
        avatarMessage.classList.remove("success");
      }
    });
  });

  // When user presses Save Avatar (THIS updates navbar icon)
  avatarForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const seed = selectedAvatarInput.value;
    const url = avatarUrl(seed);

    // Update preview (already updated but we ensure consistency)
    currentAvatarImg.src = url;

    // Update NAVBAR only after saving (your requirement)
    if (navbarProfileIcon) {
      navbarProfileIcon.src = url;
    }

    // Success message
    avatarMessage.textContent = "Avatar saved successfully!";
    avatarMessage.classList.add("success");
  });

  // ====== PASSWORD LOGIC ======
  const passwordForm = document.getElementById("passwordForm");
  const currentPassword = document.getElementById("currentPassword");
  const newPassword = document.getElementById("newPassword");
  const confirmPassword = document.getElementById("confirmPassword");
  const passwordError = document.getElementById("passwordError");
  const passwordSuccess = document.getElementById("passwordSuccess");

  // Toggle password visibility
  const toggleBtns = document.querySelectorAll(".toggle-visibility");
  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.target;
      const input = document.getElementById(targetId);
      if (!input) return;

      input.type = input.type === "password" ? "text" : "password";
    });
  });

  // Simple password validation
  passwordForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const newPass = newPassword.value.trim();
    const confirmPass = confirmPassword.value.trim();

    passwordError.textContent = "";
    passwordSuccess.textContent = "";

    if (newPass !== confirmPass) {
      passwordError.textContent = "Passwords do not match.";
      return;
    }

    if (newPass.length < 8) {
      passwordError.textContent = "Password must be at least 8 characters.";
      return;
    }

    const hasLetter = /[A-Za-z]/.test(newPass);
    const hasDigit = /\d/.test(newPass);

    if (!hasLetter || !hasDigit) {
      passwordError.textContent =
        "Password must contain letters and numbers.";
      return;
    }

    passwordSuccess.textContent = "Password saved successfully.";
  });
});
