from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Link to the user's account
    name = models.CharField(max_length=100)  # Wallet name
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Initial balance

    def __str__(self):
        return f"{self.name} ({self.user.username})"  # For readable display


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
    description = models.TextField(blank=True, null=True)  # Optional description
    date = models.DateTimeField(auto_now_add=True)  # Transaction date
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} - {self.category.name if self.category else 'Uncategorized'}"
