function previewImage(event, imageContainerId, imageId) {
    const input = event.target;
    const container = document.getElementById(imageContainerId);
    const image = document.getElementById(imageId);

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

function downloadImage(imgId, fileName) {
    var new_anchor = document.createElement("a")
    document.body.appendChild(new_anchor);
    new_anchor.download = fileName;
    new_anchor.href = document.getElementById(imgId).src;
    // click the anchor to trigger download
    new_anchor.click();
    new_anchor.remove();
}

function downloadKey(divId, fileName) {
    var new_anchor = document.createElement("a")
    document.body.appendChild(new_anchor);
    new_anchor.download = fileName;
    new_anchor.href = "data:text/html," + document.getElementById(divId).innerHTML;
    // click the anchor to trigger download
    new_anchor.click();
    new_anchor.remove();
}