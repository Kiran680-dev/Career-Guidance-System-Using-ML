document.getElementById("signupForm").addEventListener("submit", function (e) {
  let name = document.getElementById("name").value.trim();
  let email = document.getElementById("email").value.trim();
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("confirm_password").value;

  let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

  if (name.length < 3) {
    alert("Full name must be at least 3 characters");
    e.preventDefault();
    return;
  }

  if (!email.match(emailPattern)) {
    alert("Enter a valid email address");
    e.preventDefault();
    return;
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters");
    e.preventDefault();
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    e.preventDefault();
    return;
  }
});
