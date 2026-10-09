/**
 * Nest Animated Toast Notification System
 * Position: Bottom Corner (fixed bottom-right)
 * Features: NO Icons, Animated Slide-in/Slide-out, Auto-removing Progress Timer
 */
(function (window) {
    'use strict';

    function getOrCreateContainer() {
        let container = document.getElementById('nest-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'nest-toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    /**
     * Display an animated toast at the bottom corner without any icons.
     * @param {string} message - Text content of the notification.
     * @param {string} type - 'success' | 'error' | 'danger' | 'warning' | 'info'
     * @param {number} duration - Auto-removal time in milliseconds (default: 4000ms).
     */
    function showToast(message, type = 'success', duration = 4000) {
        if (!message || !message.trim()) return;

        const container = getOrCreateContainer();

        // Create clean toast element (WITHOUT ANY ICON)
        const toast = document.createElement('div');
        toast.className = `nest-toast nest-toast-${type}`;

        const textSpan = document.createElement('span');
        textSpan.className = 'nest-toast-text';
        textSpan.textContent = message;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'nest-toast-close';
        closeBtn.setAttribute('aria-label', 'Close toast');
        closeBtn.innerHTML = '&times;';

        const progressBar = document.createElement('div');
        progressBar.className = 'nest-toast-progress';
        progressBar.style.animationDuration = `${duration}ms`;

        toast.appendChild(textSpan);
        toast.appendChild(closeBtn);
        toast.appendChild(progressBar);

        container.appendChild(toast);

        let timerId = null;

        function dismiss() {
            if (toast.classList.contains('nest-toast-hiding')) return;
            toast.classList.add('nest-toast-hiding');
            if (timerId) clearTimeout(timerId);
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }

        if (duration > 0) {
            timerId = setTimeout(dismiss, duration);
        }

        closeBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            dismiss();
        });

        toast.addEventListener('click', function () {
            dismiss();
        });
    }

    // Expose global window.showToast
    window.showToast = showToast;

    // Auto-detect and show server-side Django messages on page load
    document.addEventListener('DOMContentLoaded', function () {
        const djangoMessages = document.querySelectorAll('.django-toast-data');
        djangoMessages.forEach(el => {
            const msg = el.dataset.message || el.textContent.trim();
            const type = el.dataset.type || 'info';
            const duration = parseInt(el.dataset.duration || '4000', 10);
            if (msg) {
                showToast(msg, type, duration);
            }
        });
    });

})(window);
