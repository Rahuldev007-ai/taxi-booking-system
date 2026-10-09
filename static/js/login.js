document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('user_login');
    const loaderOverlay = document.getElementById('loginLoaderOverlay');
    const emailValue = document.getElementById('email');
    const pwsValue = document.getElementById('password');
    const email_error = document.getElementById('email_error');
    const pws_error = document.getElementById('pws_error');

    function emailCheck() {
        if (!emailValue) return true;
        const em = emailValue.value.trim();
        const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
        if (!emailRegex.test(em)) {
            emailValue.classList.add('is-invalid');
            if (email_error) email_error.innerText = "Enter a valid email address.";
            return false;
        }
        emailValue.classList.remove("is-invalid");
        if (email_error) email_error.innerText = "";
        return true;
    }

    function pwsCheck() {
        if (!pwsValue) return true;
        const pws = pwsValue.value.trim();
        if (pws.length < 6) {
            pwsValue.classList.add("is-invalid");
            if (pws_error) pws_error.innerText = "Password must be at least 6 characters.";
            return false;
        }
        pwsValue.classList.remove("is-invalid");
        if (pws_error) pws_error.innerText = "";
        return true;
    }

    if (emailValue) {
        emailValue.addEventListener('blur', emailCheck);
    }

    if (pwsValue) {
        pwsValue.addEventListener('blur', pwsCheck);
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            const validEmail = emailCheck();
            const validPws = pwsCheck();

            if (!validEmail || !validPws) {
                e.preventDefault();
                if (window.showToast) {
                    window.showToast("Please enter a valid email address and password.", "error", 4000);
                }
                return false;
            }

            if (loaderOverlay) {
                loaderOverlay.classList.add('active');
            }
        });
    }
});
