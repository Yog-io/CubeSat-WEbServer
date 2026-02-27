const maxDataPoints = 30; // Points to show on chart at once

// Colors
const colors = {
    temp: '#ef4444',
    hum: '#3b82f6',
    press: '#eab308',
    alt: '#10b981',
    accelX: '#f43f5e',
    accelY: '#8b5cf6',
    accelZ: '#d946ef',
    gyroX: '#f97316',
    gyroY: '#06b6d4',
    gyroZ: '#14b8a6',
    vib: '#84cc16',
    gpsLat: '#f43f5e',
    gpsLon: '#3b82f6',
    gpsAlt: '#22c55e'
};

const darkChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    color: '#94a3b8',
    plugins: {
        legend: { labels: { color: '#94a3b8' } }
    },
    scales: {
        x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8', display: false } },
        y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } }
    },
    animation: { duration: 0 }
};

const initChart = (ctxId, datasets) => {
    return new Chart(document.getElementById(ctxId).getContext('2d'), {
        type: 'line',
        data: {
            labels: Array(maxDataPoints).fill(''),
            datasets: datasets.map(ds => ({
                label: ds.label,
                data: Array(maxDataPoints).fill(null),
                borderColor: ds.color,
                backgroundColor: ds.color + '33',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4,
                fill: ds.fill || false
            }))
        },
        options: darkChartOptions
    });
};

const charts = {
    dht: initChart('dhtChart', [{ label: 'Temp (°C)', color: colors.temp }, { label: 'Humidity (%)', color: colors.hum }]),
    bmp: initChart('bmpChart', [{ label: 'Pressure (hPa)', color: colors.press }]),
    accel: initChart('accelChart', [{ label: 'Accel X', color: colors.accelX }, { label: 'Accel Y', color: colors.accelY }, { label: 'Accel Z', color: colors.accelZ }]),
    gyro: initChart('gyroChart', [{ label: 'Gyro X', color: colors.gyroX }, { label: 'Gyro Y', color: colors.gyroY }, { label: 'Gyro Z', color: colors.gyroZ }]),
    vib: initChart('vibChart', [{ label: 'Vibration Level', color: colors.vib, fill: true }]),
    gps: initChart('gpsChart', [{ label: 'Latitude', color: colors.gpsLat }, { label: 'Longitude', color: colors.gpsLon }, { label: 'Altitude', color: colors.gpsAlt }])
};

// Playback State
let telemetryData = [];
let playbackIndex = 0;
let isPlaying = false;
let playbackTimeout = null;

// DOM Elements
const btnPlay = document.getElementById('btn-play');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const scrubber = document.getElementById('time-scrubber');
const timeDisplay = document.getElementById('current-playback-time');
const controlsWrapper = document.getElementById('playback-controls');
const statusText = document.getElementById('status-text');

const formatTime = (timestamp) => {
    const d = new Date(timestamp * 1000);
    return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
};

const updateDOMValue = (id, value) => {
    document.getElementById(id).innerText = value !== undefined ? value : '--';
};

const updateChartData = (chart, newValues) => {
    chart.data.labels.push('');
    chart.data.labels.shift();
    chart.data.datasets.forEach((dataset, index) => {
        dataset.data.push(newValues[index]);
        dataset.data.shift();
    });
    chart.update();
};

const renderFrame = (index) => {
    if (index >= telemetryData.length) {
        pausePlayback();
        return;
    }

    playbackIndex = index;
    const data = telemetryData[index];

    // Update UI
    if (data.timestamp) {
        timeDisplay.innerText = formatTime(data.timestamp);
    }
    scrubber.value = index;

    // Update values
    updateDOMValue('val-dht-temp', data.dht11?.temperature);
    updateDOMValue('val-dht-hum', data.dht11?.humidity);
    updateDOMValue('val-bmp-press', data.bmp280?.pressure);
    updateDOMValue('val-bmp-alt', data.bmp280?.altitude);
    updateDOMValue('val-mpu-accel-z', data.mpu9250?.accel?.z);
    updateDOMValue('val-mpu-gyro-z', data.mpu9250?.gyro?.z);
    updateDOMValue('val-vib', data.vibration?.level);
    updateDOMValue('val-gps-lat', data.gps?.latitude);
    updateDOMValue('val-gps-lon', data.gps?.longitude);
    updateDOMValue('val-gps-alt', data.gps?.altitude);

    // Update charts
    if (data.dht11) updateChartData(charts.dht, [data.dht11.temperature, data.dht11.humidity]);
    if (data.bmp280) updateChartData(charts.bmp, [data.bmp280.pressure]);
    if (data.mpu9250) {
        updateChartData(charts.accel, [data.mpu9250.accel.x, data.mpu9250.accel.y, data.mpu9250.accel.z]);
        updateChartData(charts.gyro, [data.mpu9250.gyro.x, data.mpu9250.gyro.y, data.mpu9250.gyro.z]);
    }
    if (data.vibration) updateChartData(charts.vib, [data.vibration.level]);
    if (data.gps) updateChartData(charts.gps, [data.gps.latitude, data.gps.longitude, data.gps.altitude]);
};

