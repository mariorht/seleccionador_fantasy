document.addEventListener("DOMContentLoaded", function() {
    const scatterForm = document.getElementById("scatterForm");

    scatterForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const xAxis = document.getElementById("x-axis").value;
        const yAxis = document.getElementById("y-axis").value;
        generateScatterPlot(xAxis, yAxis);
    });

    function generateScatterPlot(xAxis, yAxis) {
        const data = playersData.map(player => ({
            x: player[xAxis],
            y: player[yAxis]
        }));

        const ctx = document.getElementById('scatterChart').getContext('2d');
        new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: `${xAxis} vs ${yAxis}`,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: xAxis
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: yAxis
                        }
                    }
                }
            }
        });
    }
});
