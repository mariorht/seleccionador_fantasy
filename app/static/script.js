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
        field.className = `field ${this.value}`;
    });

    // Añadir opciones de jugadores a cada selector
    $('.player-select').each(function() {
        let select = $(this);
        playersData.forEach(player => {
            let priceInMillions = (player['Precio'] / 1000000).toFixed(2) + 'M€';
            select.append(`<option value="${player['ID']}">${player['Player Name'].replace(/-/g, ' ')} - ${priceInMillions}</option>`);
        });
    });



    // Añadir evento de cambio a cada selector
    $('.player-select').change(function() {
        const playerId = $(this).val();
        const position = $(this).data('position');
        const imageUrl = `/images/${playerId}`;
        $(`.player[data-position="${position}"] .player-image-container`).html(`
            <img src="${imageUrl}" alt="Player Image" class="player-image">
        `);
    });

});
