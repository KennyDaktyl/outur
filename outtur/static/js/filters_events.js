document.addEventListener("DOMContentLoaded", function () {
    let debounceTimeout;
    const spinner = document.querySelector("#loading-spinner");
    
    const showSpinner = () => {
        spinner.style.display = "block";
    };

    const hideSpinner = () => {
        spinner.style.display = "none";
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

    const submitFiltersForm = (page = 1) => {
        const form = document.querySelector("form.filters_form");
        const eventsContainer = document.querySelector(".event_listing");
        const paginationContainer = document.querySelector(".pagination-container");
    
        if (!form || !eventsContainer || !paginationContainer) return;
    
        const formData = new FormData(form);
        formData.set("page", page); 
    
        const params = new URLSearchParams(formData).toString();
    
        showSpinner();
    
        fetch(`/events/ajax/filter-events/?${params}`, {
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
                if (data.html) {
                    eventsContainer.innerHTML = data.html; 
                }
                if (data.pagination) {
                    paginationContainer.innerHTML = data.pagination; 
                    initializePagination();
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                eventsContainer.innerHTML =
                    "<p class='text-danger'>Wystąpił błąd podczas ładowania danych.</p>";
            })
            .finally(() => {
                hideSpinner(); 
    };

    const handlePaginationClick = (event) => {
        event.preventDefault();
        const page = event.target.getAttribute("data-page");
    
        if (page) {
            submitFiltersForm(page); 
        }
    };

    const initializePagination = () => {
        const paginationLinks = document.querySelectorAll(".pagination a");
        paginationLinks.forEach((link) => {
            link.removeEventListener("click", handlePaginationClick); 
            link.addEventListener("click", handlePaginationClick); 
        });
    };

    // Inicjalizacja przy załadowaniu strony
    initializePagination();

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
