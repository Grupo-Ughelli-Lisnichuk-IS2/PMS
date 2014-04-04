$('tr').click(function() {
    $('tr').removeClass('selected');
    $(this).addClass('selected');

    var td = $(this).children('td');
    for (var i = 0; i < td.length; ++i) {
        alert(i + ': ' + td[i].innerText);
    }
});
