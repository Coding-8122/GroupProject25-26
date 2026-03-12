// Week 1 & 2: Chart.js logic
console.log("chart.js loaded");

// Reusable options to keep things tidy
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
};

function renderWeightOverTime() {
  const el = document.getElementById("weightOverTimeChart");
  if (!el) return;
  new Chart(el, {
    type: "line",
    data: {
      labels: ["W1", "W2", "W3"],
      datasets: [{ label: "Weight", data: [80, 79.5, 79] }]
    },
    options: chartOptions // Added this!
  });
  const noData = document.getElementById("weightNoData");
  if (noData) noData.style.display = "none";
}

function renderBodyFatOverTime() {
  const el = document.getElementById("bodyFatOverTimeChart");
  if (!el) return;
  new Chart(el, {
    type: "line",
    data: {
      labels: ["W1", "W2", "W3"],
      datasets: [{ label: "Body Fat %", data: [18, 17.8, 17.5] }]
    },
    options: chartOptions // Added this!
  });
  const noData = document.getElementById("bodyFatNoData");
  if (noData) noData.style.display = "none";
}

function renderMuscleVolume() {
  const el = document.getElementById("muscleVolumeChart");
  if (!el) return;
  new Chart(el, {
    type: "bar",
    data: {
      labels: ["Chest", "Back", "Legs"],
      datasets: [{ label: "Weekly Volume", data: [12, 16, 20] }]
    },
    options: chartOptions // Added this!
  });
  const noData = document.getElementById("muscleNoData");
  if (noData) noData.style.display = "none";
}

function renderWeeklyTrainingVolume() {
  const canvas = document.getElementById("weeklyTrainingVolumeChart");
  const noData = document.getElementById("weeklyTrainingVolumeNoData");
  if (!canvas) return;

  // Syncing labels and data count to stop the "off-screen" line
  const labels = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"];
  const data = [10, 14, 9, 18, 16]; 

  if (!data || data.length === 0) {
    if (noData) noData.style.display = "block";
    canvas.style.display = "none";
    return;
  }
  if (noData) noData.style.display = "none";

  if (typeof Chart === "undefined") {
    console.warn("Chart.js not loaded");
    return;
  }

  new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
          label: "Training volume",
          data,
          borderColor: '#3e95cd', // Pro-tip: adding a color makes it pop
          fill: false
        }],
    },
    options: chartOptions // Using the shared options
  });
}