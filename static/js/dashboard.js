const systemStatusEl = document.getElementById('system-status');
const vehicleCountEl = document.getElementById('vehicle-count');
const congestionStatusEl = document.getElementById('congestion-status');
const alertStatusEl = document.getElementById('alert-status');
const resultOutputEl = document.getElementById('result-output');
const eventsTableEl = document.getElementById('events-table');
const uploadFormEl = document.getElementById('upload-form');
const loadingEl = document.getElementById('loading');
const errorBoxEl = document.getElementById('error-box');
const trafficLights = {
  RED: document.getElementById('light-red'),
  YELLOW: document.getElementById('light-yellow'),
  GREEN: document.getElementById('light-green')
};

function setSystemStatus(message) {
  systemStatusEl.textContent = message;
}

function setTrafficLights(signalState) {
  Object.entries(trafficLights).forEach(([key, light]) => {
    light.classList.toggle('active', key === signalState);
  });
}

async function fetchHealth() {
  const response = await fetch('/api/health');
  const data = await response.json();
  setSystemStatus(data.mode === 'mock' ? 'Mock mode active' : 'Model mode active');
}

async function fetchTrafficStatus() {
  const response = await fetch('/api/traffic/status');
  const data = await response.json();
  const { traffic } = data;
  vehicleCountEl.textContent = traffic.vehicle_count;
  congestionStatusEl.textContent = traffic.status;
  alertStatusEl.textContent = traffic.emergency_detected ? 'Emergency' : 'Clear';
  setTrafficLights(traffic.signal_state || 'RED');
}

async function fetchEvents() {
  const response = await fetch('/api/events');
  const data = await response.json();
  eventsTableEl.innerHTML = '';

  (data.events || []).slice(0, 10).forEach((event) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${event.timestamp || 'n/a'}</td>
      <td>${event.detected_class || 'unknown'}</td>
      <td>${Number(event.confidence || 0).toFixed(2)}</td>
      <td>${event.emergency_alert ? 'Yes' : 'No'}</td>
      <td>${event.simulated_signal || 'RED'}</td>
    `;
    eventsTableEl.appendChild(row);
  });
}

uploadFormEl.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(uploadFormEl);
  loadingEl.classList.remove('hidden');
  errorBoxEl.classList.add('hidden');
  errorBoxEl.textContent = '';

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();

    if (!response.ok) {
      errorBoxEl.textContent = data.error || 'Request failed.';
      errorBoxEl.classList.remove('hidden');
      return;
    }

    resultOutputEl.textContent = JSON.stringify(data, null, 2);
    await fetchTrafficStatus();
    await fetchEvents();
  } catch (error) {
    errorBoxEl.textContent = 'Unable to reach the server.';
    errorBoxEl.classList.remove('hidden');
  } finally {
    loadingEl.classList.add('hidden');
  }
});

document.querySelectorAll('[data-signal]').forEach((button) => {
  button.addEventListener('click', async () => {
    const signal = button.dataset.signal;
    const response = await fetch('/api/traffic/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ signal_state: signal })
    });
    const data = await response.json();
    if (response.ok) {
      setTrafficLights(data.traffic.signal_state);
      resultOutputEl.textContent = JSON.stringify(data, null, 2);
    }
  });
});

document.getElementById('reset-button').addEventListener('click', async () => {
  const response = await fetch('/api/reset', { method: 'POST' });
  const data = await response.json();
  if (response.ok) {
    setTrafficLights(data.traffic.signal_state);
    resultOutputEl.textContent = JSON.stringify(data, null, 2);
    await fetchTrafficStatus();
    await fetchEvents();
  }
});

document.getElementById('start-webcam').addEventListener('click', async () => {
  resultOutputEl.textContent = 'Webcam demo is simulated in this prototype. A real camera can be integrated later with OpenCV and a local stream source.';
  setSystemStatus('Webcam demo available');
});

fetchHealth();
fetchTrafficStatus();
fetchEvents();
