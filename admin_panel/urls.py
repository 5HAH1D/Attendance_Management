from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user_record', views.user_record_management, name='user_record_management'),
    path('attendance_management', views.attendance_management, name='attendance_management'),
    path('user_attendance_report', views.user_attendance_report, name='user_attendance_report'),
    path('leave_requests', views.leave_requests, name='leave_requests'),
    path('leave_approval/<int:leave_id>', views.leave_approval, name='leave_approval'),
    path('leave_reject/<int:leave_id>', views.leave_reject, name='leave_reject'),
    path('system_report', views.system_report, name='system_report'),
    path('grading_system', views.grading_system, name='grading_system'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('logout', views.logout_admin, name='logout_admin'),
]
