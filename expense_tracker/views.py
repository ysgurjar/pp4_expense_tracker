# Import related to general functionalites
from django.shortcuts import render
from django.shortcuts import render, redirect, reverse

# Import related to auth
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Import related to creating class based view
from .forms import TransactionForm,UpdateTransactionForm,DeleteTransactionForm
from .models import Transaction,Wallet
from django.views.generic.edit import CreateView
from django.views.generic import ListView,UpdateView,DeleteView
from django.urls import reverse_lazy


# Import related to wallet balance update on transaction creation
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Import related to aggrigate query for overview pag
import json
from django.db.models import Sum,Case, When, Value, DecimalField
from django.http import JsonResponse
from django.core.serializers import serialize
from decimal import Decimal

# Imports related to wallet balance update on deletion of transaction
from django.db.models.signals import pre_delete

# Import related to messages
from django.contrib import messages

# Import related to wallets

from .forms import WalletForm,UpdateWalletForm,DeleteWalletForm

# =============================




def home(request):
    return render(request,'expense_tracker/home.html')

# If user attempts to access page without log in
# redirect to home
@login_required(login_url="/")
def personal_home(request):
    user=request.user
    context = {
        'username':user.username,
    }
    return render(request,'expense_tracker/personal_home.html', context)


def sign_up(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect(reverse('login'))
    else:
        form=RegisterForm()

    return render(request,'registration/sign_up.html',{"form":form})


# Create form for transaction
class TransactionCreateView(CreateView):
    # 1- binding view class to model
    model=Transaction
    # 2 - binding view class to form
    form_class=TransactionForm

    # 3 - html that the view will serve, which will be a form
    template_name="expense_tracker/create_transaction.html"

    # 4 - upon successful completion of form, user is redirect to
    success_url=reverse_lazy('list_transaction')

    def get_form_kwargs(self):
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Add the current user to the kwargs
        kwargs['user'] = self.request.user

        return kwargs  # Return the modified kwargs


    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user before saving
        super().form_valid(form)
        return redirect('list_transaction')

# show a list of transactions
class ListTransaction(ListView):
    #template_name="expense_tracker/transactions.html"
    model = Transaction
    context_object_name="transactions"

    def get_queryset(self):
        # Get the default queryset
        
        # Order the queryset by the 'date' field in descending order
        user = self.request.user
        queryset = super().get_queryset().filter(user=user).order_by('-date')
        return queryset


# ===== Wallets =====

# Create form for wallets
class WalletCreateView(CreateView):
    # 1- binding view class to model
    model=Wallet
    # 2 - binding view class to form
    form_class=WalletForm

    # 3 - html that the view will serve, which will be a form
    template_name="expense_tracker/create_wallet.html"

    # 4 - upon successful completion of form, user is redirect to
    success_url=reverse_lazy('list_wallet')

    def get_form_kwargs(self):
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Add the current user to the kwargs
        kwargs['user'] = self.request.user

        return kwargs  # Return the modified kwargs


    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user before saving
        super().form_valid(form)
        return redirect('list_wallet')

# show a list of wallets
class ListWallet(ListView):
    #template_name="expense_tracker/transactions.html"
    model = Wallet
    context_object_name="wallets"

    def get_queryset(self):
        # Get the default queryset
        
        # Order the queryset by the 'date' field in descending order
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)
        return queryset


class UpdateWallet(UpdateView):
    model = Wallet
    form_class=UpdateWalletForm
    template_name = 'expense_tracker/update_wallet.html'  # Template for update form
    success_url = reverse_lazy('list_wallet')  # URL to redirect after successful update

    def get_form_kwargs(self):
        kwargs = super(UpdateTransaction, self).get_form_kwargs()
        # Add the current user to form kwargs
        kwargs['user'] = self.request.user
        return kwargs

class DeleteWallet(DeleteView):
    model = Wallet
    #form_class=DeleteTransactionForm
    template_name = 'expense_tracker/wallet_confirm_delete.html'  # Template for update form
    success_url = reverse_lazy('list_wallet')  # URL to redirect after successful update

