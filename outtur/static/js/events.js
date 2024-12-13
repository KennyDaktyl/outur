function addUserToEvent(element) {
    const eventId = element.dataset.eventId;

    fetch(`/events/add_user_to_event/${eventId}/`, {
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
