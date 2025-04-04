document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const loginButton = document.getElementById("showLogin");
    const registerButton = document.getElementById("showRegister");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const passwordError = document.getElementById("passwordError");
  
    // Toggle to Login
    loginButton.addEventListener("click", function () {
        loginForm.classList.remove("hidden");
        registerForm.classList.add("hidden");
        loginButton.classList.add("active");
        registerButton.classList.remove("active");
    });
  
    // Toggle to Register
    registerButton.addEventListener("click", function () {
        registerForm.classList.remove("hidden");
        loginForm.classList.add("hidden");
        registerButton.classList.add("active");
        loginButton.classList.remove("active");
    });
  
    // Password Validation on Register
    registerForm.addEventListener("submit", function (e) {
        if (password.value !== confirmPassword.value) {
            e.preventDefault(); // Prevent form submission
            passwordError.textContent = "Passwords do not match!";
            passwordError.style.color = "red";
        } else {
            passwordError.textContent = "";
        }
    });
  });
  