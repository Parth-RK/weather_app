document.addEventListener("DOMContentLoaded", function() {
    // Handle form submission
    const weatherForm = document.querySelector('form');
    if (weatherForm) {
        weatherForm.addEventListener('submit', function() {
            // Store form data in session storage before submission
            const city = document.querySelector('input[name="city"]').value;
            sessionStorage.setItem('lastCity', city);
        });
    }

    // Disable refresh warning
    window.onbeforeunload = null;

    // Handle browser back/forward cache
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    });

    // Clear form data on page load to prevent browser storing it
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
});