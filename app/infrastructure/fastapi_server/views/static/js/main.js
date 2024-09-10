console.log('main.js loaded!')


const socket = io({ path: '/ws' });


// socket.on('connect', async () => {
//   for (let i = 0; i < 100; i++) {
//     const randomMessage = btoa(Math.random().toString());
//     socket.emit('message', { data: randomMessage });
//   }
//   console.log('Finish')
// });


const video = document.getElementById('video');
const cameraSelect = document.getElementById('camera-select');
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');

// Obtener la lista de dispositivos de cámara disponibles
navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    devices.forEach(device => {
      if (device.kind === 'videoinput') {
        const option = document.createElement('option');
        option.value = device.deviceId;
        option.text = device.label;
        cameraSelect.appendChild(option);
      }
    });
  })
  .catch(error => {
    console.error('Error al obtener la lista de dispositivos:', error);
  });

// Agregar evento de cambio al select de cámara
cameraSelect.addEventListener('change', async () => {
  try {
    const deviceId = cameraSelect.value;
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: deviceId
      }
    });
    video.srcObject = stream;
    startButton.disabled = true;
    stopButton.disabled = false;
  } catch (error) {
    console.error('Error al acceder a la cámara:', error);
  }
});

// Agregar evento de clic al botón de inicio
startButton.addEventListener('click', async () => {
  try {
    const deviceId = cameraSelect.value;
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: deviceId
      }
    });
    video.srcObject = stream;
    startButton.disabled = true;
    stopButton.disabled = false;
  } catch (error) {
    console.error('Error al acceder a la cámara:', error);
  }
});

// Agregar evento de clic al botón de detención
stopButton.addEventListener('click', () => {
  video.srcObject = null;
  startButton.disabled = false;
  stopButton.disabled = true;
});
