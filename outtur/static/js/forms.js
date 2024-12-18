

document.addEventListener("DOMContentLoaded", () => {
    // Pobierz pola formularza
    const emailField = document.getElementById("id_username");
    const phoneField = document.getElementById("id_phone_number");
    const passwordField = document.getElementById("id_password");
    const confirmPasswordField = document.getElementById("id_confirm_password");

    emailField.addEventListener("input", () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        validateField(emailField, emailRegex.test(emailField.value), "Podaj poprawny adres email.");
    });

    if (phoneField) {
        phoneField.addEventListener("input", () => {
            const phoneValue = phoneField.value.replace(/\s+/g, ""); // Usuń spacje
            const isValidPhone = /^[0-9]{9}$/.test(phoneValue);
            validateField(phoneField, isValidPhone, "Numer telefonu musi mieć dokładnie 9 cyfr.");
        });
    }

    passwordField.addEventListener("input", () => {
        const isValidPassword = passwordField.value.length >= 8;
        validateField(passwordField, isValidPassword, "Hasło musi mieć co najmniej 8 znaków.");
    });

    if (confirmPasswordField) {
        confirmPasswordField.addEventListener("input", () => {
            const isValidConfirmation = confirmPasswordField.value === passwordField.value;
            validateField(confirmPasswordField, isValidConfirmation, "Hasła muszą być takie same.");
        });
    }

    function validateField(field, isValid, errorMessage) {
        let parent = field.closest(".input-group.has-validation") || field.parentElement; 
        let feedbackElement = parent.querySelector(".invalid-feedback");
    
        if (isValid) {
            field.classList.remove("is-invalid");
            field.classList.add("is-valid");
            if (feedbackElement) feedbackElement.style.display = "none";
        } else {
            field.classList.remove("is-valid");
            field.classList.add("is-invalid");
            if (feedbackElement) {
                feedbackElement.style.display = "block";
                feedbackElement.textContent = errorMessage;
            }
        }
    }
    

    document.getElementById('toggle-password').addEventListener('click', function () {
        const passwordInput = document.getElementById('id_password');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.innerHTML = type === 'password' ? '<i class="fa-regular fa-eye"></i>' : '<i class="fa-solid fa-lock"></i>';
    });
    
    document.getElementById('toggle-confirm-password').addEventListener('click', function () {
        const passwordInput = document.getElementById('id_confirm_password');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.innerHTML = type === 'password' ? '<i class="fa-regular fa-eye"></i>' : '<i class="fa-solid fa-lock"></i>';
    });
});
