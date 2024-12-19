document.addEventListener("DOMContentLoaded", function () {
    let debounceTimeout;
    const spinner = document.querySelector("#loading-spinner");

    const showSpinner = () => {
        if (spinner) spinner.style.display = "block";
    };

    const hideSpinner = () => {
        if (spinner) spinner.style.display = "none";
    };

    const enforceSingleSelect = (formSelector, checkboxSelector) => {
        const form = document.querySelector(formSelector);
        if (!form) return;

        const checkboxes = form.querySelectorAll(checkboxSelector);

        checkboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", function () {
                if (this.checked) {
                    checkboxes.forEach((cb) => {
                        if (cb !== this) cb.checked = false;
                    });
                }
                debounceSubmit(formSelector);
            });
        });
    };

    const debounceSubmit = (formSelector, page = 1) => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            submitFiltersForm(formSelector, page);
        }, 1000);
    };

    const submitFiltersForm = (formSelector, page = 1) => {
        const form = document.querySelector(formSelector);
        const eventsContainer = document.querySelector(".event_listing");
        const paginationContainer = document.querySelector(".pagination-container");

        if (!form || !eventsContainer || !paginationContainer) {
            console.warn("Brak formularza filtrów, listy wydarzeń lub kontenera paginacji!");
            return;
        }

        const formData = new FormData(form);
        formData.set("page", page);

        const params = new URLSearchParams(formData).toString();

        showSpinner();

        fetch(`/wydarzenia/ajax/filter-events/?${params}`, {
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
                    initializePagination(formSelector);
                }
                if (typeof FB !== "undefined" && FB.XFBML) {
                    FB.XFBML.parse();
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                eventsContainer.innerHTML =
                    "<p class='text-danger'>Wystąpił błąd podczas ładowania danych.</p>";
            })
            .finally(() => {
                hideSpinner();
            });
    };

    const handlePaginationClick = (event, formSelector) => {
        event.preventDefault();
        const page = event.target.getAttribute("data-page");

        if (page) {
            submitFiltersForm(formSelector, page);
        }
    };

    const initializePagination = (formSelector) => {
        const paginationLinks = document.querySelectorAll(".pagination a");
        paginationLinks.forEach((link) => {
            link.removeEventListener("click", (e) => handlePaginationClick(e, formSelector));
            link.addEventListener("click", (e) => handlePaginationClick(e, formSelector));
        });
    };

    const initializeFilterListeners = (formSelector) => {
        const form = document.querySelector(formSelector);
        if (!form) return;

        const allCheckboxes = form.querySelectorAll(".form-check-input");
        allCheckboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", () => debounceSubmit(formSelector));
        });
    };

    const init = () => {
        const mobileFormSelector = "#filtersMenuMobile";
        const desktopFormSelector = "#filtersMenuDesktop";

        // Inicjalizacja dla formularzy mobilnych
        initializeFilterListeners(mobileFormSelector);
        enforceSingleSelect(mobileFormSelector, ".location-checkbox");
        enforceSingleSelect(mobileFormSelector, ".entry-checkbox");
        enforceSingleSelect(mobileFormSelector, ".added-by-checkbox");
        initializePagination(mobileFormSelector);

        // Inicjalizacja dla formularzy desktopowych
        initializeFilterListeners(desktopFormSelector);
        enforceSingleSelect(desktopFormSelector, ".location-checkbox");
        enforceSingleSelect(desktopFormSelector, ".entry-checkbox");
        enforceSingleSelect(desktopFormSelector, ".added-by-checkbox");
        initializePagination(desktopFormSelector);

        console.log("Filters script initialized for both mobile and desktop.");
    };

    init();
});
