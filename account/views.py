from typing import Any, Dict
from django.shortcuts import render, redirect
from . import forms
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import posts
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
# Create your views here.

class signUp(generic.CreateView):
    template_name='signUp.html'
    form_class=forms.registrationForm

    def get_success_url(self) -> str:
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title']='Sign up'
        return context
    

class login(LoginView):
    template_name='login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('profile')
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title']='Login'
        return context
    

class logout(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')


class profile(LoginRequiredMixin, View):
    template_name = 'profile.html'
    def get(self, request):
        blogs=posts.objects.filter(blogger=request.user)
        p=Paginator(blogs, 3)
        page_num=self.request.GET.get('page')
        page_obj=p.get_page(page_num)
        context={
            'blogs':blogs,
            'title':'Profile',
            'page_obj':page_obj,
        }
        if not request.user.is_superuser:
            context['form']=forms.UpdateForm(instance=request.user)
        return render(request,self.template_name,context)
    
    def post(self, request):
        form=forms.UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request,self.template_name, {'form':form})
    
    

class ChangPass(LoginRequiredMixin, View):
    def post(self, request):
        form=PasswordChangeForm(user=request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
        return render(request, 'profile.html', {'form':form, 'title':'Profile'})
    
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'pass_change.html', {'form':form,'title':'Profile'})
