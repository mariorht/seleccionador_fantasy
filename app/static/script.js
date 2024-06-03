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
                select += `<option value="${player['ID']}">${player['Player Name'].replace(/-/g, ' ')}</option>`;
            });
            select += `</select>`;
            $(this).find('.player-select-placeholder').html(select);

            // Añadir evento de cambio al select
            $('.player-select').change(function() {
                const playerId = $(this).val();
                const position = $(this).data('position');
                const playerName = $(this).find('option:selected').text();
                const imageUrl = `/images/${playerId}`;
                $(`.player[data-position="${position}"]`).html(`
                    <div class="player-image-container">
                        <img src="${imageUrl}" alt="Player Image" class="player-image">
                    </div>
                    <div class="player-name">${playerName}</div>
                `);
            }).focus();
        }
    });
});
