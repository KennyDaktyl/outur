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

    const debounceSubmit = (formSelector) => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            submitFiltersForm(formSelector);
        }, 1000);
    };

    const submitFiltersForm = (formSelector) => {
        const form = document.querySelector(formSelector);
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
                    mapContainer.innerHTML = data.map_html;
                    initializeMapInteractions();
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
        console.log("Mapa została odświeżona.");
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
        // Obsługa formularzy mobilnych i desktopowych
        const mobileFormSelector = "#filtersMenuMobile";
        const desktopFormSelector = "#filtersMenuDesktop";

        initializeFilterListeners(mobileFormSelector);
        initializeFilterListeners(desktopFormSelector);

        enforceSingleSelect(mobileFormSelector, ".location-checkbox");
        enforceSingleSelect(mobileFormSelector, ".entry-checkbox");
        enforceSingleSelect(mobileFormSelector, ".added-by-checkbox");

        enforceSingleSelect(desktopFormSelector, ".location-checkbox");
        enforceSingleSelect(desktopFormSelector, ".entry-checkbox");
        enforceSingleSelect(desktopFormSelector, ".added-by-checkbox");

        console.log("Filters map script initialized.");
    };

    init();
});
