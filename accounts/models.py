from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    OTP = models.BigIntegerField(default=2048)
    IsVerified = models.BooleanField(default=False)
