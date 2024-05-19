document.addEventListener("DOMContentLoaded", function() {
    const formationSelector = document.getElementById("formation");
    const field = document.getElementById("field");

    formationSelector.addEventListener("change", function() {
        field.className = `field ${this.value}`;
    });
});
