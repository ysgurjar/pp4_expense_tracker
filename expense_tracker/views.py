# Import related to general functionalites
from django.shortcuts import render
from django.shortcuts import render, redirect, reverse

# Import related to auth
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Import related to creating class based view
from .forms import TransactionForm
from .models import Transaction,Wallet
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy


# Import related to wallet balance update on transaction creation
from django.db.models.signals import post_save
from django.dispatch import receiver


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
            return redirect(reverse('home'))
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
    success_url=reverse_lazy('overview')

    def get_form_kwargs(self):
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Add the current user to the kwargs
        kwargs['user'] = self.request.user

        return kwargs  # Return the modified kwargs


    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user before saving
        super().form_valid(form)
        return redirect('home')

# show a list of transactions
class ListTransaction(ListView):
    template_name="expense_tracker/transactions.html"
    model = Transaction
    context_object_name="transactions"



# overview function
def overview(request):

    wallets=Wallet.objects.filter(user=request.user)
    return render(request, "expense_tracker/overview.html", {
        "wallets":wallets
    })


# Update wallet balance on transaction createion
@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    """Update the wallet's balance when a new transaction is created."""
    if created:
        wallet = instance.wallet
        wallet.balance += instance.amount
        wallet.save()