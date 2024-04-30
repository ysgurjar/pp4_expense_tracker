from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.home,name="home"),
    path('personal/',views.personal_home, name="personal_home"),
    path('sign-up/',views.sign_up,name="sign-up"),
    path('login/',LoginView.as_view(),name='login'),
    # Transaction
    path('personal/transaction/create',views.TransactionCreateView.as_view(),name="create_transaction"),
    path('personal/transactions',views.ListTransaction.as_view(),name="list_transaction"),
    path('personal/overview',views.overview,name="overview")
]
