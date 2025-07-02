from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('budgetwise', '0004_create_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='category_fk',
            field=models.ForeignKey(
                to='budgetwise.Category',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transactions'
            ),
        ),
    ]
