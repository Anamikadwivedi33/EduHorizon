document.addEventListener("DOMContentLoaded", () => {
    const section = document.querySelector(".slide-in");
    if (section) {
        section.style.opacity = "1";
        section.style.transform = "translateY(0)";
    }

    // Back to Top Button Logic
    const backToTop = document.getElementById("backToTop");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 200) {
            backToTop.style.display = "block";
        } else {
            backToTop.style.display = "none";
        }
    });

    backToTop.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});
