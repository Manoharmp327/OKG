function login() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  if (username === "" || password === "") {
    alert("Please fill in both fields.");
    return;
  }

  // For demonstration purposes, we will simply redirect to a new page
  // In a real-world scenario, you would perform an AJAX request to your server for authentication
  alert("Login successful!");
  window.location.href = "next_page.html"; // Replace with your next page
}
