document.addEventListener("DOMContentLoaded", function() {
    // ===== Get Input Elements =====
    const donorEmail = document.getElementById("donor_email");
    const donorPhone = document.getElementById("donor_phone");
    const donorPassword = document.getElementById("donor_password");
    const donorConfirm = document.getElementById("donor_confirm_password");
    const donorSubmit = document.getElementById("donor_submit");

    // ===== Get Error Elements =====
    const emailError = document.getElementById("donor_email_error");
    const phoneError = document.getElementById("donor_phone_error");
    const passwordError = document.getElementById("donor_password_error");
    const confirmError = document.getElementById("donor_confirm_error");

    // ===== Regex Patterns =====
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[0-9]{10}$/;
    const passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{5,}$/;

    // ===== Validation Functions =====
    function toggleSubmit() {
        const valid = emailRegex.test(donorEmail.value) &&
                      phoneRegex.test(donorPhone.value) &&
                      passwordRegex.test(donorPassword.value) &&
                      donorConfirm.value === donorPassword.value &&
                      donorConfirm.value !== "";
        donorSubmit.disabled = !valid;
    }

    donorEmail.addEventListener("input", () => {
        if (emailRegex.test(donorEmail.value)) {
            emailError.textContent = "";
            donorEmail.style.border = "1px solid #28a745";
        } else {
            emailError.textContent = "Invalid email";
            donorEmail.style.border = "1px solid #dc3545";
        }
        toggleSubmit();
    });

    donorPhone.addEventListener("input", () => {
        if (phoneRegex.test(donorPhone.value)) {
            phoneError.textContent = "";
            donorPhone.style.border = "1px solid #28a745";
        } else {
            phoneError.textContent = "Phone must be 10 digits";
            donorPhone.style.border = "1px solid #dc3545";
        }
        toggleSubmit();
    });

    donorPassword.addEventListener("input", () => {
        if (passwordRegex.test(donorPassword.value)) {
            passwordError.textContent = "";
            donorPassword.style.border = "1px solid #28a745";
        } else {
            passwordError.textContent = "Min 5 chars, 1 number & 1 special char";
            donorPassword.style.border = "1px solid #dc3545";
        }
        toggleSubmit();
    });

    donorConfirm.addEventListener("input", () => {
        if (donorConfirm.value === donorPassword.value && donorConfirm.value !== "") {
            confirmError.textContent = "";
            donorConfirm.style.border = "1px solid #28a745";
        } else {
            confirmError.textContent = "Passwords do not match";
            donorConfirm.style.border = "1px solid #dc3545";
        }
        toggleSubmit();
    });

    // Disable submit initially
    donorSubmit.disabled = true;
});
