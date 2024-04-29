from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('home',views.user_home, name="home"),
    path('sign-up',views.sign_up,name="sign-up"),
]
