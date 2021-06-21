from django import forms

from main.models import *

class AuthForm(forms.Form):
  username = forms.CharField(
    label='Имя пользователя',
    required=True,
  )
  password = forms.CharField(
    widget=forms.PasswordInput(),
    label='Пароль',
    required=True,
  )

  def save(self, request):
      username_clean = cleaned_data['username']
      password_clean = cleaned_data['password']
      user = authenticate(request, username=username_clean, password=password_clean)
      if user is not None:
          login(request, user)
          return True
      else:
          self.add_error(None, 'Неверное мя пользователя или пароль')
      return False