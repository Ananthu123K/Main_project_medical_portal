// ===== Get Elements =====
const form = document.getElementById("ambulanceForm");
const licenseInput = document.getElementById("license_number");
const ambulanceInput = document.getElementById("ambulance_number");
const emailInput = document.getElementById("email");
const phoneInput = document.getElementById("phone");
const passwordInput = document.getElementById("password");
const driverNameInput = document.getElementById("driver_name");
const usernameInput = document.getElementById("username");
const addressInput = document.getElementById("address");
const submitBtn = document.getElementById("submitBtn");

// ===== Error Elements =====
const licenseError = document.getElementById("license_error");
const ambulanceError = document.getElementById("ambulance_error");
const driverNameError = document.getElementById("driver_name_error");
const usernameError = document.getElementById("username_error");
const addressError = document.getElementById("address_error");

const emailError = document.createElement("small");
emailInput.parentNode.appendChild(emailError);
emailError.style.color = "#dc3545";

const mobileError = document.createElement("small");
phoneInput.parentNode.appendChild(mobileError);
mobileError.style.color = "#dc3545";

const passwordError = document.createElement("small");
passwordInput.parentNode.appendChild(passwordError);
passwordError.style.color = "#dc3545";

// ===== Regex Patterns =====
const licenseRegex = /^[A-Z]{2}[0-9]{2}[0-9]{4}[0-9]{7}$/;
const ambulanceRegex = /^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$/;
const phoneRegex = /^[0-9]{10}$/;
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{5,}$/;

// ===== Validation Functions =====
function validateLicense() {
    licenseInput.value = licenseInput.value.toUpperCase();
    if (licenseRegex.test(licenseInput.value)) {
        licenseError.textContent = "";
        licenseInput.style.border = "1px solid #28a745";
        return true;
    } else {
        licenseError.textContent = "Format: KL0720110001234";
        licenseInput.style.border = "1px solid #dc3545";
        return false;
    }
}

function validateAmbulance() {
    ambulanceInput.value = ambulanceInput.value.toUpperCase();
    if (ambulanceRegex.test(ambulanceInput.value)) {
        ambulanceError.textContent = "";
        ambulanceInput.style.border = "1px solid #28a745";
        return true;
    } else {
        ambulanceError.textContent = "Format: KL07AB1234";
        ambulanceInput.style.border = "1px solid #dc3545";
        return false;
    }
}

function validateEmail() {
    if (emailRegex.test(emailInput.value)) {
        emailError.textContent = "";
        emailInput.style.border = "1px solid #28a745";
        return true;
    } else {
        emailError.textContent = "Invalid email";
        emailInput.style.border = "1px solid #dc3545";
        return false;
    }
}

function validatePhone() {
    if (phoneRegex.test(phoneInput.value)) {
        mobileError.textContent = "";
        phoneInput.style.border = "1px solid #28a745";
        return true;
    } else {
        mobileError.textContent = "Invalid phone number";
        phoneInput.style.border = "1px solid #dc3545";
        return false;
    }
}

function validatePassword() {
    if (passwordRegex.test(passwordInput.value)) {
        passwordError.textContent = "";
        passwordInput.style.border = "1px solid #28a745";
        return true;
    } else {
        passwordError.textContent = "Min 5 chars, 1 number & 1 special char";
        passwordInput.style.border = "1px solid #dc3545";
        return false;
    }
}

function validateDriverName() {
    if (driverNameInput.value.trim() !== "") {
        driverNameInput.style.border = "1px solid #28a745";
        driverNameError.textContent = "";
        return true;
    } else {
        driverNameInput.style.border = "1px solid #dc3545";
        driverNameError.textContent = "Name cannot be empty";
        return false;
    }
}

function validateUsername() {
    if (usernameInput.value.trim() !== "") {
        usernameInput.style.border = "1px solid #28a745";
        usernameError.textContent = "";
        return true;
    } else {
        usernameInput.style.border = "1px solid #dc3545";
        usernameError.textContent = "Username cannot be empty";
        return false;
    }
}

function validateAddress() {
    if (addressInput.value.trim() !== "") {
        addressInput.style.border = "1px solid #28a745";
        addressError.textContent = "";
        return true;
    } else {
        addressInput.style.border = "1px solid #dc3545";
        addressError.textContent = "Address cannot be empty";
        return false;
    }
}

// ===== Toggle Submit Button =====
function toggleSubmit() {
    const validForm = validateLicense() && validateAmbulance() &&
                      validateEmail() && validatePhone() &&
                      validatePassword() && validateDriverName() &&
                      validateUsername() && validateAddress();
    submitBtn.disabled = !validForm;
    return validForm;
}

// ===== Event Listeners =====
[
    licenseInput,
    ambulanceInput,
    emailInput,
    phoneInput,
    passwordInput,
    driverNameInput,
    usernameInput,
    addressInput
].forEach(input => input.addEventListener("input", toggleSubmit));

// ===== Form Submission Check =====
form.addEventListener("submit", function(e) {
    if (!toggleSubmit()) e.preventDefault();
});

// ===== Disable initially =====
submitBtn.disabled = true;
