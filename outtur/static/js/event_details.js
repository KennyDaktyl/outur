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

function toggleLike(element) {
    const eventId = element.getAttribute('data-event-id');

    fetch(`/wydarzenia/add-like-event/${eventId}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likesCountElement = document.getElementById(`likes-count-${eventId}`);
            likesCountElement.textContent = data.likes_count;

            if (data.is_liked) {
                element.classList.remove('text-dark');
                element.classList.add('text-danger');
                element.setAttribute('title', 'Kliknij, aby usunąć polubienie');
            } else {
                element.classList.remove('text-danger');
                element.classList.add('text-dark');
                element.setAttribute('title', 'Kliknij, aby polubić');
            }
        } else {
            alert('Nie udało się zmienić statusu polubienia.');
        }
    })
    .catch(error => {
        console.error('Błąd:', error);
    });
}