document.addEventListener("DOMContentLoaded", () => {
    const section = document.querySelector(".slide-in");
    if (section) {
        section.style.opacity = "1";
        section.style.transform = "translateY(0)";
    }
});
