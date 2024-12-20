function toggleLike(element) {
    const eventId = element.getAttribute('data-event-id');
    const addLikeUrl = element.getAttribute('data-add-like-url');

    fetch(addLikeUrl, {
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

function addUserToEvent(element) {
    const eventId = element.dataset.eventId;
    const addUserUrl = element.getAttribute('data-add-user-url');

    fetch(addUserUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            "Content-Type": "application/json"
        },
        credentials: "same-origin",
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById(`users-count-${eventId}`).textContent = data.users_count;
                alert("Dodano do uczestników!");
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error("Error:", error));
}