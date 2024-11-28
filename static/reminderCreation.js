document.addEventListener("DOMContentLoaded", () => {
  const typeSelector = document.getElementById("type-selector");
  const timeFields = document.getElementById("time-fields");
  const locationFields = document.getElementById("location-fields");
  const locationSelector = document.getElementById("location-selector");

  typeSelector.addEventListener("change", async (event) => {
    const selectedType = event.target.value;

    timeFields.classList.add("hidden");
    locationFields.classList.add("hidden");

    if (selectedType === "time") {
      timeFields.classList.remove("hidden");
    } else if (selectedType === "loc") {
      await loadLocations();
      locationFields.classList.remove("hidden");
    } else if (selectedType === "time&loc") {
      timeFields.classList.remove("hidden");
      await loadLocations();
      locationFields.classList.remove("hidden");
    }
  });

  async function loadLocations() {
    try {
      const response = await fetch("http://127.0.0.1:5000/location/all");
      const data = await response.json();
      const locations = data.locations;

      locationSelector.innerHTML = '<option value="">-- Select Location --</option>';

      locations.forEach((location) => {
        const option = document.createElement("option");
        option.value = location.location_id; 
        option.textContent = location.location_detail;
        locationSelector.appendChild(option);
      });
    } catch (error) {
      console.error("Error fetching locations:", error);
    }
  }

  timeFields.classList.remove("hidden");
});

async function sendCreateReminderRequest() {
  const description = document.getElementById("description").value;
  const notificationType = document.getElementById("notification-selector").value;
  const reminderType = document.getElementById("type-selector").value;

  let timeTrigger = null;
  let locationId = null;

  if (reminderType === "time" || reminderType === "time&loc") {
    const time = document.getElementById("time-input").value;
    const date = document.getElementById("date-input").value;
    if (time && date) {
      timeTrigger = `${date}T${time}`;
    }
  }

  if (reminderType === "loc" || reminderType === "time&loc") {
    locationId = document.getElementById("location-selector").value;
  }

  const payload = {
    description,
    reminder_type: reminderType,
    notification_type: notificationType,
    time_trigger: timeTrigger || null,
    location_id: locationId || null,
  };

  console.log("Payload:", payload);

  try {
    const response = await fetch("http://127.0.0.1:5000/reminder/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      const result = await response.json();
      alert("Reminder created successfully!");
      console.log("Response:", result);
      window.location.href = "/reminder";
    } else {
      alert(`Failed to create reminder: ${response.statusText}`);
    }
  } catch (error) {
    console.error("Error:", error.message);
    alert("Failed to create reminder. Please try again.");
  }
}

