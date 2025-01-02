document.addEventListener('DOMContentLoaded', function () {
    const maxSelections = 4;
    const categoriesContainer = document.getElementById('categories-container');
    const checkboxes = categoriesContainer.querySelectorAll('input[type="checkbox"]');
    const errorMessage = document.getElementById('categories-error');

    // Ograniczenie liczby wybranych kategorii
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const selectedCheckboxes = Array.from(checkboxes).filter(chk => chk.checked);

            if (selectedCheckboxes.length > maxSelections) {
                this.checked = false;
                errorMessage.style.display = 'flex';
            } else {
                errorMessage.style.display = 'none';
            }
        });
    });

    // Formatowanie kodu pocztowego
    document.getElementById('id_postal_code').addEventListener('input', function (e) {
        let value = e.target.value.replace(/[^0-9]/g, '');
        if (value.length > 2) {
            value = value.substring(0, 2) + '-' + value.substring(2, 5);
        }
        e.target.value = value;
    });

    // Sekcje wydarzenia
    const oneDayEvent = document.getElementById("id_event_type_1");
    const multiDayEvent = document.getElementById("id_event_type_2");
    const recurringEvent = document.getElementById("id_event_type_3");

    const oneDaySection = document.getElementById("one-day-section");
    const multiDaySection = document.getElementById("multi-day-section");
    const recurringSection = document.getElementById("recurring-section");

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

    updateSections();
    [oneDayEvent, multiDayEvent, recurringEvent].forEach(radio => {
        radio.addEventListener("change", updateSections);
    });

    // Flatpickr inicjalizacja
    flatpickr("#id_one_day_date", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        locale: "pl"
    });
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

    // Główne zdjęcie
    const mainImageInput = document.getElementById("id_main_image");
    const mainImagePreview = document.getElementById("main_image_preview");
    const croppedImageInput = document.getElementById("cropped_image");
    const imageToCrop = document.getElementById("image_to_crop");
    const cropImageButton = document.getElementById("crop_image_button");
    let cropper;

    mainImageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imageToCrop.src = e.target.result;

                const cropperModal = new bootstrap.Modal(document.getElementById("cropperModal"));
                cropperModal.show();

                cropperModal._element.addEventListener("shown.bs.modal", function () {
                    if (cropper) cropper.destroy();
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

    cropImageButton.addEventListener("click", function () {
        if (cropper) {
            const canvas = cropper.getCroppedCanvas();
            canvas.toBlob(function (blob) {
                const croppedFile = new File([blob], "cropped_main_image.jpeg", { type: "image/jpeg" });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(croppedFile);
                mainImageInput.files = dataTransfer.files;

                mainImagePreview.src = canvas.toDataURL("image/jpeg");
                mainImagePreview.style.display = "block";

                croppedImageInput.value = canvas.toDataURL("image/jpeg");
                const cropperModal = bootstrap.Modal.getInstance(document.getElementById("cropperModal"));
                cropperModal.hide();
                cropper.destroy();
                cropper = null;
            });
        }
    });

    // Zdjęcia galerii
    const galleryFields = ["gallery_image_1", "gallery_image_2", "gallery_image_3", "gallery_image_4"];
    galleryFields.forEach(fieldName => {
        const input = document.getElementById(`id_${fieldName}`);
        const preview = document.getElementById(`preview_${fieldName}`);
        const hiddenInput = document.getElementById(`cropped_${fieldName}`);
        const modal = document.getElementById(`cropperModal_${fieldName}`);
        const imageToCrop = document.getElementById(`image_to_crop_${fieldName}`);
        const cropButton = document.getElementById(`crop_image_button_${fieldName}`);
        let cropper = null;

        input.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imageToCrop.src = e.target.result;

                    const cropperModal = new bootstrap.Modal(modal);
                    cropperModal.show();

                    modal.addEventListener("shown.bs.modal", function () {
                        if (cropper) cropper.destroy();
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

        cropButton.addEventListener("click", function () {
            if (cropper) {
                const canvas = cropper.getCroppedCanvas();
                const convertedCanvas = document.createElement("canvas");
                const context = convertedCanvas.getContext("2d");
        
                // Ustaw wymiary nowego canvas
                convertedCanvas.width = canvas.width;
                convertedCanvas.height = canvas.height;
        
                // Rysuj na nowym canvas bez kanału alfa
                context.fillStyle = "#FFFFFF"; // Tło białe
                context.fillRect(0, 0, convertedCanvas.width, convertedCanvas.height);
                context.drawImage(canvas, 0, 0);
        
                convertedCanvas.toBlob(function (blob) {
                    const croppedFile = new File([blob], `${fieldName}.jpeg`, { type: "image/jpeg" });
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(croppedFile);
                    input.files = dataTransfer.files;
        
                    preview.src = convertedCanvas.toDataURL("image/jpeg");
                    preview.style.display = "block";
        
                    hiddenInput.value = convertedCanvas.toDataURL("image/jpeg");
                    const cropperModal = bootstrap.Modal.getInstance(modal);
                    cropperModal.hide();
                    cropper.destroy();
                    cropper = null;
                }, "image/jpeg");
            }
        });
    });
});
