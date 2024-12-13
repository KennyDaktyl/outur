document.addEventListener('DOMContentLoaded', function () {
    const maxSelections = 4;
    const categoriesContainer = document.getElementById('categories-container');
    const checkboxes = categoriesContainer.querySelectorAll('input[type="checkbox"]');
    const errorMessage = document.getElementById('categories-error');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const selectedCheckboxes = Array.from(checkboxes).filter(chk => chk.checked);

            if (selectedCheckboxes.length > maxSelections) {
                this.checked = false; 
                errorMessage.style.display = 'flex';
            } else {
                errorMessage.style.display = 'none' 
            }
        });
    });

    document.getElementById('id_postal_code').addEventListener('input', function(e) {
        let value = e.target.value.replace(/[^0-9]/g, ''); 
        if (value.length > 2) {
            value = value.substring(0, 2) + '-' + value.substring(2, 5); 
        }
        e.target.value = value;
    });

    const oneDayEvent = document.getElementById("id_event_type_1");
    const multiDayEvent = document.getElementById("id_event_type_2");
    const recurringEvent = document.getElementById("id_event_type_3");

    const oneDaySection = document.getElementById("one-day-section");
    const multiDaySection = document.getElementById("multi-day-section");
    const recurringSection = document.getElementById("recurring-section");

    // Funkcja do ustawiania widoczności sekcji na podstawie zaznaczenia
    function updateSections() {
        if (oneDayEvent.checked) {
            oneDaySection.classList.remove("d-none");
            multiDaySection.classList.add("d-none");
            recurringSection.classList.add("d-none");
        } else if (multiDayEvent.checked) {
            oneDaySection.classList.add("d-none");
            multiDaySection.classList.remove("d-none");
            recurringSection.classList.add("d-none");
        } else if (recurringEvent.checked) {
            oneDaySection.classList.add("d-none");
            multiDaySection.classList.add("d-none");
            recurringSection.classList.remove("d-none");
        }
    }

    // Inicjalizacja na podstawie bieżącego stanu
    updateSections();

    // Event listener dla zmian typu wydarzenia
    [oneDayEvent, multiDayEvent, recurringEvent].forEach(radio => {
        radio.addEventListener("change", updateSections);
    });

    // Inicjalizacja Flatpickr dla wydarzenia jednodniowego (data + godzina)
    flatpickr("#id_one_day_date", {
        enableTime: true,        
        dateFormat: "Y-m-d H:i",  
        time_24hr: true,         
        locale: "pl"             
    });

    // Inicjalizacja Flatpickr dla wydarzeń kilkudniowych (tylko data)
    flatpickr("#id_start_date", {
        enableTime: true,        
        dateFormat: "Y-m-d H:i",  
        time_24hr: true,         
        locale: "pl"        
    });

    flatpickr("#id_end_date", {
        enableTime: true,        
        dateFormat: "Y-m-d H:i",  
        time_24hr: true,         
        locale: "pl"        
    });

    const mainImageInput = document.getElementById("id_main_image");
    const mainImagePreview = document.getElementById("main_image_preview");
    const croppedImageInput = document.getElementById("cropped_image");
    const imageToCrop = document.getElementById("image_to_crop");
    const cropImageButton = document.getElementById("crop_image_button");
    let cropper;

    // Obsługa wyboru pliku
    mainImageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];

        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imageToCrop.src = e.target.result;

                // Pokaż modal do przycinania
                const cropperModal = new bootstrap.Modal(document.getElementById("cropperModal"));
                cropperModal.show();

                cropperModal._element.addEventListener("shown.bs.modal", function () {
                    // Inicjalizacja Cropper.js
                    if (cropper) {
                        cropper.destroy();
                    }
                    cropper = new Cropper(imageToCrop, {
                        aspectRatio: 4 / 3,
                        viewMode: 1,
                        autoCropArea: 1,
                        responsive: true,
                        background: false,
                    });
                });
            };
            reader.readAsDataURL(file);
        }
    });

    // Obsługa przycisku "Przytnij"
    cropImageButton.addEventListener("click", function () {
        if (cropper) {
            const canvas = cropper.getCroppedCanvas();

            // Ustaw przycięty obraz jako podgląd
            mainImagePreview.src = canvas.toDataURL("image/jpeg");
            mainImagePreview.style.display = "block";

            // Zapisz obraz w ukrytym polu jako Base64
            croppedImageInput.value = canvas.toDataURL("image/jpeg");

            // Zamknij modal
            const cropperModal = bootstrap.Modal.getInstance(document.getElementById("cropperModal"));
            cropperModal.hide();

            // Zniszcz cropper
            cropper.destroy();
            cropper = null;
        }
    });

    function setupImagePreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);

        input.addEventListener("change", function (event) {
            const file = event.target.files[0];

            if (file && file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = "block"; // Pokaż obraz
                };
                reader.readAsDataURL(file);
            } else {
                preview.src = "";
                preview.style.display = "none"; // Ukryj obraz, jeśli plik nie jest obrazem
            }
        });
    }

    // Inicjalizacja podglądów dla każdego pola
    // Inicjalizacja podglądów dla każdego pola
    setupImagePreview("id_gallery_image_1", "preview_gallery_image_1");
    setupImagePreview("id_gallery_image_2", "preview_gallery_image_2");
    setupImagePreview("id_gallery_image_3", "preview_gallery_image_3");
    setupImagePreview("id_gallery_image_4", "preview_gallery_image_4");
});