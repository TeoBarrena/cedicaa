document.addEventListener('DOMContentLoaded', function () {
    var changeStateModal = document.getElementById('changeStateModal'); // Modal para cambiar estado

    changeStateModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Botón que activó el modal
        var messageId = button.getAttribute('data-message-id'); // ID del mensaje

        // Referencias al formulario y a los campos dentro del modal
        var form = changeStateModal.querySelector('form');
        var hiddenMessageId = changeStateModal.querySelector('#modalMessageId');
        var hiddenAction = changeStateModal.querySelector('#modalAction');

        // Establecer la acción y el ID en el formulario
        hiddenMessageId.value = messageId;
        hiddenAction.value = "change_state"; // Acción específica para cambiar el estado
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Modal para editar comentario
    var editCommentModal = document.getElementById("editCommentModal");
    var commentMessageIdInput = document.getElementById("commentMessageId");
    var commentTextarea = document.getElementById("comment");

    // Configurar evento al mostrar el modal
    editCommentModal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget; // Botón que activó el modal
        var messageId = button.getAttribute("data-message-id");
        var comment = button.getAttribute("data-message-comment");

        // Establecer valores en el formulario del modal
        commentMessageIdInput.value = messageId;
        commentTextarea.value = comment ? comment : ""; 
    });
});