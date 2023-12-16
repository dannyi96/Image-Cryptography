function previewImage(event, imageId) {
    const input = event.target;
    const image = document.getElementById(imageId);

    const file = input.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            image.src = e.target.result;
        };

        reader.readAsDataURL(file);
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

function toggleState(stateIdToEnable, stateIdToDisable) {
    document.getElementById(stateIdToEnable).style.display = "block";
    document.getElementById(stateIdToDisable).style.display = "none";
}

function previewText(event, divContainerId) {
    const input = event.target;
    const container = document.getElementById(divContainerId);

    const file = input.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            container.textContent = e.target.result;
        };

        reader.readAsText(file);
    }
}

// Trigger click on the hidden file input when the custom button is clicked
document.getElementById('img-uploader-btn').addEventListener('click', function() {
    document.getElementById('file-input').click();
});