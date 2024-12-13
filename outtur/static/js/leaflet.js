document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([52.2297, 21.0122], 13); // Domyślna lokalizacja (Warszawa)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let marker;
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const mapError = document.getElementById('map-error');

    // Funkcja ustawiająca marker
    function setMarker(lat, lon) {
        if (!marker) {
            marker = L.marker([lat, lon], { draggable: true }).addTo(map);
        } else {
            marker.setLatLng([lat, lon]);
        }
        map.setView([lat, lon], 13);
        latitudeInput.value = lat;
        longitudeInput.value = lon;
        mapError.style.display = 'none';
    }

    // Odczytaj istniejącą lokalizację
    if (latitudeInput.value && longitudeInput.value) {
        const lat = parseFloat(latitudeInput.value);
        const lon = parseFloat(longitudeInput.value);
        setMarker(lat, lon);
        console.log(lat)
        console.log(lon)
    }

    // Aktualizacja na podstawie kliknięcia na mapie
    map.on('click', function (e) {
        const { lat, lng } = e.latlng;
        setMarker(lat, lng);
    });

    // Przeciąganie markera
    if (!marker) {
        marker = L.marker([52.2297, 21.0122], { draggable: true }).addTo(map);
    }
    marker.on('dragend', function () {
        const { lat, lng } = marker.getLatLng();
        setMarker(lat, lng);
        
    });

    // Aktualizacja na podstawie adresu
    async function updateMap() {
        const city = document.getElementById('id_city').value;
        const street = document.getElementById('id_street').value;
        const houseNumber = document.getElementById('id_house_number').value;
        const postalCode = document.getElementById('id_postal_code').value;

        if (city && street && postalCode.length === 6) {
            const address = `${street} ${houseNumber}, ${postalCode} ${city}`;
            try {
                const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`);
                const data = await response.json();

                if (data.length > 0) {
                    const { lat, lon } = data[0];
                    setMarker(lat, lon);
                } else {
                    mapError.style.display = 'block';
                }
            } catch (error) {
                console.error('Błąd lokalizacji:', error);
                mapError.style.display = 'block';
            }
        }
    }

    // Obsługa zdarzeń
    ['id_city', 'id_street', 'id_house_number', 'id_postal_code'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('input', updateMap);
        }
    });
});
