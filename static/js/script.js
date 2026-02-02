const menuOpenButton = document.querySelector("#menu-open-button");
const menuCloseButton = document.querySelector("#menu-close-button");

menuOpenButton.addEventListener("click", () => {
    document.body.classList.toggle("show-mobile-menu");
});

menuCloseButton.addEventListener("click", () => menuOpenButton.click());

document.addEventListener("DOMContentLoaded", function() {
    const banner = document.getElementById("cookie-banner");
    const acceptBtn = document.getElementById("accept-cookies");

    if (localStorage.getItem("cookiesAccepted")) {
        banner.style.display = "none";
    }

    acceptBtn.addEventListener("click", function() {
        localStorage.setItem("cookiesAccepted", "true");
        banner.style.display = "none";
    });
});


// CONTACT FORM VALIDATION

document.addEventListener("DOMContentLoaded", function () {

    const contactForm = document.querySelector(".contact-form");

    if(contactForm){

        contactForm.addEventListener("submit", function(e){

            const name = contactForm.querySelector("input[name='name']").value.trim();
            const email = contactForm.querySelector("input[name='email']").value.trim();
            const message = contactForm.querySelector("textarea[name='message']").value.trim();

            const namePattern = /^[A-Za-z\s]+$/;
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            // NAME VALIDATION
            if(name === ""){
                alert("Please enter your name");
                e.preventDefault();
                return;
            }

            if(!namePattern.test(name)){
                alert("Name should contain only letters");
                e.preventDefault();
                return;
            }

            // EMAIL VALIDATION
            if(email === ""){
                alert("Please enter your email");
                e.preventDefault();
                return;
            }

            if(!emailPattern.test(email)){
                alert("Please enter a valid email address");
                e.preventDefault();
                return;
            }

            // MESSAGE VALIDATION
            if(message.length < 10){
                alert("Message must be at least 10 characters long");
                e.preventDefault();
                return;
            }

        });

    }

});