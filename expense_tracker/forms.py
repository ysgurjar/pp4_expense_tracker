from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction,Wallet,Category
from django.utils import formats,timezone



class RegisterForm(UserCreationForm):

    class Meta:
        model=User
        fields= ["username","password1","password2"]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        #fields = ['wallet', 'category', 'amount', 'date','is_income']
        exclude=['user']
        widgets = {
            'date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date', 'max': formats.date_format(timezone.now(), 'Y-m-d')})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)

class UpdateTransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        
        exclude=['user']
        widgets = {
            'date': forms.DateInput( attrs={'type': 'date', 'max': formats.date_format(timezone.now(), 'Y-m-d')})
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print("User:", user) 
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)

class DeleteTransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields = ['user','wallet', 'category', 'amount', 'date','is_income']
        exclude=['user']
        #widgets = {
        #    'date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date', 'max': formats.date_format(timezone.now(), 'Y-m-d')})
        #}
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print("User:", user) 
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)

# Wallets

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        exclude=['user']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['name'].queryset = Wallet.objects.filter(user=user)


class UpdateWalletForm(forms.ModelForm):
    class Meta:
        model=Wallet
        
        exclude=['user']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['name'].queryset = Wallet.objects.filter(user=user)

class DeleteWalletForm(forms.ModelForm):
    class Meta:
        model=Wallet
        exclude=['user']

        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields['name'].queryset = Wallet.objects.filter(user=user)