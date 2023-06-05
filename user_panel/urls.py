from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('register_user', views.register_user, name='register_user'),
    path('dashboard', views.user_dashboard, name='user_dashboard'),
    path('change_profile_picture', views.change_profile_picture, name='change_picture'),
    path('mark_attendance', views.mark_attendance, name='mark_attendance'),
    path('request_leave', views.request_leave, name='request_leave'),
    path('view_attendance', views.view_attendance, name='view_attendance'),
    path('logout_user', views.logout_user, name='logout_user'),
]
