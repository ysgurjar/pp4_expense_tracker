from django.urls import path
from django.contrib.auth.views import LoginView

# To be able to see static files
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("personal/", views.personal_home, name="personal_home"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("login/", LoginView.as_view(), name="login"),
    # Transaction
    path(
        "personal/transaction/create",
        views.TransactionCreateView.as_view(),
        name="create_transaction",
    ),
    path(
        "personal/transactions",
        views.ListTransaction.as_view(),
        name="list_transaction",
    ),
    path("personal/overview", views.overview, name="overview"),
    path(
        "personal/transactions/<int:pk>/update",
        views.UpdateTransaction.as_view(),
        name="update_transaction",
    ),
    path(
        "personal/transactions/<int:pk>/delete",
        views.DeleteTransaction.as_view(),
        name="delete_transaction",
    ),
    # Wallet
    path(
        "personal/wallet/create",
        views.WalletCreateView.as_view(),
        name="create_wallet",
    ),
    path("personal/wallets", views.ListWallet.as_view(), name="list_wallet"),
    path(
        "personal/wallets/<int:pk>/update",
        views.UpdateWallet.as_view(),
        name="update_wallet",
    ),
    path(
        "personal/wallets/<int:pk>/delete",
        views.DeleteWallet.as_view(),
        name="delete_wallet",
    ),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
