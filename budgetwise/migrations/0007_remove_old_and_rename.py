from django.db import migrations, models
import django.db.models.deletion

def fill_missing_categories(apps, schema_editor):
    Transaction = apps.get_model('budgetwise', 'Transaction')
    Category    = apps.get_model('budgetwise', 'Category')
    default_cat, _ = Category.objects.get_or_create(name='Прочее')
    Transaction.objects.filter(category_fk__isnull=True).update(category_fk=default_cat)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('budgetwise', '0006_migrate_category_data'),
    ]

    operations = [
        migrations.RunPython(fill_missing_categories, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='category_fk',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(
                to='budgetwise.Category',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transactions',
                null=False,
            ),
        ),
    ]
