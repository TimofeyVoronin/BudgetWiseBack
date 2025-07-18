from django.conf import settings
from django.db import models
from django.db.models import Sum, Case, When, F, DecimalField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Название категории")
    description = models.TextField(blank=True, help_text="Подробное описание категории")
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='subcategories',
        help_text="Родительская категория (если это подкатегория)"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

TYPE_CHOICES = (
    (0, 'Доход'),
    (1, 'Расход'),
)

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    date = models.DateField(help_text="Дата транзакции")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='transactions',
        help_text="Категория транзакции"
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Общая сумма чека (вводит пользователь)"
    )
    type = models.ForeignKey(
        'OperationType',
        on_delete=models.PROTECT,
        db_column='type',
        help_text="Ссылка на тип операции (0=Доход, 1=Расход)",
        related_name='transactions'
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания записи")

    def __str__(self):
        return f"{self.user.username}: {self.get_type_display()} on {self.date}"


class OperationType(models.Model):
    id   = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
    def __str__(self):
        return self.name


class Position(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE,
        related_name='positions'
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='positions',
        help_text="Категория позиции"
    )
    name = models.CharField(max_length=100, help_text="Наименование позиции")
    quantity = models.PositiveIntegerField(help_text="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена за 1 шт.")
    sum = models.DecimalField(max_digits=12, decimal_places=2, help_text="Сумма")

    def save(self, *args, **kwargs):
        self.sum = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category}: {self.name} x{self.quantity}"


class Balance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='balance'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Текущий баланс пользователя"
    )

    def __str__(self):
        return f"{self.user.username} — {self.amount}"
