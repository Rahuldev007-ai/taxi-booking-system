var user_register = document.getElementById('user_register');

var nameInput = document.getElementById('name');
var emailInput = document.getElementById('email');
var phoneInput = document.getElementById('phone');
var passwordInput = document.getElementById('password');
var confirm_passwordInput = document.getElementById('confirm_password');

var errorMsg = document.getElementById('errorMsg')
var errorMsgEmail = document.getElementById('errorMsgEmail')
var errorMsgPhone = document.getElementById('errorMsgPhone')
var errorMsgCpws =  document.getElementById('errorMsgCpws')
var errorMsgpws =  document.getElementById('errorMsgpws')

function validateName() {

    const txt = nameInput.value.trim();

    if (txt.length < 3) {
        nameInput.classList.add('invalid');
        errorMsg.innerText = "Plese enter valid username"
        return false;
    }

    nameInput.classList.remove('invalid');
    errorMsg.innerText = ""
    return true;
}

function validateEmail(){
    const email = emailInput.value.trim()
    const emailRegex = /^[A-Za-z][A-Za-z0-9._-]*@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+$/;
    if (!emailRegex.test(email)){
        emailInput.classList.add('invalid');
        errorMsgEmail.innerText = "Enter valid email address."
        return false
    }
    emailInput.classList.remove("invalid");
    errorMsgEmail.innerText = ""
    return true;
}

function validatePhone(){
    const phone = phoneInput.value.trim()
    const phoneRegex = /^(?:\+91[\s-]?)?[6-9]\d{9}$/;
    if (!phoneRegex.test(phone)){
        errorMsgPhone.innerText = "Please enter valid phone number"
        phoneInput.classList.add("invalid");
        return false;
    }
    errorMsgPhone.innerText = ""
    phoneInput.classList.remove("invalid");
    return true;
}

function validatePws(){
    const password  = passwordInput.value.trim()
    if (password.length < 6){
        errorMsgpws.innerText = "Password shoud be 6 digit or more"
        passwordInput.classList.add("invalid")
        return false
    }
    errorMsgpws.innerText = ""
    passwordInput.classList.remove('invaid')
    return true
}

function validateCpws(){
    const password  = passwordInput.value.trim()
    const cpassword  = confirm_passwordInput.value.trim()
    if (password != cpassword){
        errorMsgCpws.innerText = "Please enter same password"
        confirm_passwordInput.classList.add("invalid")
        return false
    }
    errorMsgCpws.innerText = ""
    confirm_passwordInput.classList.remove('invaid')
    return true
}


nameInput.addEventListener("blur", function () {
    validateName();
});
emailInput.addEventListener("blur", function () {
    validateEmail();
});
phoneInput.addEventListener("blur", function () {
    validatePhone();
});
passwordInput.addEventListener("blur", function () {
    validatePws();
});
confirm_passwordInput.addEventListener("blur", function () {
    validateCpws();
});

user_register.addEventListener("submit", function (event) {

    let isValid = true;
    if (!validateName()) {
        isValid = false
    }
    if (!validateEmail()) {
        isValid = false
    }
    if (!validatePhone()) {
        isValid = false
    }
    if (!validatePws()) {
        isValid = false
    }
    if (!validateCpws()) {
        isValid = false
    }

    if (!isValid) {
        event.preventDefault();
        alert("Please correct the invalid fields.");
    }

    const loader = document.getElementById('loader');
    const submitBtn = document.getElementById('submitBtn');
    loader.classList.remove("d-none");

    submitBtn.disabled  = true
    submitBtn.innerText = "Create account...";

});