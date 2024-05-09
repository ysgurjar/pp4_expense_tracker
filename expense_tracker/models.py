# Import to validate amount (only non neg entries allowed)
from decimal import Decimal
from django.core.validators import MinValueValidator

# Generic import
from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    """
    Represents a wallet owned by a user. Wallets store financial information
    such as the balance and are uniquely named per user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user to whom the wallet belongs.",
    )  # Link to the user's account
    name = models.CharField(
        max_length=100,
        default="default wallet",
        help_text="The name of the wallet.",
    )  # Wallet name
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="The initial balance of the wallet.",
    )  # Initial balance

    # Meta class to allow two different users to have same wallet name
    # but it prevents a given user from having two wallets of same name
    class Meta:
        unique_together = [("user", "name")]

    def __str__(self):
        return f"{self.name}"  # For readable display


class Category(models.Model):
    """
    Represents a transaction category. Each category has a unique name.
    Categories are used to organize transactions.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The unique name of the category.",
    )  # Unique category name

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
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )  # Transaction amount
    date = models.DateField()  # Transaction date
    is_income = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        category_name = (
            self.category.name if self.category else "Uncategorized"
        )
        return f"{self.amount} - {category_name}"
