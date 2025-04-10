function blockUser(userId) {
    document.getElementById('action').value = 'block';
    document.getElementById('user_id').value = userId;

    // Obtener la página actual de los parámetros de la URL
    const currentPage = new URLSearchParams(window.location.search).get('page') || 1;
    const inputPage = document.createElement('input');
    inputPage.type = 'hidden';
    inputPage.name = 'page';
    inputPage.value = currentPage;
    document.forms[0].appendChild(inputPage);

    document.forms[0].submit();
}

function unblockUser(userId) {
    document.getElementById('action').value = 'unblock';
    document.getElementById('user_id').value = userId;

    // Obtener la página actual de los parámetros de la URL
    const currentPage = new URLSearchParams(window.location.search).get('page') || 1;
    const inputPage = document.createElement('input');
    inputPage.type = 'hidden';
    inputPage.name = 'page';
    inputPage.value = currentPage;
    document.forms[0].appendChild(inputPage);

    document.forms[0].submit();
}

document.addEventListener('DOMContentLoaded', function () {
    var changeRoleModal = document.getElementById('changeRoleModal');
    changeRoleModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;  // Botón que activa el modal
        var userId = button.getAttribute('data-userid');  // Extraer el ID del usuario
        var currentRole = button.getAttribute('data-currentrole');  // Extraer el rol actual
        
        var modalUserId = changeRoleModal.querySelector('#modalUserId');
        var modalNewRole = changeRoleModal.querySelector('#newRole');

        // Establecer el ID de usuario en el modal
        modalUserId.value = userId;

        // Establecer el rol actual en el desplegable del modal
        modalNewRole.value = currentRole || 'None';  // Asegúrate de que 'None' sea un valor válido
    });
});