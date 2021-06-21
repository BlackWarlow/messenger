from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
  status = models.CharField(
    verbose_name = 'Статус',
    max_length = 50,
    null = False,
    blank = False,
    default = '',
  )

  birth = models.DateField(
    verbose_name = 'Дата рождения',
    null = False,
    blank = False,
    auto_now = False,
    auto_now_add = False,
  )

  user = models.ForeignKey(
    to = User,
    verbose_name = 'Ядро пользователя',
    on_delete = models.CASCADE,
    null = False,
    blank = False,
  )

  def __str__(self):
    return '{} - {}'.format(self.user.id, self.user.username)

  class Meta:
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'

class Dialog(models.Model):
  sender = models.ForeignKey(
    to = Profile,
    verbose_name= 'Отправитель',
    related_name='sender_user',
    on_delete=models.CASCADE,
    null = False,
    blank = False,
  )

  reciever = models.ForeignKey(
    to = Profile,
    verbose_name='Получатель',
    related_name='receiver_user',
    on_delete=models.CASCADE,
    null=False,
    blank=False,
  )

  name = models.CharField(
    verbose_name="Имя",
    max_length=50,
    null=False,
    blank=False,
    default='',
  )

  created = models.DateField(
    verbose_name='Дата создания',
    null=False,
    blank=False,
    auto_now=True,
    auto_now_add=False,
  )

  link = models.CharField(
    verbose_name="Ссылка",
    max_length=50,
    null=False,
    blank=False,
    default='',
  )

  def __str__(self):
    return '{} - {} - {}'.format(self.id, self.sender.user.username, self.receiver.user.username)
  class Meta:
    verbose_name = 'Диалог'
    verbose_name_plural = 'Диалоги'

class Message(models.Model):
  dialog = models.ForeignKey(
    to = Dialog,
    on_delete = models.CASCADE,
    verbose_name='Диалог',
    null=False,
    blank=False,
  )# Ссылка на диалог
  content = models.TextField(
    verbose_name="Текст сообщения",
    null=False,
    blank=False,
    default='',
  )  # Текст сообщения
  msg_hash = models.CharField(
    verbose_name="Хэш сообщения",
    max_length=100,
    null=False,
    blank=False,
    default='',
  )  # Хэш сообщения
  sent = models.DateTimeField(
    verbose_name="Время и дата отправки",
    null=False,
    blank=False,
    auto_now=True,
  )  # Время и дата отправки
  is_read = models.BooleanField(
    null=False,
    blank=False,
    default=False,
    verbose_name='',
  )  # Прочитано?
  sender = models.ForeignKey(
    to = Profile,
    on_delete = models.CASCADE,
    verbose_name='Отправитель',
    null=False,
    blank=False,
  ) # Отправитель -> to Profile

  def __str__(self):
    return '{} - {} - {}'.format(self.id, self.sender.user.username, self.msg_hash)

  class Meta:
    verbose_name = 'Беседа'
    verbose_name_plural = 'Беседы'