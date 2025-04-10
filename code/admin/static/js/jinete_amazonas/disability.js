
// Obtener los elementos
const hasDisabilityYes = document.getElementById('has_disability_certificate_yes');
const hasDisabilityNo = document.getElementById('has_disability_certificate_no');
const diagnosisSection = document.getElementById('diagnosis_section');
const otherDiagnosisSection = document.getElementById('other_diagnosis_section');
const diagnosisSelect = document.getElementById('diagnosis');

// Mostrar u ocultar la sección de diagnóstico según la selección
function toggleDiagnosisSection() {
    if (hasDisabilityYes.checked) {
        diagnosisSection.style.display = 'block';
    } else {
        diagnosisSection.style.display = 'none';
        otherDiagnosisSection.style.display = 'none'; // Ocultar "OTRO" también
        diagnosisSelect.value = ''; // Resetear el valor de diagnosis
    }
}

// Mostrar u ocultar el campo "OTRO" si se selecciona "OTRO" en el diagnóstico
function toggleOtherDiagnosis() {
    if (diagnosisSelect.value === 'OTRO') {
        otherDiagnosisSection.style.display = 'block';
    } else {
        otherDiagnosisSection.style.display = 'none';
        document.getElementById('other_diagnosis').value = ''; // Resetear el campo de texto
    }
}

// Añadir eventos de cambio a los radio buttons y select
hasDisabilityYes.addEventListener('change', toggleDiagnosisSection);
hasDisabilityNo.addEventListener('change', toggleDiagnosisSection);
diagnosisSelect.addEventListener('change', toggleOtherDiagnosis);

// Inicialización (para asegurar que la sección de diagnóstico esté oculta al principio)
toggleDiagnosisSection();
