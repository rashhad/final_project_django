from django.db import models
from django.contrib.auth.models import User
from . import choices
# Create your models here.

class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob=models.DateField()
    gender=models.CharField(max_length=10, choices=choices.GENDER)
    about = models.TextField(blank=True)
    address=models.TextField()
    pro_pic = models.ImageField(upload_to='pro_pic/', null=True)