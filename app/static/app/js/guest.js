function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setLocation);
    }
}

function encodeData(data) {
    return Object.keys(data).map(function (key) {
        return [key, data[key]].map(encodeURIComponent).join("=");
    }).join("&");
}

function getAddress(road, houseNumber, city) {
    var address = "";
    if (typeof road !== 'undefined') {
        address = address + road;
        if (typeof houseNumber !== 'undefined') {
            address = address + " " + houseNumber;
        }
    }

    if (typeof city != 'undefined') {
        if (typeof road !== 'undefined') {
            address = address + ", ";
        }
        address = address + city;
    }

    return address;
}

function setLocation(position) {
    var apiToken = '43cf3f75156b90';
    var apiBaseUrl = 'https://eu1.locationiq.com/v1/reverse.php?';
    var data = {
        key: apiToken,
        lat: position.coords.latitude,
        lon: position.coords.longitude,
        format: 'json'
    };
    var params = encodeData(data);
    var apiUrl = apiBaseUrl + params;

    fetch(apiUrl)
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            var road = jsonResponse.address.road;
            var houseNumber = jsonResponse.address.house_number;
            var city = jsonResponse.address.city;
            var address = getAddress(road, houseNumber, city);
            document.getElementById("location").value = address;
        });
}

getLocation();