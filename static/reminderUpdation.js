document.addEventListener("DOMContentLoaded", async () => {
    const selectedReminder = JSON.parse(localStorage.getItem("selectedReminder"));
  
    if (!selectedReminder) {
      console.error("No reminder selected in localStorage.");
      return;
    }
  
    const descriptionInput = document.getElementById("description");
    const timeInput = document.getElementById("time-input");
    const dateInput = document.getElementById("date-input");
    const locationSelector = document.getElementById("location-selector");
    const typeSelector = document.getElementById("type-selector");
  
    descriptionInput.value = selectedReminder.description ;
    const [date, time] = (selectedReminder.time_trigger || "").split("T");
    dateInput.value = date || "";
    timeInput.value = time || "";
    locationSelector.value = selectedReminder.location_id || "";
  
    
    if (selectedReminder.time_trigger && selectedReminder.location_id) {
      typeSelector.value = "time&loc";
    } else if (selectedReminder.time_trigger) {
      typeSelector.value = "time";
    } else if (selectedReminder.location_id) {
      typeSelector.value = "loc";
    }
  
    
    await toggleFields(typeSelector.value);
  
    typeSelector.addEventListener("change", async (event) => {
      await toggleFields(event.target.value);
    });
  
    async function toggleFields(type) {
      const timeFields = document.getElementById("time-fields");
      const locationFields = document.getElementById("location-fields");
  
      timeFields.classList.add("hidden");
      locationFields.classList.add("hidden");
  
      if (type === "time") {
        timeFields.classList.remove("hidden");
      } else if (type === "loc") {
        await loadLocations();
        locationFields.classList.remove("hidden");
      } else if (type === "time&loc") {
        timeFields.classList.remove("hidden");
        await loadLocations();
        locationFields.classList.remove("hidden");
      }
    }
  
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
  });
  
  async function sendUpdateReminderRequest() {
    try {
      const selectedReminder = JSON.parse(localStorage.getItem("selectedReminder"));
      if (!selectedReminder) {
        console.error("No reminder selected in localStorage.");
        return;
      }
  
      const reminderId = selectedReminder.reminder_id;
      const description = document.getElementById("description").value;
      const time = document.getElementById("time-input").value;
      const date = document.getElementById("date-input").value;
      const locationId = document.getElementById("location-selector").value;
      const typeSelector = document.getElementById("type-selector").value;
  
      const timeTrigger = date && time ? `${date}T${time}` : null;
  
      const payload = {
        reminder_id: reminderId,
        description,
        notification_type : "mail",
        reminder_type : typeSelector,
        time_trigger: timeTrigger,
        location_id: locationId || null,
      };
  
      console.log("Payload to send:", payload);
  
      const response = await fetch("http://127.0.0.1:5000/reminder/update", {
        method: "PUT", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        console.log("Reminder updated successfully.");
        alert("Reminder updated successfully.")
        window.location.href = "/reminder"
      } else {
        console.error("Error updating reminder:", response.statusText);
      }
    } catch (error) {
      console.error("Error sending update request:", error);
    }
  }
  