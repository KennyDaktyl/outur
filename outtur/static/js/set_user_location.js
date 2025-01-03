document.addEventListener('DOMContentLoaded', () => {
    const sortSelects = document.querySelectorAll('.sort-select'); // Wybieramy wszystkie selecty
    const forms = document.querySelectorAll('.filter-form'); // Wybieramy wszystkie formularze
    const locationModalEl = document.getElementById('locationModal');
    const locationModal = new bootstrap.Modal(locationModalEl);
    const saveButton = document.getElementById('save-location');

    let map = null;
    let marker = null;
    let selectedLocation = null;

    // Obsługa zmiany w selectach
    sortSelects.forEach((sortSelect) => {
        sortSelect.addEventListener('change', (event) => {
            if (sortSelect.value === 'nearest') {
                event.preventDefault();
                locationModal.show();

                setTimeout(() => {
                    if (!map) {
                        map = L.map('map').setView([52.2297, 21.0122], 6);
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '© OpenStreetMap contributors'
                        }).addTo(map);

                        map.on('click', (e) => {
                            if (marker) {
                                marker.setLatLng(e.latlng);
                            } else {
                                marker = L.marker(e.latlng).addTo(map);
                            }
                            selectedLocation = e.latlng;
                        });
                    } else {
                        map.invalidateSize();
                    }
                }, 300);
            }
        });
    });

    // Usuwanie backdrop po zamknięciu modala
    locationModalEl.addEventListener('hidden.bs.modal', () => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach((backdrop) => backdrop.remove());

        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
    });

    // Obsługa zapisu lokalizacji
    saveButton.addEventListener('click', () => {
        if (selectedLocation) {
            locationModal.hide();

            // Znajdujemy widoczny formularz
            const visibleForm = Array.from(forms).find(form => form.offsetParent !== null);

            if (visibleForm) {
                let locationInput = document.createElement('input');
                locationInput.type = 'hidden';
                locationInput.name = 'user_location';
                locationInput.value = `${selectedLocation.lat},${selectedLocation.lng}`;
                visibleForm.appendChild(locationInput);

                visibleForm.submit();
            }
        }
    });
});
