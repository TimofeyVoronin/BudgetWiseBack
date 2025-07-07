from django.db import migrations, models

def copy_type_to_int(apps, schema_editor):
    Transaction = apps.get_model('budgetwise', 'Transaction')
    for obj in Transaction.objects.all():
        if obj.type == 'income':
            obj._type_int = 0
        elif obj.type == 'outcome':
            obj._type_int = 1
        obj.save(update_fields=['_type_int'])

class Migration(migrations.Migration):
    dependencies = [
        ('budgetwise', '0013_populate_category_descriptions'),  # замените на вашу последнюю миграцию
    ]

    operations = [
        # 1) создаём новое поле, разрешаем null пока копируем
        migrations.AddField(
            model_name='transaction',
            name='_type_int',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        # 2) заполняем его из старого строкового `type`
        migrations.RunPython(copy_type_to_int, reverse_code=migrations.RunPython.noop),
    ]
