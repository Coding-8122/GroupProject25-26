// Week 1: Chart.js setup
console.log("charts.js loaded");

function renderWeightOverTime() {
  const el = document.getElementById("weightOverTimeChart");
  if (!el) return;
  new Chart(el, {
    type: "line",
    data: {
      labels: ["W1", "W2", "W3"],
      datasets: [{ label: "Weight", data: [80, 79.5, 79] }]
    }
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
    }
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
    }
  });
  const noData = document.getElementById("muscleNoData");
  if (noData) noData.style.display = "none";
}
