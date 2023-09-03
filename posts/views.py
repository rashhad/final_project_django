from typing import Any, Dict
from django.db.models.query import QuerySet, Q
from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.urls import reverse_lazy
from .models import posts

# Create your views here.

class CreatePost(LoginRequiredMixin, generic.CreateView):
    template_name='create.html'
    form_class=forms.PostCreateForm
    success_url=reverse_lazy('home')

    def get_initial(self) -> Dict[str, Any]:
        return {'blogger': self.request.user}
    
class readPost(generic.DetailView):
    model=posts
    template_name='read_post.html'

class editPost(generic.UpdateView):
    model=posts
    form_class=forms.PostCreateForm
    template_name='edit_post.html'

    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          pk=self.kwargs['pk']
          return reverse_lazy('read', kwargs={'pk': pk})

class delPost(generic.DeleteView):
    model=posts
    success_url = reverse_lazy('profile')
    template_name='profile.html'


class ShowContentsTopicWise(generic.ListView):
    template_name='show_topic_content.html'

    def get_queryset(self) -> QuerySet[Any]:
        s=self.kwargs['s']
        return posts.objects.filter(topic=s)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title']=self.kwargs['s']
        return context
    


class searchResult(generic.ListView):
    template_name='show_topic_content.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        search_text = self.request.GET.get('search')
        qset= posts.objects.filter(Q(title__icontains=search_text)|Q(content__icontains=search_text))
        print(search_text, qset)
        return qset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title']='Search Result'
        return context