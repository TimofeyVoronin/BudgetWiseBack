from django.conf import settings
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Положительное число для дохода, отрицательное — для расхода"
    )
    date = models.DateField(
        help_text="Дата транзакции"
    )
    category = models.CharField(
        max_length=50,
        help_text="Категория транзакции"
    )
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]
    type = models.CharField(
        max_length=7,
        choices=TYPE_CHOICES,
        help_text="Доход или расход"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Время создания записи"
    )

    def __str__(self):
        return f"{self.user.username}: {self.get_type_display()} {self.amount} on {self.date}"