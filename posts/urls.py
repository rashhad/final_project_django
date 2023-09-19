from django.urls import path
from . import views


urlpatterns = [
    path('create/',views.CreatePost.as_view(), name='create'),
    path('readpost/<int:pk>',views.readPost.as_view(), name='read'),
    path('edit/<int:pk>',views.editPost.as_view(), name='edit'),
    path('delete/<int:pk>',views.delPost.as_view(), name='delete'),
    path('topic/<str:topic>/',views.ShowContentsTopicWise.as_view(), name='topic'),
    path('search/',views.searchResult.as_view(), name='search'),
    path('add_comm/<int:pk>',views.add_comment.as_view(), name='add_comment'),
    path('rep/<int:post_id>/<int:id>',views.reply_handler.as_view(), name='reply'),
]
