document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");

  form.addEventListener("submit", function (e) {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value;
    let remember = document.getElementById("remember").checked;

    let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (email === "") {
      alert("Please enter your email");
      e.preventDefault();
      return;
    }

    if (!email.match(emailPattern)) {
      alert("Please enter a valid email address");
      e.preventDefault();
      return;
    }

    if (password === "") {
      alert("Please enter your password");
      e.preventDefault();
      return;
    }

    if (password.length < 6) {
      alert("Password must be at least 6 characters");
      e.preventDefault();
      return;
    }

    /* Remember Me validation */
    if (!remember) {
      alert("Please click the Remember Me checkbox before login");
      e.preventDefault();
      return;
    }
  });
});
