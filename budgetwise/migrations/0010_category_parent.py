from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('budgetwise', '0009_alter_position_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                to='budgetwise.Category',
                null=True,
                blank=True,
                related_name='subcategories',
                on_delete=django.db.models.deletion.CASCADE
            ),
        ),
    ]
