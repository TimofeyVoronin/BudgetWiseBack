from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('budgetwise', '0010_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, help_text='Подробное описание категории'),
        ),
    ]
