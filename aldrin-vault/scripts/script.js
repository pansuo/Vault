$(document).ready(function() {
    $('#upload_radio_button').click(function() {
        //$('#just_passphrase_form').fadeOut(500).delay(500);
        $('#just_passphrase_form').css('display', 'none');
        //$('#upload_form').fadeIn(1000);
        $('#upload_form').css('display', 'block');
    });
    $('#unlock_radio_button').click(function() {
        //$('#upload_form').fadeOut(500).delay(500);
        $('#upload_form').css('display', 'none');
        //$('#just_passphrase_form').fadeIn(1000);
        $('#just_passphrase_form').css('display', 'block');
    });
});