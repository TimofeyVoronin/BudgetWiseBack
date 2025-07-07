from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('budgetwise', '0014_migrate_type_to_int'),
    ]

    operations = [
        # 1) удаляем старый CharField
        migrations.RemoveField(
            model_name='transaction',
            name='type',
        ),
        # 2) переименовываем временное _type_int в type
        migrations.RenameField(
            model_name='transaction',
            old_name='_type_int',
            new_name='type',
        ),
        # 3) делаем поле обязательным (null=False)
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0,'Доход'),(1,'Расход')]),
        ),
    ]
