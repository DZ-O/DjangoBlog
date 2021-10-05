function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            //   Does   this   cookie   string   begin   with   the   name   we   want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    //   these   HTTP   methods   do   not   require   CSRF   protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});




$('#like_btn').click(function () {
    $.ajax({
        url: '/like/',
        type: 'post',
        data: {
            'like_state': $('#like_state').text(),
            'article_id': $('#article_id').val(),

        },
        success: function (args) {

            if (args.error == 200) {
                $('#like_count').text(args.likecount)
                $('#like_count').css('color','red')
            } else {
                $('#like_count').text(args.likecount)
                $('#like_count').css('color','black')
            }
        }
    })
})