const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const phoneInput = document.getElementById("phone");
const passwordInput = document.getElementById("password");
const confirmInput = document.getElementById("confirm_password");

const nameError = document.getElementById("name_error");
const emailError = document.getElementById("email_error");
const phoneError = document.getElementById("phone_error");
const passwordError = document.getElementById("password_error");
const confirmError = document.getElementById("confirm_error");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const phoneRegex = /^[0-9]{10}$/;
const passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*]).{5,}$/;

function validateName() {
  if (nameInput.value.trim() !== "") {
    nameInput.style.borderBottom = "2px solid #28a745";
    nameError.textContent = "";
    return true;
  } else {
    nameInput.style.borderBottom = "2px solid #dc3545";
    nameError.textContent = "Name is required";
    return false;
  }
}

function validateEmail() {
  if (emailRegex.test(emailInput.value)) {
    emailInput.style.borderBottom = "2px solid #28a745";
    emailError.textContent = "";
    return true;
  } else {
    emailInput.style.borderBottom = "2px solid #dc3545";
    emailError.textContent = "Invalid email format";
    return false;
  }
}

function validatePhone() {
  if (phoneRegex.test(phoneInput.value)) {
    phoneInput.style.borderBottom = "2px solid #28a745";
    phoneError.textContent = "";
    return true;
  } else {
    phoneInput.style.borderBottom = "2px solid #dc3545";
    phoneError.textContent = "Enter valid 10-digit number";
    return false;
  }
}

function validatePassword() {
  if (passwordRegex.test(passwordInput.value)) {
    passwordInput.style.borderBottom = "2px solid #28a745";
    passwordError.textContent = "";
    return true;
  } else {
    passwordInput.style.borderBottom = "2px solid #dc3545";
    passwordError.textContent = "Min 5 chars, 1 number & 1 special char";
    return false;
  }
}

function validateConfirmPassword() {
  if (confirmInput.value === passwordInput.value && confirmInput.value !== "") {
    confirmInput.style.borderBottom = "2px solid #28a745";
    confirmError.textContent = "";
    return true;
  } else {
    confirmInput.style.borderBottom = "2px solid #dc3545";
    confirmError.textContent = "Passwords do not match";
    return false;
  }
}

function final_validation() {
  return (
    validateName() &&
    validateEmail() &&
    validatePhone() &&
    validatePassword() &&
    validateConfirmPassword()
  );
}

nameInput.addEventListener("input", validateName);
emailInput.addEventListener("input", validateEmail);
phoneInput.addEventListener("input", validatePhone);
passwordInput.addEventListener("input", validatePassword);
confirmInput.addEventListener("input", validateConfirmPassword);

