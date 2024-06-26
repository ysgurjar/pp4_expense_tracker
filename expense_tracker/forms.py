from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import formats, timezone

from .models import Transaction, Wallet


class RegisterForm(UserCreationForm):
    """Form for registering a new user with a username and password."""

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class TransactionForm(forms.ModelForm):
    """Form for creating a new transaction."""
    is_income = forms.BooleanField(
        label="Mark transaction as income", required=False
    )
    class Meta:
        model = Transaction
        # fields = ['wallet', 'category', 'amount', 'date','is_income']
        exclude = ["user"]
        widgets = {
            "date": forms.DateInput(
                format="%d-%m-%Y",
                attrs={
                    "type": "date",
                    "max": formats.date_format(timezone.now(), "Y-m-d"),
                },
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields["wallet"].queryset = Wallet.objects.filter(user=user)


class UpdateTransactionForm(forms.ModelForm):
    """Form for updating an existing transaction."""

    is_income = forms.BooleanField(
        label="Mark transaction as income", required=False
    )

    class Meta:
        model = Transaction
        exclude = ["user"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": formats.date_format(timezone.now(), "Y-m-d"),
                }
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        print("User:", user)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields["wallet"].queryset = Wallet.objects.filter(user=user)


class DeleteTransactionForm(forms.ModelForm):
    """Form for deleting an existing transaction."""

    class Meta:
        model = Transaction
        fields = ["user", "wallet", "category", "amount", "date", "is_income"]
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        print("User:", user)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields["wallet"].queryset = Wallet.objects.filter(user=user)


class WalletForm(forms.ModelForm):
    """Form for creating a new wallet."""

    class Meta:
        model = Wallet
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)  # Initialize the form

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if Wallet.objects.filter(user=self.user, name=name).exists():
            raise ValidationError(
                {"name": "You already have a wallet with this name."}
            )

        return cleaned_data


class UpdateWalletForm(forms.ModelForm):
    """Form for updating an existing wallet."""

    class Meta:
        model = Wallet

        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(UpdateWalletForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            Wallet.objects.filter(user=self.user, name=name)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise forms.ValidationError(
                "You already have a wallet with this name."
            )
        return name


class DeleteWalletForm(forms.ModelForm):
    """Form for deleting an existing wallet."""

    class Meta:
        model = Wallet
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)  # Initialize the form

        if user is not None:  # Check if user is provided
            # Filter wallets by the current user's wallets
            self.fields["name"].queryset = Wallet.objects.filter(user=user)
