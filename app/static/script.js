document.addEventListener("DOMContentLoaded", function() {
    const formationSelector = document.getElementById("formation");
    const field = document.getElementById("field");

    formationSelector.addEventListener("change", function() {
        field.className = `field ${this.value}`;
    });
});



document.addEventListener("DOMContentLoaded", function() {

    // Inicializar DataTables
    $('#playerTable').DataTable({
        "order": [[ 3, "desc" ]] // Ordenar por la tercera columna (Rating) en orden descendente
    });


    const formationSelector = document.getElementById("formation");
    const field = document.getElementById("field");


    formationSelector.addEventListener("change", function() {
        const selectedFormation = this.value;
        field.className = `field ${selectedFormation}`;
        updatePlayerOptions(selectedFormation);
    });


    formationSelector.addEventListener("change", function() {
        field.className = `field ${this.value}`;
    });

    // Inicializar las opciones de jugadores para la formación predeterminada
    updatePlayerOptions('formation-4-3-3');


    // Añadir evento de cambio a cada selector
    $('.player-select').change(function() {
        const playerId = $(this).val();
        const position = $(this).data('position');
        const playerName = $(this).find('option:selected').text();
        const imageUrl = `/images/${playerId}`;
        $(`.player[data-position="${position}"] .player-image-container`).html(`
            <img src="${imageUrl}" alt="Player Image" class="player-image">
        `);
        $(`.player[data-position="${position}"] .player-name`).text(playerName);
    });

});




const formationMappings = {
    'formation-4-3-3': {
        1: 'Portero',
        2: 'Defensa',
        3: 'Defensa',
        4: 'Defensa',
        5: 'Defensa',
        6: 'Centrocampista',
        7: 'Centrocampista',
        8: 'Centrocampista',
        9: 'Delantero',
        10: 'Delantero',
        11: 'Delantero'
    },
    'formation-3-4-3': {
        1: 'Portero',
        2: 'Defensa',
        3: 'Defensa',
        4: 'Defensa',
        5: 'Centrocampista',
        6: 'Centrocampista',
        7: 'Centrocampista',
        8: 'Centrocampista',
        9: 'Delantero',
        10: 'Delantero',
        11: 'Delantero'
    }
};

// Función para actualizar las opciones de los selectores
function updatePlayerOptions(formation) {
    const positionMapping = formationMappings[formation];

    $('.player-select').each(function() {
        let select = $(this);
        const position = select.data('position');
        const requiredPosition = positionMapping[position];
        select.empty(); // Vaciar las opciones actuales
        select.append(`<option value="">Select player</option>`);

        playersData.forEach(player => {
            if (player['Posición'] === requiredPosition) {
                let priceInMillions = (player['Precio'] / 1000000).toFixed(2) + 'M€';
                select.append(`<option value="${player['ID']}">${player['Player Name'].replace(/-/g, ' ')} - ${priceInMillions}</option>`);
            }
        });
    });
}