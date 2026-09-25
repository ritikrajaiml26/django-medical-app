// ====================== SIGNUP LOGIC ======================
const signupForm = document.getElementById("signupForm");
if (signupForm) {
  signupForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirm = document.getElementById("confirmPassword").value.trim();

    if (password !== confirm) {
      alert("Passwords do not match!");
      return;
    }

    // ✅ Save user in localStorage
    const user = { name, email, password };
    localStorage.setItem("medicineUser", JSON.stringify(user));

    alert("Account created successfully! Please login now.");
    window.location.href = "index.html";
  });
}


// ====================== LOGIN LOGIC ======================
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    const storedUser = localStorage.getItem("medicineUser");

    if (!storedUser) {
      alert("No account found! Please sign up first.");
      window.location.href = "signup.html";
      return;
    }

    const user = JSON.parse(storedUser);

    if (user.email === email && user.password === password) {
      alert(`Welcome back, ${user.name}!`);
      window.location.href = "dashboard.html";
    } else {
      alert("Invalid email or password!");
    }
  });
}
