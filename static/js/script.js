document.addEventListener('DOMContentLoaded', function () {
    var toastElList = [].slice.call(document.querySelectorAll('.custom-django-toast'))
    var toastList = toastElList.map(function (toastEl) {
        var toast = new bootstrap.Toast(toastEl, {
            delay: 3000
        })
        toast.show()
    })
});
(function () {
    const hour = new Date().getHours()
    const el = document.getElementById('timeGreeting')
    el.textContent = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening'
})()  