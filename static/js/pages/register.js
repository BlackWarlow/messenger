let can_send = false;

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
  clearTimeout (timer);
  timer = setTimeout(callback, ms);
 };
})();

function checkUsername(){
$.ajax({
  url: '/check/username/',
  type: 'GET',
    data: {
        'username': $('#id_username').val(),
        'csrfmiddlewaretoken': $('input[name ="csrfmiddlewaretoken"]').val()
    },
    success: function(data){
      var status = data['status'];
      var msg = data['msg']

      if (status == 'ok'){
        // Имя пользователя свободно - можно отправлять форму
        $('#username_span').css({'color': 'green'});
        $('#username_span').text('Имя пользователя свободно');
        can_send = true;
      } else {
        // Тут ошибка - значит не допустить отправки формы
        $('#username_span').css({'color': 'red'});
        $('#username_span').text(msg);
        can_send = false;
      }
    },
    error: function(data){
      $('#username_span').css({'color': 'red'});
      $('#username_span').text('На сервере произошла ошибка, попробуйте зарегестрироваться позже.');
    },
});
}

$( document ).ready(function(){
  $('#id_username').keyup(
    function() {
    delay(function(){
      checkUsername();
      }, 1000 );
    }
  );

  $('#id_password2').keyup(
    function() {
    delay(function(){
      if ($('#id_password2').val() !=  $('#id_password1').val()){
        // Пароли должны совпадать
        $('#password_span').css({'color': 'red'});
        $('#password_span').text('Пароли должны совпадать');
        password_ok = false;
      } else {
        $('#password_span').text('');
        password_ok = true;
      }
      }, 1000 );
    }
  );
  $("<span style='color: red' id='username_span'></span>").insertAfter('#id_username');
  $("<span style='color: red' id='password_span'></span>").insertAfter('#id_password2');

  $("form").submit(function(e){
    if (user_ok && password_ok){
      e.preventDefault();
    }
  });
});