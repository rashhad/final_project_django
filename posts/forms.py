from typing import Any
from . import choices
from django import forms
from . models import posts
from django.utils.text import slugify

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = posts
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blogger'].widget = forms.HiddenInput() # user er theke hide kora thakbe
