# Import related to general functionalites
from django.shortcuts import render, redirect, reverse

# Import related to auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm

# Import related to creating class based view
from .models import Transaction, Wallet
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TransactionForm, UpdateTransactionForm

# Import related to wallet balance update on transaction creation
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Import related to aggrigate queries for overview page
import json
from django.db.models import Sum, Case, When, DecimalField
from decimal import Decimal

# Imports related to wallet balance update on deletion of transaction
from django.db.models.signals import pre_delete

# Import related to messages
from django.contrib import messages

# Import related to wallets
from .forms import WalletForm, UpdateWalletForm

# Import related to protecting class based view
from django.contrib.auth.mixins import LoginRequiredMixin

# ============================= View Functions =============================


def home(request):
    """Render the home page."""
    return render(request, "expense_tracker/home.html")


# Only authenticated users allowed
@login_required
def personal_home(request):
    """Display personal home page for logged-in users."""
    user = request.user
    context = {
        "username": user.username,
    }
    return render(request, "expense_tracker/personal_home.html", context)


def sign_up(request):
    """Handle user registration and log in upon successful registration."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Account created successfully! Please log in."
            )
            return redirect(reverse("login"))
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})


# === Transaction related views ===


# Class-based view for creating transactions
class TransactionCreateView(LoginRequiredMixin, CreateView):
    """Create a new transaction for logged-in users."""

    # 1- binding view class to model
    model = Transaction
    # 2 - binding view class to form
    form_class = TransactionForm

    # 3 - html that the view will serve, which will be a form
    template_name = "expense_tracker/create_transaction.html"

    # 4 - upon successful completion of form, user is redirect to
    success_url = reverse_lazy("list_transaction")

    def get_form_kwargs(self):
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Add the current user to the kwargs
        kwargs["user"] = self.request.user

        return kwargs  # Return the modified kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user before saving
        super().form_valid(form)
        return redirect("list_transaction")


# Class-based view for listing transactions
class ListTransaction(LoginRequiredMixin, ListView):
    # template_name="expense_tracker/transactions.html"
    model = Transaction
    context_object_name = "transactions"

    def get_queryset(self):
        """Filter transactions to those belonging to the current user,
        ordered by date."""
        # Order the queryset by the 'date' field in descending order
        user = self.request.user
        queryset = super().get_queryset().filter(user=user).order_by("-date")
        return queryset

# Class-based view for updating transactions
class UpdateTransaction(LoginRequiredMixin, UpdateView):
    """Update an existing transaction."""
    model = Transaction
    form_class = UpdateTransactionForm
    template_name = (
        "expense_tracker/update_transaction.html"  # Template for update form
    )
    success_url = reverse_lazy(
        "list_transaction"
    )  # URL to redirect after successful update

    def get_form_kwargs(self):
        kwargs = super(UpdateTransaction, self).get_form_kwargs()
        # Add the current user to form kwargs
        kwargs["user"] = self.request.user
        return kwargs

# Class-based view for deleting transactions
class DeleteTransaction(LoginRequiredMixin, DeleteView):
    """Delete an existing transaction."""
    model = Transaction
    # form_class=DeleteTransactionForm
    template_name = "expense_tracker/transaction_confirm_delete.html"
    success_url = reverse_lazy(
        "list_transaction"
    )  # URL to redirect after successful update

# === Wallet related views ===

# Class-based view for creating wallets
class WalletCreateView(LoginRequiredMixin, CreateView):
    """Create a new wallet for the logged-in user."""
    # 1- binding view class to model
    model = Wallet
    # 2 - binding view class to form
    form_class = WalletForm

    # 3 - html that the view will serve, which will be a form
    template_name = "expense_tracker/create_wallet.html"

    # 4 - upon successful completion of form, user is redirect to
    success_url = reverse_lazy("list_wallet")

    def get_form_kwargs(self):
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Add the current user to the kwargs
        kwargs["user"] = self.request.user

        return kwargs  # Return the modified kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user before saving
        super().form_valid(form)
        return redirect("list_wallet")


# Class-based view for listing wallets
class ListWallet(LoginRequiredMixin, ListView):
    """List all wallets of the logged-in user."""
    model = Wallet
    context_object_name = "wallets"

    def get_queryset(self):
        """Filter wallets to those belonging to the current user."""
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)
        return queryset

# Class-based view for updating wallets
class UpdateWallet(LoginRequiredMixin, UpdateView):
    """Update an existing wallet."""
    model = Wallet
    form_class = UpdateWalletForm
    template_name = "expense_tracker/update_wallet.html"
    success_url = reverse_lazy(
        "list_wallet"
    )  # URL to redirect after successful update

    def get_form_kwargs(self):
        """Inject current user into form kwargs."""
        kwargs = super(UpdateWallet, self).get_form_kwargs()
        # Add the current user to form kwargs
        kwargs["user"] = self.request.user
        return kwargs

# Class-based view for deleting wallets
class DeleteWallet(LoginRequiredMixin, DeleteView):
    """Update an existing wallet."""
    model = Wallet
    template_name = "expense_tracker/wallet_confirm_delete.html"
    success_url = reverse_lazy(
        "list_wallet"
    )  # URL to redirect after successful update

# === Overview page logic

# overview function
@login_required
def overview(request):
    """Renders overview page for logged in users"""
    wallets = Wallet.objects.filter(user=request.user)

    # Get expenses by category
    expense_by_cat = (
        Transaction.objects.filter(wallet__in=wallets)
        .values("category__name")
        .annotate(total_amount=Sum("amount"))
        .order_by("-total_amount")
    )

    # Get top 5 expense transactions (not income)
    top_transactions = (
        Transaction.objects.filter(is_income=False, wallet__in=wallets)
        .order_by("-amount")
        .values("amount", "category__name", "date")[:5]
    )

    # Get total income and total expense
    totals = Transaction.objects.filter(wallet__in=wallets).aggregate(
        total_income=Sum(
            Case(
                When(is_income=True, then="amount"),
                default=0,
                output_field=DecimalField(),
            )
        ),
        total_expense=Sum(
            Case(
                When(is_income=False, then="amount"),
                default=0,
                output_field=DecimalField(),
            )
        ),
    )


    # Handling Decimal types for JSON serialization
    totals_serialized = json.dumps(
        totals, default=lambda x: str(x) if isinstance(x, Decimal) else x
    )

    return render(
        request,
        "expense_tracker/overview.html",
        {
            "wallets": wallets,
            "expense_by_cat": list(expense_by_cat),
            "top_transactions": top_transactions,
            "totals": totals_serialized,
        },
    )


# Dictionary to hold the old data temporarily
old_data = {}


@receiver(pre_save, sender=Transaction)
def capture_old_instance(sender, instance, **kwargs):
    if instance.pk:  # Ensures this is not a new instance
        old_instance = sender.objects.get(pk=instance.pk)
        old_data[instance.pk] = {
            "amount": old_instance.amount,
            "is_income": old_instance.is_income,
            "wallet_id": old_instance.wallet_id,  # Store only the wallet_id
        }


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    wallet = Wallet.objects.get(
        id=instance.wallet_id
    )  # Fetch the latest wallet state
    if created:
        if instance.is_income:
            wallet.balance += instance.amount
        else:
            wallet.balance -= instance.amount
    else:
        old_instance_data = old_data.pop(instance.pk, None)
        if old_instance_data:
            # Fetch the wallet associated with the old transaction data if it's different
            if old_instance_data["wallet_id"] != instance.wallet_id:
                old_wallet = Wallet.objects.get(
                    id=old_instance_data["wallet_id"]
                )
            else:
                old_wallet = wallet

            # Undo the old transaction effect
            if old_instance_data["is_income"]:
                old_wallet.balance -= old_instance_data["amount"]
            else:
                old_wallet.balance += old_instance_data["amount"]
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
