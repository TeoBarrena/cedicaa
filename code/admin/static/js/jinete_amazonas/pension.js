const pensionYes = document.getElementById('pension_yes');
const pensionNo = document.getElementById('pension_no');
const pensionSection = document.getElementById('pension_section');

// Mostrar u ocultar la sección de pensiones familiares según la selección
function togglePensionSection() {
    if (pensionYes.checked) {
        pensionSection.style.display = 'block';
    } else {
        pensionSection.style.display = 'none';
    }
}

pensionYes.addEventListener('change', togglePensionSection);
pensionNo.addEventListener('change', togglePensionSection);

togglePensionSection();
