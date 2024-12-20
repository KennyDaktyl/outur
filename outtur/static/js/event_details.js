document.addEventListener("DOMContentLoaded", function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    const toggleFormButton = document.getElementById("toggle-form");
    const form = document.getElementById("event-form");
    if (toggleFormButton && form) {
        toggleFormButton.addEventListener("click", () => {
            form.style.display = form.style.display === "none" ? "block" : "none";
        });
    }
});

