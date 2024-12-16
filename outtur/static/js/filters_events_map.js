document.addEventListener("DOMContentLoaded", function () {
    let debounceTimeout;
    const spinner = document.querySelector("#loading-spinner");

    const showSpinner = () => {
        if (spinner) spinner.style.display = "block";
    };

    const hideSpinner = () => {
        if (spinner) spinner.style.display = "none";
    };


    const enforceSingleSelect = (selector) => {
        const checkboxes = document.querySelectorAll(selector);

        checkboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", function () {
                if (this.checked) {
                    checkboxes.forEach((cb) => {
                        if (cb !== this) cb.checked = false;
                    });
                }
                debounceSubmit();
            });
        });
    };

    const debounceSubmit = () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            submitFiltersForm();
        }, 1000);
    };

    const submitFiltersForm = () => {
        const form = document.querySelector("form.filters_form");
        const mapContainer = document.querySelector("#map");

        if (!form || !mapContainer) {
            console.warn("Brak formularza filtrów lub kontenera mapy!");
            return;
        }

        const formData = new FormData(form);
        const params = new URLSearchParams(formData).toString();

        showSpinner();

        fetch(`/wydarzenia/ajax/filter-events-map/?${params}`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                if (data.map_html) {
                    mapContainer.innerHTML = data.map_html; // Podstaw nową mapę
                    initializeMapInteractions(); // Ponowna inicjalizacja mapy, jeśli wymagane
                }
            })
            .catch((error) => {
                console.error("Wystąpił błąd podczas ładowania mapy:", error);
                mapContainer.innerHTML =
                    "<p class='text-danger'>Wystąpił błąd podczas ładowania mapy.</p>";
            })
            .finally(() => {
                hideSpinner();
            });
    };

    const initializeMapInteractions = () => {
        // Tutaj możesz ponownie zainicjalizować dowolne interakcje związane z mapą
        console.log("Mapa została odświeżona.");
    };

    // Inicjalizacja listenerów dla checkboxów
    const initializeFilterListeners = () => {
        const allCheckboxes = document.querySelectorAll(".form-check-input");
        allCheckboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", debounceSubmit);
        });
    };

    // Inicjalizacja aplikacji
    const init = () => {
        initializeFilterListeners();
        console.log("Filters map script initialized.");
    };

    init();

     // Wymuszanie jednokrotnego wyboru dla każdej grupy
     enforceSingleSelect(".location-checkbox");
     enforceSingleSelect(".entry-checkbox");
     enforceSingleSelect(".added-by-checkbox");
 
     // Dodaj listener do wszystkich checkboxów
     const allCheckboxes = document.querySelectorAll(".form-check-input");
     allCheckboxes.forEach((checkbox) => {
         checkbox.addEventListener("change", debounceSubmit); 
     });
});