# overview function
def overview(request):

    wallets = Wallet.objects.filter(user=request.user)

    # Get expenses by category
    expense_by_cat = Transaction.objects.filter(wallet__in=wallets).values('category__name') \
                                        .annotate(total_amount=Sum('amount')) \
                                        .order_by('-total_amount')

    # Get top 5 expense transactions (not income)
    top_transactions = Transaction.objects.filter(is_income=False, wallet__in=wallets).order_by('-amount').values('amount', 'category__name', 'date')[:5]

    # Get total income and total expense
    totals = Transaction.objects.filter(wallet__in=wallets).aggregate(
        total_income=Sum(Case(
            When(is_income=True, then='amount'),
            default=0,
            output_field=DecimalField()
        )),
        total_expense=Sum(Case(
            When(is_income=False, then='amount'),
            default=0,
            output_field=DecimalField()
        ))
    )

    # Serialize data
    # Note: Serialize function is for model instances, not for dictionaries
    # So for dictionaries, we use json.dumps
    #top_transactions = serialize('json',top_transactions)

    # Handling Decimal types for JSON serialization
    totals_serialized = json.dumps(totals, default=lambda x: str(x) if isinstance(x, Decimal) else x)

    return render(request, "expense_tracker/overview.html", {
        "wallets": wallets,
        "expense_by_cat": list(expense_by_cat),
        "top_transactions": top_transactions,
        "totals": totals_serialized,
    })

# ======== wallets function
def wallets(request):

    wallets=Wallet.objects.filter(user=request.user)
    return render(request, "expense_tracker/wallets.html", {
        "wallets":wallets
    })


# Dictionary to hold the old data temporarily
old_data = {}

@receiver(pre_save, sender=Transaction)
def capture_old_instance(sender, instance, **kwargs):
    if instance.pk:  # Ensures this is not a new instance
        old_instance = sender.objects.get(pk=instance.pk)
        old_data[instance.pk] = {
            'amount': old_instance.amount,
            'is_income': old_instance.is_income,
            'wallet_id': old_instance.wallet_id,  # Store only the wallet_id
        }

@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    wallet = Wallet.objects.get(id=instance.wallet_id)  # Fetch the latest wallet state
    if created:
        if instance.is_income:
            wallet.balance += instance.amount
        else:
            wallet.balance -= instance.amount
    else:
        old_instance_data = old_data.pop(instance.pk, None)
        if old_instance_data:
            # Fetch the wallet associated with the old transaction data if it's different
            if old_instance_data['wallet_id'] != instance.wallet_id:
                old_wallet = Wallet.objects.get(id=old_instance_data['wallet_id'])
            else:
                old_wallet = wallet

            # Undo the old transaction effect
            if old_instance_data['is_income']:
                old_wallet.balance -= old_instance_data['amount']
            else:
                old_wallet.balance += old_instance_data['amount']
            old_wallet.save()

            # Apply the new transaction effect
            if instance.is_income:
                wallet.balance += instance.amount
            else:
                wallet.balance -= instance.amount

    wallet.save()

# Create default "Your wallet" on account creation
@receiver(post_save, sender=User)
def create_default_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, name="Your Wallet", balance=0.00)


# =====


class UpdateTransaction(UpdateView):
    model = Transaction
    form_class=UpdateTransactionForm
    template_name = 'expense_tracker/update_transaction.html'  # Template for update form
    success_url = reverse_lazy('list_transaction')  # URL to redirect after successful update

    def get_form_kwargs(self):
        kwargs = super(UpdateTransaction, self).get_form_kwargs()
        # Add the current user to form kwargs
        kwargs['user'] = self.request.user
        return kwargs

class DeleteTransaction(DeleteView):
    model = Transaction
    #form_class=DeleteTransactionForm
    template_name = 'expense_tracker/transaction_confirm_delete.html'  # Template for update form
    success_url = reverse_lazy('list_transaction')  # URL to redirect after successful update


# UPDATE WALLET BALANCE WHEN TRANSACTION IS DELETED

@receiver(pre_delete, sender=Transaction)
def adjust_wallet_on_delete(sender, instance, **kwargs):
    """Adjust the wallet balance when a transaction is deleted."""
    wallet = instance.wallet
    if instance.is_income:
        wallet.balance -= instance.amount
    else:
        wallet.balance += instance.amount
    wallet.save()


