from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View, generic
from posts.models import posts
from django.db.models import Count
from posts import choices
# Create your views here.

class home(generic.TemplateView):
    template_name='core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_data"] = posts.objects.all()
        context["all_topics"] = choices.TOPICS
        context['title']='Home'
        return context