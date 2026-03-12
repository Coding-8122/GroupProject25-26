// charts.js - Full Updated Version
console.log("chart.js loaded");

// Reusable options to ensure the chart fits the 280px container
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // MANDATORY: Allows chart to fill the .chart-container height
  scales: {
    y: {
      beginAtZero: true
    }
  }
};

function renderWeightOverTime() {
  const el = document.getElementById("weightOverTimeChart");
  if (!el) return;
  new Chart(el, {
    type: "line",
    data: {
      labels: ["W1", "W2", "W3"],
      datasets: [{ 
        label: "Weight (kg)", 
        data: [80, 79.5, 79],
        borderColor: '#22c55e',
        tension: 0.1
      }]
    },
    options: chartOptions
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
      datasets: [{ 
        label: "Body Fat %", 
        data: [18, 17.8, 17.5],
        borderColor: '#f59e0b',
        tension: 0.1
      }]
    },
    options: chartOptions
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
      datasets: [{ 
        label: "Weekly Volume", 
        data: [12, 16, 20],
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: chartOptions
  });
  const noData = document.getElementById("muscleNoData");
  if (noData) noData.style.display = "none";
}

function renderWeeklyTrainingVolume() {
  const canvas = document.getElementById("weeklyTrainingVolumeChart");
  if (!canvas) return;

  const labels = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"];
  const data = [10, 14, 9, 18, 16]; 

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
          borderColor: '#3e95cd',
          backgroundColor: 'rgba(62, 149, 205, 0.1)',
          fill: true,
          tension: 0.3
        }],
    },
    options: chartOptions
  });
  
  const noData = document.getElementById("weeklyTrainingVolumeNoData");
  if (noData) noData.style.display = "none";
}

// Initialize all charts when the DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  renderWeightOverTime();
  renderBodyFatOverTime();
  renderMuscleVolume();
  renderWeeklyTrainingVolume();
});