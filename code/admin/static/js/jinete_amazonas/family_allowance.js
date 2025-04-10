const familyAllowanceYes = document.getElementById('family_allowance_yes');
const familyAllowanceNo = document.getElementById('family_allowance_no');
const familyAllowanceSection = document.getElementById('family_allowance_section');

// Mostrar u ocultar la sección de pensiones familiares según la selección
function toggleFamilyAllowanceSection() {
    if (familyAllowanceYes.checked) {
        familyAllowanceSection.style.display = 'block';
    } else {
        familyAllowanceSection.style.display = 'none';
    }
}

familyAllowanceYes.addEventListener('change', toggleFamilyAllowanceSection);
familyAllowanceNo.addEventListener('change', toggleFamilyAllowanceSection);

// Inicialización (para asegurar que las secciones estén ocultas al principio)
toggleDiagnosisSection();
toggleFamilyAllowanceSection();
