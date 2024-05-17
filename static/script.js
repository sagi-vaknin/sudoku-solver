$(document).ready(function() {
    $('input[type="text"]').on('input', function() {
        var row = $(this).closest('tr').index();
        var col = $(this).closest('td').index();

        var number = parseInt($(this).val());
        var $inputField = $(this);

        $.ajax({
            url: '/check_input',
            type: 'POST',
            data: {
                row: row,
                col: col,
                number: number
            },
            success: function(response) {
                if (response.result === 'valid') {
                    $('#error-message').text('');
                } else {
                    alert('Invalid input');
                    $inputField.val('');
                    $inputField.focus();
                }
            }
        });
    });
});
