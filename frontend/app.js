const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");

const carIcon = new Image();
carIcon.src = "./icons/taxi.png";

const personIcon = new Image();
personIcon.src = "./icons/persona.png";

let socket = io.connect("http://localhost:5050");

let drivers = []
let requests = []

const drawIcon = (icon, x, y, size) => {
    if (icon.complete) {
        ctx.drawImage(icon, x, y, size, size);
    }
}

const updateCanvas = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drivers.forEach(driver => drawIcon(carIcon, driver.x, driver.y, 50));
    requests.forEach(request => drawIcon(personIcon, request.x, request.y, 30));

    requestAnimationFrame(updateCanvas);
};

socket.on("update_driver", function (driver) {
    
    const index = drivers.findIndex(d => d.driver_id === driver.driver_id);
    if(index >= 0){
        drivers[index] = driver;
    }else{
        drivers.push(driver);
    }
});

socket.on('update_request', function(request) {
    const index = requests.findIndex(r => r.request_id === request.request_id);
    if (index >= 0) {
        requests[index] = request; 
    } else {
        requests.push(request); 
    }
});


requestAnimationFrame(updateCanvas);