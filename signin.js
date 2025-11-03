// Değişken adları ve ID'ler güncellendi
const signin_container = document.getElementById("signin_container");
const signin_registerBtn = document.getElementById("signin_register");
const signin_loginBtn = document.getElementById("signin_login");

signin_registerBtn.addEventListener("click", () => {
  // Sınıf adı "signin_active" olarak güncellendi
  signin_container.classList.add("signin_active");
});

signin_loginBtn.addEventListener("click", () => {
  // Sınıf adı "signin_active" olarak güncellendi
  signin_container.classList.remove("signin_active");
});