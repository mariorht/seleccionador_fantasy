document.addEventListener("DOMContentLoaded", function() {
    const scatterForm = document.getElementById("scatterForm");
    let scatterChart = null; // Variable para almacenar la referencia del gráfico

    scatterForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const xAxis = document.getElementById("x-axis").value;
        const yAxis = document.getElementById("y-axis").value;
        generateScatterPlot(xAxis, yAxis);
    });

    function generateScatterPlot(xAxis, yAxis) {
        const data = playersData.map(player => ({
            x: player[xAxis],
            y: player[yAxis],
            name: player['Player Name'] // Añadir el nombre del jugador a los datos
        }));

        const ctx = document.getElementById('scatterChart').getContext('2d');
        
        // Destruir el gráfico anterior si existe
        if (scatterChart) {
            scatterChart.destroy();
        }

        scatterChart = new Chart(ctx, {
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
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const playerName = context.raw.name;
                                const xValue = context.raw.x;
                                const yValue = context.raw.y;
                                return `${playerName}: (${xValue}, ${yValue})`;
                            }
                        }
                    }
                }
            }
        });
    }
});
