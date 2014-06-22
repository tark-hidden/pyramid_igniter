/**
 * Created by Tark on 16.05.14.
 */

$(document).on('click', '.controls a', function(e) {
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    var span = $(this).parent().find('span');

    $.post($(this).attr('href'), {}, function(res) {
        if(res.error)
            alert(res.error);
        else if(res.rating)
            $(span).html(res.rating);
    });

    return false;
});
