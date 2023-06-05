from django.db import models

from user_panel.models import RegisterUser


class LeaveRequest(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    date = models.DateField()
    leave_status = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=leave_status, default='PENDING')

    def __str__(self):
        return str(self.user)
