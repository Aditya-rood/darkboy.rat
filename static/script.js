document.addEventListener("DOMContentLoaded", function() {
    fetchUserData();
    getUserLocation();
});

function fetchUserData() {
    fetch("/userdata")
        .then(response => {
            if (response.status === 401) {
                console.log("Unauthorized! Redirecting to login...");
                window.location.href = "/";
            }
            return response.json();
        })
        .then(data => {
            const userDataTable = document.getElementById("userDataTable");
            userDataTable.innerHTML = "";

            const row = `
                <tr>
                    <td>${data.phone_number}</td>
                    <td>${data.battery_info}</td>
                    <td>${data.live_sms}</td>
                    <td>${data.location}</td>
                </tr>
            `;
            userDataTable.innerHTML += row;
        })
        .catch(error => console.error("Error fetching user data:", error));
}

function getUserLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(position => {
            const data = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };

            fetch("/update_location", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error("Error updating location:", error));
        });
    } else {
        console.log("Geolocation is not available.");
    }
}

function logout() {
    fetch("/logout").then(() => {
        window.location.href = "/";
    });
}
