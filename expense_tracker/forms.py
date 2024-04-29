from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction,Wallet,Category

class RegisterForm(UserCreationForm):

    class Meta:
        model=User
        fields= ["username","password1","password2"]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'category', 'amount', 'date','is_income']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
            