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
let allReminders = [];

window.onload = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/reminder/all");
    const data = await response.json();

    if (data.status === "success") {
      allReminders = data.reminders; 
      populateReminders(allReminders);
    } else {
      console.error("Failed to fetch reminders:", data.message);
    }
  } catch (error) {
    console.error("Error fetching reminders:", error);
  }

  
  document.getElementById("searchBar").addEventListener("input", searchReminders);
  document.getElementById("filterSelect").addEventListener("change", () =>
    filterReminders(allReminders)
  );
};

function populateReminders(reminders) {
  const remindersContainer = document.querySelector(".reminders");
  remindersContainer.innerHTML = ""; 

  if (reminders.length === 0) {
    remindersContainer.innerHTML = "<p>No reminders found.</p>";
    return;
  }

  reminders.forEach((reminder) => {
    const card = document.createElement("div");
    card.className = "reminder-card ";
    card.dataset.type = reminder.reminder_type;

    const completedClass = reminder.is_completed ? "completed" : "";

    card.innerHTML = `
      <h3 class="${completedClass}">${reminder.description}</h3>
      <p><strong>Trigger:</strong> ${new Date(reminder.time_trigger).toLocaleString()}</p>
      <p><strong>Type:</strong> ${reminder.reminder_type}</p>
      <p><strong>Status:</strong> ${reminder.is_completed ? "Completed" : "Pending"}</p>
      <div class="actions">
        <button class="update-btn" data-reminder='${JSON.stringify(reminder)}'>Update</button>
        <button class="delete-btn" data-id="${reminder.reminder_id}">Delete</button>
        <button class="complete-btn" data-id="${reminder.reminder_id}">Complete</button>
      </div>
    `;
    console.log(reminder.is_completed)
    if(reminder.is_completed === 1){
      
      card.classList.add("disable-card")
    }

    remindersContainer.appendChild(card);
  });

  remindersContainer.addEventListener("click", handleActionClick);
}

function handleActionClick(event) {
  const target = event.target;

  if (target.classList.contains("update-btn")) {
    const reminder = JSON.parse(target.dataset.reminder);
    localStorage.setItem("selectedReminder", JSON.stringify(reminder));
    window.location.href = "reminder/update-reminder";
  }

  if (target.classList.contains("delete-btn")) {
    const reminderId = target.dataset.id;
    deleteReminder(reminderId);
  }

  if (target.classList.contains("complete-btn")) {
    const reminderId = target.dataset.id;
    completeReminder(reminderId);
  }
}

function searchReminders() {
  const searchText = document.getElementById("searchBar").value.toLowerCase();
  const filteredReminders = allReminders.filter((reminder) =>
    reminder.description.toLowerCase().includes(searchText)
  );
  filterReminders(filteredReminders);
}

function filterReminders(filteredReminders = allReminders) {
  const filterType = document.getElementById("filterSelect").value;

  const remindersToShow = filteredReminders.filter((reminder) => {
    if (filterType === "all") return true;
    return reminder.reminder_type === filterType;
  });

  populateReminders(remindersToShow);
}

async function deleteReminder(reminderId) {
  console.log(`Deleting reminder with ID: ${reminderId}`);
  const payload = {
    "reminder_id" : reminderId
  }
  const response = await fetch("http://127.0.0.1:5000/reminder/delete", {
    method: "DELETE", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
  })

  const data = await response.json();
  if (data["status"] == "success"){
    alert("Reminder Deleted!")
    window.location.href = "/reminder"
  }else{
    alert("Error occured when deleting!")
  }
}

async function completeReminder(reminderId) {
  console.log(`Marking reminder as complete with ID: ${reminderId}`);
  const response = await fetch(`http://127.0.0.1:5000/reminder/complete/${reminderId}`, {
    method: "POST", 
        headers: {
          "Content-Type": "application/json",
        }
  })

  const data = await response.json();
  if (data["status"] == "success"){
    alert("Reminder Completed!")
    window.location.href = "/reminder"
  }else{
    alert("Error occured!")
  }
}

function createReminder(){
  window.location.href = "reminder/create-reminder"
}

if (localStorage.getItem("trackingActive") === "true") {
  startTrackingLocation();
}