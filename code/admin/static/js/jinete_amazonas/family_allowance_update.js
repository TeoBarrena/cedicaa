document.addEventListener('DOMContentLoaded', function() {
    var familyAllowanceSection = document.getElementById('family_allowance_section');
    var hasAllowances = "{{ rider.allowance_type }}" !== ""; // Check if allowance_type has any value

    if (hasAllowances) {
        familyAllowanceSection.style.display = "block";
    } else {
        familyAllowanceSection.style.display = "none";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var disabilityTypes = document.getElementsByName('disability_type');
    var riderDisabilityTypes = "{{ rider.disability_type }}".split(','); // Asegúrate de que el campo esté separado por comas en el backend si es una lista.

    // Si el jinete tiene algún tipo de discapacidad, marcamos las casillas correspondientes
    if (riderDisabilityTypes.length > 0 && riderDisabilityTypes[0] !== "") {
        disabilityTypes.forEach(function(checkbox) {
            if (riderDisabilityTypes.includes(checkbox.value)) {
                checkbox.checked = true;
                checkbox.closest('.form-check').style.display = "block";  // Mostrar la opción
            } else {
                checkbox.checked = false;
                checkbox.closest('.form-check').style.display = "none";  // Ocultar la opción si no corresponde
            }
        });
    }
});
