
function imgError(image) {
    image.onerror = "";
    image.src = "/static/images/nopic.jpg";
    return true;
}

