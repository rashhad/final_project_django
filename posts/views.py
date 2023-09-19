from typing import Any, Dict
from django.db.models.query import QuerySet, Q
from django.shortcuts import render, redirect, HttpResponse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.urls import reverse_lazy, reverse
from .models import posts
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import urllib.parse
from interactions.models import interactions, relpies
from django.db.models import Avg

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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['interactions']=interactions.objects.filter(post=kwargs['object'])
        context['rating'] = interactions.objects.filter(post=kwargs['object']).aggregate(Avg('rating'))['rating__avg']
        context['rep'] = relpies.objects.filter(comment__post=kwargs['object'])
        context['comment_sw']=True
        if self.request.user in [item.user for item in interactions.objects.filter(post=kwargs['object'])]:
            context['comment_sw']=False
        return context

class reply_handler(generic.View):
    def post(self, request, post_id, id):
        print(request.POST.get('reply'), post_id, id)
        comment=interactions.objects.get(id=id)
        relpies.objects.create(
            comment=comment,
            user=request.user,
            reply=request.POST.get('reply'),
        ).save()
        return redirect(reverse_lazy("read",kwargs={'pk':post_id}))

class add_comment(generic.View):
    def post(self, request, pk):
        # print(request.POST.get('comment'), pk)
        interactions.objects.create(
            post=posts.objects.get(id=pk),
            user=request.user,
            comment=request.POST.get('comment'),
            rating=request.POST.get('rating'),
        ).save()
        return redirect(reverse_lazy('read', kwargs = {'pk': pk}))

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
        topic=self.kwargs['topic']
        return posts.objects.filter(topic=topic)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # pagination
        p=Paginator(context['object_list'], 2)
        page_number = self.request.GET.get('page')
        try:
            page_obj=p.get_page(page_number)
        except PageNotAnInteger:    #if page_number is other than int value return to page 1
            page_obj=p.page(1)
        except EmptyPage:
            page_obj=p.page(p.num_pages)    #page_number is int value but out of range, return to last page
        context['page_obj']= page_obj
        context['page_range'] = p.page_range
        context['title']=self.kwargs['topic']
        return context




class searchResult(generic.ListView):
    template_name='show_topic_content.html'
    paginate_by = 5             #handles pagination logic
    
    def get_queryset(self) -> QuerySet[Any]:
        search_text = self.request.GET.get('search')
        qset= posts.objects.filter(Q(title__icontains=search_text)|Q(content__icontains=search_text))
        print(search_text, qset)
        return qset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title']='Search Result'
        search = urllib.parse.quote_plus(self.request.GET.get('search'))
        context['search_text']=search
        return context
