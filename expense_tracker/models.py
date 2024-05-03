from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Link to the user's account
    name = models.CharField(max_length=100, default="default wallet")  # Wallet name
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Initial balance

    # Meta class to allow two different users to have same wallet name
    # but it prevents a given user from having two wallets of same name
    class Meta:
        unique_together = [('user', 'name')]

    def __str__(self):
        return f"{self.name}"  # For readable display


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique category name

    def __str__(self):
        return self.name  # For readable display

    def delete(self, *args, **kwargs):
        raise Exception("Deleting categories is not allowed.")


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE
    )  # One-to-many link to Wallet
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )  # Many-to-one link to Category
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    date = models.DateField()  # Transaction date
    is_income = models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} - {self.category.name if self.category else 'Uncategorized'}"
