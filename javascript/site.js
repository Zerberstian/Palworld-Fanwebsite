// javascript/script.js
const img = document.getElementById("map-img");

img.addEventListener("click", () => {
    if (img.style.transform === "scale(2)") {
        img.style.transform = "scale(1)";
        img.style.cursor = "zoom-in";
    } else {
        img.style.transform = "scale(2)";
        img.style.cursor = "zoom-out";
    }
});
