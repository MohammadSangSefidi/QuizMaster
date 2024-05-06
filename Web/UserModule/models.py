from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserModel(AbstractUser):
    score = models.IntegerField(default=0, verbose_name='امتیاز')
    user_class = models.CharField(max_length=10, null=True, verbose_name='کلاس')
    email = models.EmailField(null=True, verbose_name='ایمیل')
    profile_image = models.IntegerField(default=1, verbose_name='عکس پروفایل')
    isTeacher = models.BooleanField(default=False, verbose_name='معلم هست/نیست')