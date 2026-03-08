from django.db import models
from django.conf import settings
from decimal import Decimal
from cloudConverterApp.models import ConvertModel

User = settings.AUTH_USER_MODEL

class WalletModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def credit(self, amount):
        self.balance += amount
        self.save()

    def debit(self, amount):
        if self.balance <= 0:
            raise ValueError('Insufficient Balance')
        else:
            self.balance -= amount
            self.save()

    def __str__(self):
        return f'{self.user} have balance: {self.balance}'

class TransactionHistoryModel(models.Model):
    TRANSACTION_TYPE = (
        ('credit', 'CREDIT'),
        ('debit', 'DEBIT'),
    )

    wallet = models.ForeignKey(WalletModel, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPE)
    conversion = models.ForeignKey(ConvertModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_type} -> {self.amount}'