from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.home,name="home"),
    path('personal/',views.personal_home, name="personal_home"),
    path('sign-up/',views.sign_up,name="sign-up"),
    path('login/',LoginView.as_view(),name='login'),
    # Transaction
    path('transaction/create',views.TransactionCreateView.as_view(),name="create_transaction")
]
