import os
from django.db import IntegrityError
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone

from admin_panel.models import LeaveRequest
from .models import Attendance

User = get_user_model()


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('user_login_page')
            else:
                login(request, user)
                return redirect('user_dashboard')
        else:
            return redirect('login_user')
    else:
        return render(request, 'user/login.html')


def register_user(request):
    if request.method == 'POST':
        name = request.POST['user_name']
        email = request.POST['user_email']
        password = request.POST['user_password']
        try:
            new_user = User.objects.create(username=name, email=email)
            new_user.set_password(password)
            new_user.save()
            user = User.objects.get(username=name)
            attendance = Attendance(user=user, date=timezone.now().date(), status="Present")
            attendance.save()
            return HttpResponse("User Registered Successfully")
        except IntegrityError:
            return HttpResponse("ERROR! Email already exists.")
    else:
        return render(request, 'user/login.html')


@login_required(login_url='login_user')
def user_dashboard(request):
    profile = request.user.profile_picture.url
    return render(request, 'user/dashboard.html', context={'profile': profile})


@login_required(login_url='login_user')
def change_profile_picture(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        user = request.user
        if profile_picture:
            if user.profile_picture and os.path.isfile(user.profile_picture.path) and \
                    os.path.basename(user.profile_picture.path) != 'profile.png':
                os.remove(user.profile_picture.path)

            user.profile_picture = profile_picture
            user.save()
            return redirect('user_dashboard')

        else:
            return redirect('user_dashboard')
    else:
        return render(request, 'user/select_profile.html')


@login_required(login_url='login_user')
def mark_attendance(request):
    if request.method == 'POST':
        user = request.user
        today = timezone.now().date()

        if Attendance.objects.filter(user=user, date=today).exists():
            return HttpResponse("Attendance has already been marked for today!")

        attendance = Attendance(user=user, date=today, status="Present")
        attendance.save()
        return HttpResponse("Attendance has been marked successfully!")


@login_required(login_url='login_user')
def request_leave(request):
    if request.method == 'POST':
        date = timezone.now().date()
        attendance = Attendance.objects.filter(user=request.user, date=date).first()
        if attendance and attendance.status == "Present":
            return HttpResponse("Attendance has already been marked as PRESENT!")
        if not attendance:
            leave_request = LeaveRequest(user=request.user, date=date)
            leave_request.save()
            attendance_ = Attendance(user=request.user, date=date, status="Leave Pending")
            attendance_.save()
            return HttpResponse("Leave request has been submitted successfully.")
        if attendance and attendance.status == "Leave Pending":
            return HttpResponse("Leave Request has already been Sent to Admin!")
    return redirect('user_dashboard')


@login_required(login_url='login_user')
def view_attendance(request):
    user = request.user
    attendance_record = Attendance.objects.filter(user=user).order_by('-date')
    context = {'attendance_record': attendance_record}

    return render(request, 'user/view_attendance.html', context=context)


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')
