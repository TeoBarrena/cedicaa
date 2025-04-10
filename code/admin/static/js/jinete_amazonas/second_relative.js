const showSecondRelativeCheckbox = document.getElementById('show_second_relative');
const secondRelativeSection = document.getElementById('second_relative_section');

// Función para mostrar u ocultar la sección del segundo familiar
function toggleSecondRelative() {
    if (showSecondRelativeCheckbox.checked) {
        secondRelativeSection.style.display = 'block';
    } else {
        secondRelativeSection.style.display = 'none';
        // Opcional: Limpiar los campos del segundo familiar cuando se oculta
        document.getElementById('relative2_first_name').value = '';
        // Limpiar los demás campos del segundo familiar si los tienes
    }
}

// Añadir un event listener al checkbox para alternar la visibilidad
showSecondRelativeCheckbox.addEventListener('change', toggleSecondRelative);
