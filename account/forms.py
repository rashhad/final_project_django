from typing import Any
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . import choices


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
                user_instance = self.instance
            except models.profile.DoesNotExist:
                user_instance = None

            if user_instance:
                self.fields['gender'].initial = user_instance.profile.gender
                self.fields['dob'].initial = user_instance.profile.dob
                self.fields['address'].initial = user_instance.profile.address
                self.fields['about'].initial = user_instance.profile.about

    def save(self) -> Any:
        user = super().save()
        data=self.cleaned_data
        models.profile.objects.filter(user=user).update(
            dob=data['dob'],
            gender=data['gender'],
            address=data['address'],
            about=data['about'],
        )