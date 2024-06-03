document.addEventListener("DOMContentLoaded", function() {
    const scatterForm = document.getElementById("scatterForm");
    let scatterChart = null; // Variable para almacenar la referencia del gráfico

    // Definir una paleta de 20 colores
    const colorPalette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
    ];

    // Mapa para almacenar los colores asignados a cada equipo
    const teamColors = {};
    let colorIndex = 0;

    scatterForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const xAxis = document.getElementById("x-axis").value;
        const yAxis = document.getElementById("y-axis").value;
        generateScatterPlot(xAxis, yAxis);
    });

    function generateScatterPlot(xAxis, yAxis) {
        const data = playersData.map(player => {
            // Asignar un color si el equipo aún no tiene uno
            if (!teamColors[player['Team']]) {
                teamColors[player['Team']] = colorPalette[colorIndex % colorPalette.length];
                colorIndex++;
            }
            return {
                x: player[xAxis],
                y: player[yAxis],
                name: player['Player Name'],
                team: player['Team'],
                color: teamColors[player['Team']]
            };
        });

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
                    backgroundColor: data.map(d => d.color),
                    borderColor: data.map(d => d.color),
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
                                const team = context.raw.team;
                                const xValue = context.raw.x;
                                const yValue = context.raw.y;
                                return `${playerName} (${team}): (${xValue}, ${yValue})`;
                            }
                        }
                    }
                }
            }
        });
    }
});
