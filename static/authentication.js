async function sendLocationToBackend(location) {
  try {
    const response = await fetch("http://127.0.0.1:5000/location/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(location),
    });

    if (!response.ok) {
      throw new Error(`Failed to send location: ${response.statusText}`);
    }

    console.log("Location sent successfully to backend:", location);
  } catch (error) {
    console.error("Error sending location to backend:", error.message);
  }
}

function startTrackingLocation() {
  console.log("Starting location tracking...");
  
  if ("geolocation" in navigator) {
    navigator.geolocation.watchPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        console.log(`Updated Location: Latitude: ${latitude}, Longitude: ${longitude}`);

        const location = { latitude, longitude };
        await sendLocationToBackend(location);
      },
      (error) => {
        console.error("Error getting geolocation:", error.message);
        alert("Location permission denied or error occurred.");
      },
      {
        enableHighAccuracy: true,
        timeout: 500000,
        maximumAge: 0
      }
    );
  } else {
    console.error("Geolocation is not supported by this browser.");
    alert("Your browser does not support geolocation.");
  }
}
function redirectHome() {
  window.location.href = "/home";
}

function validateEmail(email) {
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
}

function switchTo(form) {
  const signup = document.querySelector(".signup");
  const login = document.querySelector(".login");
  if (form === "login") {
    signup.style.display = "None";
    login.style.display = "Block";
  } else {
    signup.style.display = "Block";
    login.style.display = "None";
  }
}



async function sendLoginRequest(event) {
  event.preventDefault();
  const email = document
    .querySelector(".login-form input[name='email']")
    .value.trim();
  const password = document.querySelector(
    ".login-form input[name='password']"
  ).value;

  if (!email || !password) {
    alert("All fields are required for login.");
    return false;
  }

  if (!validateEmail(email)) {
    alert("Please enter a valid email address.");
    return false;
  }

  const payload = {
    user_mail: email,
    password: password,
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/user/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    console.log(data);

    if (data.status === "failed") {
      alert(`Login failed: ${data.message}`);
    } else {
      localStorage.setItem("trackingActive", "true");
      alert("Login successful!");


      redirectHome();
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during login. Please try again later.");
  }
}

async function sendSignUpRequest(event) {
  event.preventDefault();
  const name = document
    .querySelector(".signup-form input[name='name']")
    .value.trim();
  const phno = document
    .querySelector(".signup-form input[name='phno']")
    .value.trim();
  const email = document
    .querySelector(".signup-form input[name='email']")
    .value.trim();
  const password = document.querySelector(
    ".signup-form input[name='password']"
  ).value;

  if (!name || !phno || !email || !password) {
    alert("All fields are required for sign-up.");
    return false;
  }

  if (!validateEmail(email)) {
    alert("Please enter a valid email address.");
    return false;
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters long.");
    return false;
  }

  if (isNaN(phno) || phno.length < 10 || phno.length > 15) {
    alert("Please enter a valid phone number.");
    return false;
  }

  const payload = {
    user_name: name,
    user_mail: email,
    user_phno: phno,
    password: password,
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/user/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    console.log(data);

    if (data.status === "failed") {
      alert(`Signup failed: ${data.message}`);
    } else {
      alert("Signup successful!");
      window.location.href = "/home";
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during signup. Please try again later.");
  }
}

if (localStorage.getItem("trackingActive") === "true") {
  startTrackingLocation();
}