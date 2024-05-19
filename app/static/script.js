document.addEventListener("DOMContentLoaded", function() {
    const formationSelector = document.getElementById("formation");
    const field = document.getElementById("field");

    formationSelector.addEventListener("change", function() {
        field.className = `field ${this.value}`;
    });
});


$(document).ready(function() {
    $('#playerTable').DataTable({
        "order": [[ 3, 'desc' ]] // Ordenar por la tercera columna (Rating) en orden descendente
    });
});