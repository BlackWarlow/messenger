from django.contrib import admin

from main.models import *
# Register your models here.

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    search_fields = ('user__username', )
    list_display = ('id', 'user', 'birth', 'status', )
    list_filter = ('birth', )
    fields = [('user', 'birth'), ('status', ), ]


@admin.register(Dialog)
class AdminDialog(admin.ModelAdmin):
    search_fields = ('sender__user__username', 'reciever__user__username', 'name', )
    list_display = ('id', 'name', 'created', 'link', 'reciever', 'sender', )
    list_filter = ('created', )
    fields = [('name', 'link', 'created', ), ('receiver', 'sender', ), ]
    readonly_fields = ('created', )


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    search_fields = ('sender__user__username', 'dialog__receiever__user__username', 'dialog__sender__user__username', )
    list_display = ('id', 'sender', 'sent', 'is_read', 'msg_hash', )
    list_filter = ('is_read', 'sent', )
    fields = [('sent', 'is_read', ), ('msg_hash', 'sender', 'dialog', ), ('content', ), ]
    readonly_fields = ('sent', 'is_read', 'msg_hash', )
