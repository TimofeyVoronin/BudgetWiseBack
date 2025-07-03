from django.db import migrations

def migrate_category(apps, schema_editor):
    Transaction = apps.get_model('budgetwise', 'Transaction')
    Category    = apps.get_model('budgetwise', 'Category')
    for txn in Transaction.objects.all():
        try:
            cat = Category.objects.get(name=txn.category)
        except Category.DoesNotExist:
            continue
        txn.category_fk = cat
        txn.save(update_fields=['category_fk'])

class Migration(migrations.Migration):

    dependencies = [
        ('budgetwise', '0005_add_category_fk'),
    ]

    operations = [
        migrations.RunPython(migrate_category, reverse_code=migrations.RunPython.noop),
    ]
