from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.profile)
class Profile(admin.ModelAdmin):
    list_display = ['user','gender']