$(document).ready(function(){
  $('form').submit(function(e){
    $.ajax({
      url: '/check/username/',
      type: 'POST',
      data: {
        'content': $('#id_content').val(),
        'link': $('#id_link').val(),
        'csrfmiddlewaretoken': $('input[name ="csrfmiddlewaretoken"]').val()
      },
      success: function(data){
        var status = data['status']
        var msg = data['msg']

        if(status == 'ok'){
          // Добавление сообщения
          $('#id_content').val('');
          $('#content_span').text('');

          var el = '<li><b>' + msg['content'] + '</b><br><i>' + msg['sent'] + '</i> - ' + msg['sender'] +  ',  ' + msg['msg_hash'] +  ', ' + msg['is_read'] + '</li>';

          $('#all_messages').append(el);
        } else {
          // Показываем ошибку
          $('#content_span').text(msg);
        }
      },
      error: function(data){
        $('#content_span').text('Сервер недоступен, попробуйте отправить сообщение позже.');
      },
    });
    e.preventDefault();
  });

  $("<span style='red' id='content_span'></span>").insertAfter('#id_content');
});