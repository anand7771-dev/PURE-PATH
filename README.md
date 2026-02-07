# 🌿 PurePath – Health-First Navigation System

PurePath is a **health-aware navigation web application** that helps users plan routes while considering **air quality (AQI)**. Unlike traditional navigation systems that focus only on distance and time, PurePath integrates **real-time AQI data** and an **AI health assistant** to support safer travel decisions.

---

## 🚀 Features

- 🗺️ **Route Planning**
  - Find routes between any two locations
  - View distance and estimated travel time
  - Interactive map using Leaflet and OpenStreetMap

- 🌫️ **Air Quality Index (AQI) Monitoring**
  - Real-time AQI for source and destination
  - Data fetched from WAQI (World Air Quality Index)

- 🤖 **AQI Health Assistant (Chatbot)**
  - Ask questions about AQI in different cities
  - Get travel safety advice based on pollution levels
  - Simple, rule-based AI logic

- ⚡ **Fast & Lightweight Backend**
  - Built using FastAPI
  - REST APIs for routing, AQI, and chatbot

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- Leaflet.js
- OpenStreetMap

### Backend
- Python
- FastAPI
- Requests library

### APIs Used
- **OpenRouteService** – Geocoding
- **OSRM** – Route calculation (distance & time)
- **WAQI API** – Real-time Air Quality Index data

---

## 📂 Project Structure

purepath/
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ ├── odisha_aqi_data.csv
│ └── odisha_aqi_transport_places.csv
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
│
└── README.md
