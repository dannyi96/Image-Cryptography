function previewImage(event) {
    const input = event.target;
    const container = document.getElementById('image-container');
    const image = document.getElementById('uploaded-image');

    const file = input.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            image.src = e.target.result;
        };

        reader.readAsDataURL(file);

        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}
