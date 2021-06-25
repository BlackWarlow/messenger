from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from hashlib import sha256

from datetime import datetime

from main.models import *


class AuthForm(forms.Form):
    submit_btn_text = 'Войти'
    
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
        if not self.is_valid():
            self.add_error(None, 'Неверное имя пользователя или пароль')
            return False
        username_clean = self.cleaned_data['username']
        password_clean = self.cleaned_data['password']
        user = authenticate(request, username = username_clean, password = password_clean)
        if user is not None:
            login(request, user)
            return True
        else:
            self.add_error(None, 'Неверное имя пользователя или пароль')
            return False


class RegisterForm(forms.Form):
    submit_btn_text = 'Зарегестрироваться'
    
    username = forms.CharField(
        label='Имя пользователя',
        required=True,
        help_text='Введите имя пользователя',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Пароль',
        required=True,
        help_text='Введите пароль',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Повтор пароля',
        required=True,
        help_text='Повторите пароль',
    )
    email = forms.EmailField(
        label='Почта',
        required=True,
        help_text='Введите почту',
    )
    first_name = forms.CharField(
        label='Имя',
        required=True,
        help_text='Введите имя',
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=True,
        help_text='Введите фамилию',
    )
    birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years = range(datetime.now().year - 100, datetime.now().year),
        ),
        label='Дата рождения',
        required=True,
        help_text='Введите дату рождения',
    )

    def save(self, request):
        if not self.is_valid():
            return False
        username_clean = self.cleaned_data['username']
        password1_clean = self.cleaned_data['password1']
        password2_clean = self.cleaned_data['password2']
        email_clean = self.cleaned_data['email']
        first_name_clean = self.cleaned_data['first_name']
        last_name_clean = self.cleaned_data['last_name']
        birth_clean = self.cleaned_data['birth']
        
        if len(User.objects.filter(username = username_clean)) == 0:
            if password1_clean == password2_clean:
                u = User.objects.create_user(
                    username = username_clean,
                    first_name = first_name_clean,
                    last_name = last_name_clean,
                    email = email_clean,
                    password = password1_clean,
                )
                u.save()

                p = Profile(
                    birth = birth_clean,
                    user = u,
                )
                p.save()

                u_auth = authenticate(request, username = username_clean, password = password1_clean)
                if u_auth is not None:
                    login(request, u_auth)
                    return True
                else:
                    self.add_error(None, 'Проблемы с авторизацией на сайте, попробуйте авторизоваться самостоятельно.')
            else:
                self.add_error('password2', 'Пароли не совпадают')
        else:
            self.add_error('username', 'Пользователь с таким именем уже существует')

        return False


class SearchProfileForm(forms.Form):
    submit_btn_text = 'Искать'

    search_str = forms.CharField(
        label='Строка поиска',
        required=True,
        min_length=3,
    )

    def search(self, request):
        if not self.is_valid():
            return []

        s_str = self.cleaned_data['search_str']
        result = []
        for s in s_str.split():
            for u in list(User.objects.filter(username__icontains=s)):
                if u not in result:
                    result.append(u)

            for u in list(User.objects.filter(first_name__icontains=s)):
                if u not in result:
                    result.append(u)

            for u in list(User.objects.filter(last_name__icontains=s)):
                if u not in result:
                    result.append(u)

        return result

class NewDialogForm(forms.Form):
    submit_btn_text = 'Создать'

    name = forms.CharField(
        max_length = 50,
        label = 'Название диалога',
    )

    def save(self, request, p1, p2):
        if not self.is_valid():
            return False, None
        name_clean = self.cleaned_data['name']
        link = str(datetime.now()) + p1.user.username + p2.user.username

        d = Dialog(
            name=name_clean,
            sender=p1,
            reciever=p2,
            link = sha256(link.encode('UTF-8')).hexdigest()[0:14],
        )
        d.save()
        return True, d