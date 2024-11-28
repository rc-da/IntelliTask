# IntelliTask

## Description
**IntelliTask** is a smart and efficient reminder application that allows users to create reminders based on time and location. It features an interactive map interface powered by **Leaflet** and **OpenStreetMap**, enabling users to select specific locations for reminders. The app uses **GeoAPI** to fetch the user’s current location dynamically and sends reminder notifications through email using the **SMTP module**. Time-based reminders are managed via **APScheduler**.

---

## Features
- **Time-Based Reminders:** Set reminders for specific dates and times.
- **Location-Based Reminders:** Choose locations using an interactive map.
- **Dynamic Location Fetching:** Automatically retrieve user location using GeoAPI.
- **Email Notifications:** Reminders are sent via email using the SMTP protocol.
- **Interactive Map Interface:** Select and visualize locations with Leaflet and OpenStreetMap.

---

## Tech Stack
### Frontend:
- **HTML** and **CSS:** For creating a responsive and user-friendly interface.

### Backend:
- **Flask:** A lightweight framework for handling APIs and server-side logic.
- **APScheduler:** To schedule and manage time-based reminders.
- **SMTP Module:** For sending reminder notifications via email.

### Mapping & Geolocation:
- **Leaflet:** For the interactive map interface.
- **OpenStreetMap:** To provide location data.
- **GeoAPI:** To dynamically fetch the user's current location.


