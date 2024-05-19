document.addEventListener("DOMContentLoaded", function() {
    const formationSelector = document.getElementById("formation");
    const field = document.getElementById("field");

    formationSelector.addEventListener("change", function() {
        field.className = `field ${this.value}`;
    });
});


$(document).ready(function() {
    $('#playerTable').DataTable({
        "order": [[ 3, "desc" ]] // Ordenar por la tercera columna (Rating) en orden descendente
    });

   
    // Añadir evento de clic a cada jugador en el campo
    $('.player').click(function() {
        if ($(this).find('.player-select').length === 0) {
            const position = $(this).data('position');
            let select = `<select class="player-select" data-position="${position}">
                            <option value="">Select player</option>`;
            playersData.forEach(player => {
                select += `<option value="${player['Player Name']}">${player['Player Name'].replace(/-/g, ' ')}</option>`;
            });
            select += `</select>`;
            $(this).html(select);

            // Añadir evento de cambio al select
            $('.player-select').change(function() {
                const selectedPlayer = $(this).val();
                const position = $(this).data('position');
                $(`.player[data-position="${position}"]`).html(selectedPlayer);
            });
        }
    });
});

