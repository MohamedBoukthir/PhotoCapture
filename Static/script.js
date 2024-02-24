navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream) {
  var video = document.getElementById('video');
  video.srcObject = stream;
  video.play();
})
.catch(function(err) {
  console.error('Error accessing camera: ', err);
});

document.getElementById('capture').addEventListener('click', function() {
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
context.drawImage(video, 0, 0, 640, 480);

// Convert the canvas content to base64 data URL
var imageData = canvas.toDataURL('image/png');

// Send the image data to the server
sendToServer(imageData);
});

function sendToServer(imageData) {
fetch('/upload', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ image: imageData })
})
.then(response => response.json())
.then(data => {
  console.log('Server response:', data);
})
.catch(error => {
  console.error('Error sending data to server:', error);
});
}