function imgError(image) {
    image.onerror = "";
    image.className = "hidden";
    return true;
}