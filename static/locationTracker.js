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
        timeout: 5000,
        maximumAge: 0
      }
    );
  } else {
    console.error("Geolocation is not supported by this browser.");
    alert("Your browser does not support geolocation.");
  }
}