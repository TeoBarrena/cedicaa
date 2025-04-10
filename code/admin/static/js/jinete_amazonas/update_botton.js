
document.addEventListener('DOMContentLoaded', function() {
    var editButton = document.getElementById('editButton');
    var saveButton = document.getElementById('saveButton');
    var formElements = document.querySelectorAll('input, select, textarea'); // Captura todos los elementos del formulario

    editButton.addEventListener('click', function() {
        // Habilitar los campos para edición
        formElements.forEach(function(element) {
            element.removeAttribute('disabled');
        });

        // Ocultar el botón "Modificar" y mostrar el botón "Guardar"
        editButton.style.display = 'none';
        saveButton.style.display = 'inline-block';

        
    });
});
