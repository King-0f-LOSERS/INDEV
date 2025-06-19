document.addEventListener("DOMContentLoaded", function () {
    const logo = document.querySelector(".logo");
    const names = [
        { text: "INDEV", color: "white" },
        { text: "INDIA'S", color: "orange" },
        { text: "NEWEST", color: "orange" },
        { text: "DIRECT", color: "white" },
        { text: "ECOMMERCE", color: "lime" },
        { text: "VENDOR", color: "lime" }
    ];
    let index = 0;

    function changeLogoText() {
        logo.textContent = names[index].text;
        logo.style.color = names[index].color;
        index = (index + 1) % names.length;
    }

    setInterval(changeLogoText, 2000); // Change every 2 seconds
});
