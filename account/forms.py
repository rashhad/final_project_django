from typing import Any
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . import choices
import os

class registrationForm(UserCreationForm):
    dob=forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=choices.GENDER, required=True)
    address=forms.CharField(widget=forms.TextInput)
    class Meta:
        model=User
        fields=[
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
        ]

    def save(self, commit=True) -> Any:
        user = super().save(commit=False)
        if(commit==True):
            user.save()

            data=self.cleaned_data
            models.profile.objects.create(
                user=user,
                dob=data['dob'],
                gender=data['gender'],
                address=data['address'],
            ).save()


class UpdateForm(UserChangeForm):
    password=None
    profile_picture = forms.FileField(max_length=100, required=False)
    dob=forms.DateField(required=True, widget=forms.DateInput())
    gender=forms.ChoiceField(choices=choices.GENDER, required=True)
    address=forms.CharField(widget=forms.TextInput)
    about=forms.CharField(widget=forms.TextInput)
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_instance = self.instance.profile
            except models.profile.DoesNotExist:
                user_instance = None
                
            if user_instance:
                self.fields['gender'].initial = user_instance.gender
                self.fields['dob'].initial = user_instance.dob
                self.fields['address'].initial = user_instance.address
                self.fields['about'].initial = user_instance.about

    def save(self) -> Any:
        user = super().save()
        old_image = models.profile.objects.get(user=user)
        data=self.cleaned_data
        if old_image.pro_pic and data['profile_picture']:
            image_path = old_image.pro_pic.path
            if os.path.exists(image_path):
                os.remove(image_path)
            old_image.pro_pic=data['profile_picture']
            print('chosen new pro pic, old pro pic o/w')
        elif old_image.pro_pic == '' and data['profile_picture']:
            old_image.pro_pic=data['profile_picture']
            print('new pro pic set')
        old_image.dob=data['dob']
        old_image.gender=data['gender']
        old_image.address=data['address']
        old_image.about=data['about']
        old_image.save()
