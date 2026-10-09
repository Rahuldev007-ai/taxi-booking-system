/**
 * Separate OTP Digit Input Box Controller
 * Auto-advances focus on digit input, handles Backspace, Paste, and syncs hidden OTP input.
 */
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('otpContainer');
    if (!container) return;

    const inputs = container.querySelectorAll('.otp-digit-input');
    const hiddenOtp = document.getElementById('hidden_otp');
    const form = container.closest('form');

    function updateHiddenOtp() {
        let code = '';
        inputs.forEach(input => {
            code += input.value.trim();
        });
        if (hiddenOtp) {
            hiddenOtp.value = code;
        }
    }

    inputs.forEach((input, index) => {
        // Enforce numeric input and auto-advance
        input.addEventListener('input', function () {
            const val = this.value.replace(/[^0-9]/g, '');
            this.value = val;

            if (val) {
                this.classList.add('filled');
                if (index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            } else {
                this.classList.remove('filled');
            }
            updateHiddenOtp();
        });

        // Handle Backspace navigation
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Backspace' && !this.value && index > 0) {
                inputs[index - 1].focus();
            }
        });

        // Handle Paste event (e.g., pasting "123456")
        input.addEventListener('paste', function (e) {
            e.preventDefault();
            const clipboardData = (e.clipboardData || window.clipboardData);
            if (!clipboardData) return;

            const pastedText = clipboardData.getData('text').replace(/[^0-9]/g, '').trim();
            if (!pastedText) return;

            const digits = pastedText.split('');
            inputs.forEach((inp, idx) => {
                if (digits[idx]) {
                    inp.value = digits[idx];
                    inp.classList.add('filled');
                }
            });

            updateHiddenOtp();

            const nextFocusIndex = Math.min(digits.length, inputs.length - 1);
            inputs[nextFocusIndex].focus();
        });
    });

    if (form) {
        form.addEventListener('submit', function (e) {
            updateHiddenOtp();
            if (hiddenOtp && hiddenOtp.value.length < inputs.length) {
                e.preventDefault();
                if (window.showToast) {
                    window.showToast("Please enter all digit boxes of the OTP code.", "error", 4000);
                } else {
                    alert("Please enter all digit boxes of the OTP code.");
                }
                // Focus the first empty box
                for (let inp of inputs) {
                    if (!inp.value) {
                        inp.focus();
                        break;
                    }
                }
            }
        });
    }
});
