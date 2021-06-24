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
    path('profile/<str:username>/', views.profile_page.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
