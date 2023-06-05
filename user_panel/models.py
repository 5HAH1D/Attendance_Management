from django.db import models

from django.contrib.auth.models import AbstractUser


class RegisterUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=100, null=False)
    profile_picture = models.ImageField(upload_to='user/profiles', default='user/profiles/profile.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Attendance(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(f"{self.user} ------------ {self.date}")

