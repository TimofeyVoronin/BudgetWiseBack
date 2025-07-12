from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Case, When, F, DecimalField
from .models import Transaction, Balance

@receiver([post_save, post_delete], sender=Transaction)
def update_user_balance(sender, instance, **kwargs):
    user = instance.user
    agg = Transaction.objects.filter(user=user).aggregate(
        balance=Sum(
            Case(
                When(type=0, then=F('amount')),
                When(type=1, then=-F('amount')),
                output_field=DecimalField()
            )
        )
    )
    total = agg['balance'] or 0

    Balance.objects.update_or_create(
        user=user,
        defaults={'amount': total}
    )