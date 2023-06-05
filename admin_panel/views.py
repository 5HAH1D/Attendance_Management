from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from admin_panel.models import LeaveRequest
from user_panel.models import *


def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('admin_login')
        else:
            return redirect('admin_login')
    else:
        return render(request, 'admin_p/login.html')


@login_required(login_url='admin_login')
def dashboard(request):
    user_count = RegisterUser.objects.filter(is_superuser=False).count()
    admins = RegisterUser.objects.filter(is_superuser=True).count()
    leaves = LeaveRequest.objects.filter(status='PENDING').count()

    today = timezone.now().date()
    start_date = today - timezone.timedelta(days=2)
    end_date = today
    recent_users = RegisterUser.objects.filter(
        is_superuser=False,
        date_joined__date__range=[start_date, end_date]
    ).count()

    context = {'user_count': user_count,
               'admins': admins,
               'leaves': leaves,
               'recent_users': recent_users}

    return render(request, 'admin_p/dashboard.html', context=context)


@login_required(login_url='admin_login')
def user_record_management(request):
    users = RegisterUser.objects.filter(is_superuser=False)
    context = {'users': users}
    return render(request, 'admin_p/users_record.html', context=context)


@login_required(login_url='admin_login')
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(RegisterUser, username=username)
        user.delete()
        return redirect('user_record_management')


@login_required(login_url='admin_login')
def attendance_management(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        action = request.POST.get('action')

        user = get_object_or_404(RegisterUser, id=user_id)

        if action == 'add':
            attendance_record = Attendance(user=user, date=date, status=status)
            attendance_record.save()

        elif action == 'edit':
            parsed_date = timezone.datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
            attendance_record = Attendance.objects.get(user=user, date=parsed_date)
            attendance_record.status = status
            attendance_record.save()

        elif action == 'delete':
            parsed_date = timezone.datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
            attendance_record = Attendance.objects.get(user=user, date=parsed_date)
            attendance_record.delete()

        return redirect('attendance_management')

    else:
        attendance_records = Attendance.objects.all().order_by('-date')
        users = RegisterUser.objects.filter(is_superuser=False)

        context = {
            'attendance_records': attendance_records,
            'users': users,
        }

        return render(request, 'admin_p/attendance_management.html', context)


@login_required(login_url='admin_login')
def user_attendance_report(request):
    if request.method == 'POST':
        user = request.POST['username']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        username = RegisterUser.objects.filter(username=user).first()

        attendance_records = Attendance.objects.filter(user=username, date__range=[from_date, to_date])

        context = {
            'user': username,
            'attendance_records': attendance_records,
            'from_date': from_date,
            'to_date': to_date,
        }
        return render(request, 'admin_p/user_attendance_report.html', context)

    else:
        users = RegisterUser.objects.filter(is_superuser=False)
        context = {'users': users}
        return render(request, 'admin_p/generate_report.html', context)


@login_required(login_url='admin_login')
def leave_requests(request):
    leaves = LeaveRequest.objects.filter(status='PENDING').order_by('-date')
    return render(request, 'admin_p/leave_requests.html', {'leaves': leaves})


@login_required(login_url='admin_login')
def leave_approval(leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    if leave.status == 'PENDING':
        leave.status = 'APPROVED'
        leave.save()
        attendance = Attendance.objects.filter(user=leave.user, date=leave.date)
        print(attendance)
        if attendance:
            attendance.status = 'Leave'
            attendance.save()
    return redirect('leave_requests')


@login_required(login_url='admin_login')
def leave_reject(leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    if leave.status == 'PENDING':
        leave.status = 'REJECTED'
        leave.save()
        attendance = Attendance.objects.filter(user=leave.user, date=leave.date).first()
        if attendance:
            attendance.status = 'Absent'
            attendance.save()
    return redirect('leave_requests')


@login_required(login_url='admin_login')
def system_report(request):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date]).order_by('-date')

        context = {
            'attendance_records': attendance_records,
            'from_date': from_date,
            'to_date': to_date,
        }
        return render(request, 'admin_p/system_report.html', context)
    else:
        return render(request, 'admin_p/generate_system_report.html')


@login_required(login_url='admin_login')
def grading_system(request):
    users = RegisterUser.objects.filter(is_superuser=False)
    users_data = []

    for user in users:
        presents = Attendance.objects.filter(user=user, status='Present').count()
        absents = Attendance.objects.filter(user=user, status='Absent').count()
        leaves = Attendance.objects.filter(user=user, status='Leave').count()
        total_days = presents + absents + leaves

        if total_days == 0:
            attendance_percentage = 0
        else:
            attendance_percentage = int((presents / total_days) * 100)

        if attendance_percentage >= 80:
            grade = 'A'
        elif 70 <= attendance_percentage < 80:
            grade = 'B'
        elif 50 <= attendance_percentage < 70:
            grade = 'C'
        elif 35 <= attendance_percentage < 50:
            grade = 'D'
        else:
            grade = 'F'
        users_data.append({'user': user, 'presents': presents, 'absents': absents,
                           'leaves': leaves, 'percentage': attendance_percentage, 'grade': grade})

    return render(request, 'admin_p/gradings.html', {'users_data': users_data})


@login_required(login_url='admin_login')
def logout_admin(request):
    logout(request)
    return redirect('admin_login_page')
