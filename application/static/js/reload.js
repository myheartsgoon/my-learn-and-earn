 var formHasChanged = false;
 var submitted = false;

$(document).on('change', 'form input, form textarea', function (e) {
    formHasChanged = true;
});

$(document).ready(function () {
    window.onbeforeunload = function (e) {
        if (CKEDITOR.instances.editor.checkDirty()) {
            formHasChanged = true;
        }
        if (formHasChanged && !submitted) {
            var message = "You have not saved your changes.", e = e || window.event;
            if (e) {
                e.returnValue = message;
            }
            return message;
        }
    }
 $("form").submit(function() {
     submitted = true;
     });
});