/**
 * Created by Tark on 16.05.14.
 */

function quote_hide(el) {
    el.hide('slow');
    if(--quote_count == 0)
        window.location.reload();
}

$('.controls')
    .on('click', '.approve', function(e) {
        var el = $(this).parent().parent();
        var data = {'action': 'approve'}
        var quote_id = $(this).attr('id');
        var div = $('#quote_body' + quote_id);
        if(div.length)
            data['body'] = div.val();

        $.post($(this).attr('href') + '/' + csrf, data, function(res) { quote_hide(el); });
        return false;})
    .on('click', '.edit', function(e) {
        var quote_id = $(this).attr('id');
        var div = $('#quote-' + quote_id);
        if(!div.length)
            return false;
        var height = div.outerHeight();
        var quote_data = div.html().replace(/<\/?p>/g, '').replace(/<br\s?\/?>\n/g, '\n');

        var ta = $("<textarea class='quote' id='quote_body" + quote_id + "'>");

        div.replaceWith(ta);
        ta.css({'height': height, 'width': '100%'});
        ta.html(quote_data);
        ta.focus();
        return false;
    })
    .on('click', '.refuse', function(e) {
        var el = $(this).parent().parent();
        $.post($(this).attr('href') + '/' + csrf, {'action': 'refuse'}, function(res) { quote_hide(el); });
        return false;})
    .on('click', '.delete', function(e) {
        var el = $(this).parent().parent();
        $.post($(this).attr('href') + '/' + csrf, {'action': 'delete'}, function(res) { quote_hide(el); });
        return false;});
