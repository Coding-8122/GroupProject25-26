const CHART_THEME = {
    weight: '#22c55e',
    fat: '#f59e0b',
    volume: '#3e95cd'
};

const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: true, position: 'top' }
    }
};

async function initDynamicChart(endpoint, elementId, type, label, color, dataKey = 'data') {
    const canvas = document.getElementById(elementId);
    if (!canvas) return;

    const noDataMsg = document.getElementById(`${elementId}NoData`);

    try {
        const response = await fetch(endpoint);
        const result = await response.json();

        // Check if data exists and is not empty
        if (!result[dataKey] || result[dataKey].length === 0) {
            if (noDataMsg) noDataMsg.style.display = 'block';
            canvas.style.display = 'none'; // Hide empty canvas
            return;
        }

        // We have data, render the chart
        if (noDataMsg) noDataMsg.style.display = 'none';
        canvas.style.display = 'block';

        new Chart(canvas, {
            type: type,
            data: {
                labels: result.labels,
                datasets: [{
                    label: label,
                    data: result[dataKey],
                    borderColor: color,
                    backgroundColor: type === 'bar' ? 'rgba(54, 162, 235, 0.7)' : 'transparent',
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: baseOptions
        });
    } catch (error) {
        console.error(`Error fetching chart data for ${elementId}:`, error);
        if (noDataMsg) noDataMsg.style.display = 'block';
    }
}

// Global render functions called by the HTML templates
window.renderWeightOverTime = function() {
    initDynamicChart('/api/stats/weight', 'weightOverTimeChart', 'line', 'Weight (kg)', CHART_THEME.weight, 'weight');
};

window.renderBodyFatOverTime = function() {
    initDynamicChart('/api/stats/weight', 'bodyFatOverTimeChart', 'line', 'Body Fat %', CHART_THEME.fat, 'fat');
};

window.renderMuscleVolume = function() {
    initDynamicChart('/api/stats/volume', 'muscleVolumeChart', 'bar', 'Total Volume (kg)', CHART_THEME.volume, 'data');
};