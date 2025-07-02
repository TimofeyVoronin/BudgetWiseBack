from django.db import migrations, models

def populate_categories(apps, schema_editor):
    Category = apps.get_model('budgetwise', 'Category')
    default_names = [
        'Обязательные расходы',
        'Расходы на питание',
        'Расходы на хозяйственно-бытовые нужды',
        'Расходы на предметы личного пользования',
        'Расходы на предметы быта',
    ]
    for name in default_names:
        Category.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    initial = False
    dependencies = [
        ('budgetwise', '0003_position_delete_mymodel_remove_transaction_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RunPython(
            code=populate_categories, 
            reverse_code=migrations.RunPython.noop
        ),
    ]
