$(document).ready(function() {
    $('button#go-back').on('click', function(e){
        e.preventDefault();
        window.history.back();
    });
});