document.addEventListener('DOMContentLoaded', function() {
    var deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function(event) {
            // Obtén el botón que activó el modal
            var button = event.relatedTarget;
            // Extrae el valor de `data-url`
            var url = button.getAttribute('data-url');
            // Actualiza la acción del formulario con la URL obtenida
            var deleteForm = document.getElementById('deleteForm');
            deleteForm.action = url;
        });
    } else {
        console.error('El modal de eliminación no se encontró en el DOM.');
    }
});