const playNextFrame = () => {
    if (!isPlaying || playbackIndex >= telemetryData.length - 1) {
        pausePlayback();
        return;
    }

    const currentFrameTime = telemetryData[playbackIndex].timestamp || 0;
    const nextFrameTime = telemetryData[playbackIndex + 1].timestamp || 0;

    renderFrame(playbackIndex + 1);

    // Calculate real-time delay or fallback to nominal delay if timestamps are missing
    let delayMs = 1000;
    if (currentFrameTime > 0 && nextFrameTime > 0) {
        delayMs = (nextFrameTime - currentFrameTime) * 1000;
    }
    delayMs = Math.max(10, Math.min(delayMs, 2000)); // Cap between 10ms and 2s

    playbackTimeout = setTimeout(playNextFrame, delayMs);
};

const startPlayback = () => {
    if (telemetryData.length === 0 || playbackIndex >= telemetryData.length - 1) return;
    isPlaying = true;
    btnPlay.style.display = 'none';
    btnPause.style.display = 'inline-block';
    playNextFrame();
};

const pausePlayback = () => {
    isPlaying = false;
    btnPlay.style.display = 'inline-block';
    btnPause.style.display = 'none';
    clearTimeout(playbackTimeout);
};

const resetPlayback = () => {
    pausePlayback();
    renderFrame(0);
};

// Event Listeners
btnPlay.addEventListener('click', startPlayback);
btnPause.addEventListener('click', pausePlayback);
btnReset.addEventListener('click', resetPlayback);

scrubber.addEventListener('input', (e) => {
    pausePlayback();
    renderFrame(parseInt(e.target.value, 10));
});

// Init
const fetchHistory = async () => {
    statusText.innerText = "Downloading large log file...";
    try {
        const response = await fetch('/api/readings');
        if (!response.ok) throw new Error("API not ok");

        statusText.innerText = "Parsing history...";

        // Fetch as text to support both normal JSON array and streaming JSON Lines
        const rawText = await response.text();

        if (!rawText || rawText.trim() === '') {
            statusText.innerText = "No data available";
            return;
        }

        const trimmed = rawText.trim();

        // Defensive Parsing logic
        if (trimmed.startsWith('[')) {
            // It's a standard JSON array
            try {
                telemetryData = JSON.parse(trimmed);
            } catch (e) {
                console.error("Failed to parse JSON array", e);
            }
        } else if (trimmed.startsWith('{')) {
            // It might be JSON lines (multiple JSON objects separated by newline)
            // Or it could be a single JSON object.
            const lines = trimmed.split('\n');
            telemetryData = [];

            for (let line of lines) {
                line = line.trim();
                if (!line) continue;

                // If the single JSON object itself spans multiple lines, 
                // this split by newline breaks it.
                // Let's attempt to test if the whole thing is one big object first
                if (lines.length > 5 && line.endsWith(',')) {
                    // Try parsing whole thing (fallback to single object)
                    try {
                        const wholeObj = JSON.parse(trimmed);
                        telemetryData = [wholeObj];
                        break;
                    } catch (e) { }
                }

                try {
                    telemetryData.push(JSON.parse(line));
                } catch (e) {
                    // Ignore broken JSON lines to allow graceful recovery
                    console.warn("Skipped malformed json line");
                }
            }
        }

        if (telemetryData.length === 0) {
            statusText.innerText = "Failed to parse records";
            return;
        }

        // Setup Scrubber
        scrubber.max = telemetryData.length - 1;
        scrubber.disabled = false;

        // Show controls
        controlsWrapper.style.display = 'flex';
        statusText.innerText = `Loaded ${telemetryData.length} records`;

        // Render first frame
        resetPlayback();

    } catch (error) {
        console.error("Error fetching data:", error);
        statusText.innerText = 'Failed to load history';
    }
};

fetchHistory();
