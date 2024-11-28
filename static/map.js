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

document.addEventListener("DOMContentLoaded", () => {
    const map = L.map("map-container").setView([51.505, -0.09], 13);
  
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
  
    let marker;
  
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        map.setView([latitude, longitude], 13);
        marker = L.marker([latitude, longitude]).addTo(map);
        document.getElementById("latitude").value = latitude;
        document.getElementById("longitude").value = longitude;
      },
      () => {
        alert("Could not fetch user location. Default map view is used.");
      }
    );
  
    map.on("click", function (e) {
      if (marker) {
        map.removeLayer(marker);
      }
      marker = L.marker(e.latlng).addTo(map);
      document.getElementById("latitude").value = e.latlng.lat;
      document.getElementById("longitude").value = e.latlng.lng;
    });
  
    document.getElementById("location-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        location_detail: document.getElementById("location-detail").value.trim(),
        latitude: parseFloat(document.getElementById("latitude").value),
        longitude: parseFloat(document.getElementById("longitude").value),
      };
  
      if (!payload.location_detail) {
        alert("Please provide a valid location detail.");
        return;
      }
  
      try {
        const response = await fetch("http://127.0.0.1:5000/location/create", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
          fetchLocations();
          document.getElementById("location-form").reset();
        }
      } catch {
        alert("An error occurred while adding the location.");
      }
    });
  
    async function fetchLocations() {
      try {
        const response = await fetch("http://127.0.0.1:5000/location/all");
        const result = await response.json();
        const tableBody = document.getElementById("locations-list");
        tableBody.innerHTML = "";
  
        if (response.ok && result.locations) {
          result.locations.forEach((location) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${location.location_detail}</td>
              <td>${location.latitude}</td>
              <td>${location.longitude}</td>
              <td><button class="delete-btn" data-id="${location.location_id}">Delete</button></td>
            `;
            tableBody.appendChild(row);
          });
  
          document.querySelectorAll(".delete-btn").forEach((button) => {
            button.addEventListener("click", () => deleteLocation(button.dataset.id));
          });
        } else {
          alert(result.message || "No locations found.");
        }
      } catch {
        alert("An error occurred while fetching locations.");
      }
    }
  
    async function deleteLocation(locationId) {
      if (!confirm("Are you sure you want to delete this location?")) return;
  
      try {
        const response = await fetch(`http://127.0.0.1:5000/location/delete/${locationId}`, {
          method: "DELETE",
        });
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
          fetchLocations();
        }
      } catch {
        alert("An error occurred while deleting the location.");
      }
    }
  
    fetchLocations();
  });

  if (localStorage.getItem("trackingActive") === "true") {
    startTrackingLocation();
  }