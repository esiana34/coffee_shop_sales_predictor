function GetLocation(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    }
    else{
           alert("Geolocation is not supported by this browser.");
        }
    
    }

function showPosition(position){
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    console.log("Latitude:", latitude);
    console.log("Longitude:", longitude);
  
    sendLocationToPython(latitude, longitude); 
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

function sendLocationToPython(latitude, longitude) {
    fetch('http://127.0.0.1:5000/get-location', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ latitude: latitude, longitude: longitude }),
    })
    .then(response => response.json())
    .then(data => console.log('Location sent to server:', data))
    .catch((error) => console.error('Error sending location:', error));
}