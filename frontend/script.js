let map = L.map('map').setView([20.5937, 78.9629], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

let routeLine;
let markers = [];

function clearMap() {
    if (routeLine) map.removeLayer(routeLine);
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

function findRoutes() {
    const source = document.getElementById("source").value;
    const destination = document.getElementById("destination").value;

    document.getElementById("results").innerHTML = "Calculating route & AQI...";

    fetch("http://127.0.0.1:8000/routes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, destination })
    })
    .then(res => res.json())
    .then(data => {

        if (data.error) {
            document.getElementById("results").innerHTML =
                `<span style="color:red;">❌ ${data.error}</span>`;
            return;
        }

        clearMap();

        const coords = data.geometry.map(p => [p[1], p[0]]);

        routeLine = L.polyline(coords, {
            color: "blue",
            weight: 5
        }).addTo(map);

        markers.push(L.marker(data.source).addTo(map).bindPopup(
            `Source AQI: ${data.source_aqi} (${data.source_aqi_status})`
        ));

        markers.push(L.marker(data.destination).addTo(map).bindPopup(
            `Destination AQI: ${data.destination_aqi} (${data.destination_aqi_status})`
        ));

        map.fitBounds(routeLine.getBounds());

        document.getElementById("results").innerHTML = `
            <p><b>Distance:</b> ${data.distance_km} km</p>
            <p><b>Time:</b> ${data.time_min} minutes</p>
            <hr>
            <p><b>Source AQI:</b> ${data.source_aqi} (${data.source_aqi_status})</p>
            <p><b>Destination AQI:</b> ${data.destination_aqi} (${data.destination_aqi_status})</p>
        `;
    });
}
