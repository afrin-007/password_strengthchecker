document.addEventListener("DOMContentLoaded", () => {
    const chartCanvas = document.getElementById("strengthChart");

    if (!chartCanvas) return;

    const scores = JSON.parse(chartCanvas.dataset.scores);
    const counts = JSON.parse(chartCanvas.dataset.counts);

    new Chart(chartCanvas, {
        type: "bar",
        data: {
            labels: scores.map(score => `Score ${score}`),
            datasets: [{
                label: "Password Count",
                data: counts,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "black"
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "black"
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "black"
                    }
                }
            }
        }
    });
});