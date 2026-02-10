from django.db import models
from django.contrib.auth.models import User


# ===== REMINDER MODEL =====
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    note = models.TextField(blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine


# ===== PROFILE MODEL =====
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
