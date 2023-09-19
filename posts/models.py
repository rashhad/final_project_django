from django.db import models
from django.contrib.auth.models import User
from . import choices
# Create your models here.

class posts(models.Model):
    blogger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=250)
    topic = models.CharField(max_length=50, choices=choices.TOPICS)
    content=models.TextField()
    pub_date=models.DateTimeField(auto_now_add=True)
    mod_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
