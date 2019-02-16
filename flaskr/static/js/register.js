var pass1 = document.getElementById("password1");
var pass2 = document.getElementById("password2")
pass2.addEventListener("input", function (event) {
  if (pass1.value !== pass2.value) {
    pass2.setCustomValidity("Two passwords are different");
  } else {
    pass2.setCustomValidity("");
  }
});