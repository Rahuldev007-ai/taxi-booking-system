<<<<<<< HEAD
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
                return false;
            }

            if (loaderOverlay) {
=======
const loginForm = document.getElementById('user_login');
const loaderOverlay = document.getElementById('loginLoaderOverlay');
const emailValue = document.getElementById('email');
const pwsValue = document.getElementById('password');
const email_error = document.getElementById('email_error')
const pws_error = document.getElementById('pws_error')



function emailCheck() {
    const em = emailValue.value.trim()
    const emailRegex = /^[A-Za-z][A-Za-z0-9._-]*@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+$/;
    if (!emailRegex.test(em)) {
        emailValue.classList.add('invalid');
        email_error.innerText = "Enter valid email address."
        return false
    }
    emailValue.classList.remove("invalid");
    email_error.innerText = ""
    return true;

}

function pwsCheck() {
    const pws = pwsValue.value.trim()
    if (pws.length < 6) {
        pwsValue.classList.add("invalid");
        pws_error.innerText = "Enter valid password of 6 digit."
        return false
    }
    pwsValue.classList.remove("invalid");
    pws_error.innerText = ""
    return true
}

emailValue.addEventListener('blur', () => {
    emailCheck();
})


pwsValue.addEventListener('blur', () => {
    pwsCheck();
})

loginForm.addEventListener("submit", (e) => {
    let isValid = true;
    if (!emailCheck()) {
        isValid = false
    }
    if (!pwsCheck()) {
        isValid = false
    }

    if (!isValid) {
        e.preventDefault();
        alert("Please correct the invalid fields.");
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            if (loginForm.checkValidity()) {
>>>>>>> 2caebf79202aefa6a8387d6fd2594af48dd0171c
                loaderOverlay.classList.add('active');
            }
        });
    }
<<<<<<< HEAD
});
=======

})
>>>>>>> 2caebf79202aefa6a8387d6fd2594af48dd0171c
