from django.urls import path
from . import views


urlpatterns = [
    path('sign_up/',views.signUp.as_view(),name='signup'),
    path('login/',views.login.as_view(),name='login'),
    path('logout/',views.logout.as_view(),name='logout'),
    # path('profile/',views.profile,name='profile'),
    path('profile/',views.profile.as_view(),name='profile'),
    path('passChange/',views.ChangPass.as_view(),name='passChange'),
]
