"""
project URL Configuration
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

# Renaming django admin title
admin.site.site_header = 'Панель администрации'
admin.site.site_title = 'Messenger'
admin.site.index_title = 'Модерация сайта'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page.as_view(), name='index_page'),
    path('login/', views.login_page.as_view(), name='login_page'),
    path('logout/', views.logout_page.as_view(), name='logout_page'),
    path('register/', views.register_page.as_view(), name='register_page'),
    path('profile/', views.profile_page.as_view(), name='my_profile_page'),
    path('profile/<str:username>/', views.profile_page.as_view(), name='user_profile'),
    path('search/profile/<str:search_str>/', views.profile_search.as_view(), name='user_profile_search'),
    path('search/profile/', views.profile_search.as_view(), name='profile_search_page'),
    path('dialogs/', views.all_dialogs.as_view(), name='my_dialogs'),
    path('new/dialog/<str:username>/', views.create_dialog.as_view(), name='create_dialog_page'),
    path('new/dialog/', views.create_dialog.as_view(),name='create_dialog_page'),
    path('dialog/<str:link>/', views.dialog_page.as_view(), name='dialog'),
    path('dialog/', views.dialog_page.as_view(), name='dialog_error'),
    path('check/username/', views.check_username, name='check_username_ajax'),
    path('message/', views.create_message, name='create_massage_ajax'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
