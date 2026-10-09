document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('driver_register_form');
    if (!form) return;

    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const licenseInput = document.getElementById('license_number');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const termsCheck = document.getElementById('termsCheck');

    const errorMsgName = document.getElementById('errorMsgName');
    const errorMsgEmail = document.getElementById('errorMsgEmail');
    const errorMsgPhone = document.getElementById('errorMsgPhone');
    const errorMsgLicense = document.getElementById('errorMsgLicense');
    const errorMsgPassword = document.getElementById('errorMsgPassword');
    const errorMsgConfirmPassword = document.getElementById('errorMsgConfirmPassword');
    const errorMsgTerms = document.getElementById('errorMsgTerms');

    function setValid(input, errorElement) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        if (errorElement) errorElement.innerText = '';
    }

    function setInvalid(input, errorElement, message) {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        if (errorElement) errorElement.innerText = message;
    }

    function validateName() {
        const val = nameInput.value.trim();
        if (val.length < 3) {
            setInvalid(nameInput, errorMsgName, 'Please enter a valid driver name (at least 3 characters).');
            return false;
        }
        setValid(nameInput, errorMsgName);
        return true;
    }

    function validateEmail() {
        const val = emailInput.value.trim();
        const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
        if (!emailRegex.test(val)) {
            setInvalid(emailInput, errorMsgEmail, 'Please enter a valid email address (e.g. driver@fleet.com).');
            return false;
        }
        setValid(emailInput, errorMsgEmail);
        return true;
    }

    function validatePhone() {
        const val = phoneInput.value.trim();
        const phoneClean = val.replace(/[\s\-\(\)\+]/g, '');
        if (phoneClean.length < 10 || phoneClean.length > 15 || !/^\d+$/.test(phoneClean)) {
            setInvalid(phoneInput, errorMsgPhone, 'Please enter a valid phone number (e.g. 9876543210).');
            return false;
        }
        setValid(phoneInput, errorMsgPhone);
        return true;
    }

    function validateLicense() {
        const val = licenseInput.value.trim();
        const licenseRegex = /^[A-Za-z0-9\s\-]{5,30}$/;
        if (val.length < 5 || !licenseRegex.test(val)) {
            setInvalid(licenseInput, errorMsgLicense, 'Enter a valid driver license number (minimum 5 alphanumeric characters).');
            return false;
        }
        setValid(licenseInput, errorMsgLicense);
        return true;
    }

    function validatePassword() {
        const val = passwordInput.value.trim();
        if (val.length < 6) {
            setInvalid(passwordInput, errorMsgPassword, 'Password must be at least 6 characters long.');
            return false;
        }
        setValid(passwordInput, errorMsgPassword);
        return true;
    }

    function validateConfirmPassword() {
        const pVal = passwordInput.value.trim();
        const cpVal = confirmPasswordInput.value.trim();
        if (!cpVal) {
            setInvalid(confirmPasswordInput, errorMsgConfirmPassword, 'Please confirm your password.');
            return false;
        }
        if (pVal !== cpVal) {
            setInvalid(confirmPasswordInput, errorMsgConfirmPassword, 'Passwords do not match. Please re-enter.');
            return false;
        }
        setValid(confirmPasswordInput, errorMsgConfirmPassword);
        return true;
    }

    function validateTerms() {
        if (termsCheck && !termsCheck.checked) {
            if (errorMsgTerms) errorMsgTerms.innerText = 'You must agree to the driver terms to continue.';
            return false;
        }
        if (errorMsgTerms) errorMsgTerms.innerText = '';
        return true;
    }

    // Real-time validation listeners
    nameInput.addEventListener('blur', validateName);
    nameInput.addEventListener('input', function () { if (nameInput.classList.contains('is-invalid')) validateName(); });

    emailInput.addEventListener('blur', validateEmail);
    emailInput.addEventListener('input', function () { if (emailInput.classList.contains('is-invalid')) validateEmail(); });

    phoneInput.addEventListener('blur', validatePhone);
    phoneInput.addEventListener('input', function () { if (phoneInput.classList.contains('is-invalid')) validatePhone(); });

    licenseInput.addEventListener('blur', validateLicense);
    licenseInput.addEventListener('input', function () {
        licenseInput.value = licenseInput.value.toUpperCase();
        if (licenseInput.classList.contains('is-invalid')) validateLicense();
    });

    passwordInput.addEventListener('blur', validatePassword);
    passwordInput.addEventListener('input', function () {
        if (passwordInput.classList.contains('is-invalid')) validatePassword();
        if (confirmPasswordInput.value.trim().length > 0) validateConfirmPassword();
    });

    confirmPasswordInput.addEventListener('blur', validateConfirmPassword);
    confirmPasswordInput.addEventListener('input', function () {
        if (confirmPasswordInput.classList.contains('is-invalid')) validateConfirmPassword();
    });

    if (termsCheck) {
        termsCheck.addEventListener('change', validateTerms);
    }

    // Form submission validation
    form.addEventListener('submit', function (event) {
        const isNameOk = validateName();
        const isEmailOk = validateEmail();
        const isPhoneOk = validatePhone();
        const isLicenseOk = validateLicense();
        const isPassOk = validatePassword();
        const isConfirmOk = validateConfirmPassword();
        const isTermsOk = validateTerms();

        const allValid = isNameOk && isEmailOk && isPhoneOk && isLicenseOk && isPassOk && isConfirmOk && isTermsOk;

        if (!allValid) {
            event.preventDefault();
            event.stopPropagation();
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.focus();
            }
            return false;
        }

        const loader = document.getElementById('loader');
        const submitBtn = document.getElementById('submitBtn');
        if (loader) {
            loader.classList.remove('d-none');
            loader.classList.add('active');
        }
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerText = 'Submitting Application...';
        }
    });
});
