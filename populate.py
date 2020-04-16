import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jpisforum.settings')

import django
django.setup()

import random
from faker import Faker

fake = Faker()

from django.contrib.auth.models import User
import xlrd
from accounts.models import Register

wb = xlrd.open_workbook("Students.xlsx")
sheet = wb.sheet_by_index(0)

count = 0
while True:
    try:
        user = User.objects.create_user(username=sheet.cell_value(count+2, 0),password='jpis@123',email=sheet.cell_value(count+2, 1))
        register = Register(user=user, OTP=0,IsVerified=True)
        register.save()
        count += 1
    except:
        break




# class Post(models.Model):
#     Name = models.CharField(max_length = 264)
#     Init_time = models.DateTimeField()
#     Description = models.TextField()
#     Author = models.CharField(max_length = 264)
#     Image = models.FileField(blank=True)
#     Video = models.FileField(blank=True)
#     Doc = models.FileField(blank=True)
#
#     def __str__(self):
#         return self.Name

# class Painting(models.Model):
#     category = models.CharField(max_length=264)
#     artist = models.CharField(max_length=264)
#     price = models.IntegerField()
#     height = models.IntegerField()
#     width = models.IntegerField()
