from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def create_operation_types(apps, schema_editor):
    OperationType = apps.get_model('budgetwise', 'OperationType')
    # id=0 → Доход, id=1 → Расход
    OperationType.objects.bulk_create([
        OperationType(id=0, name='Доход'),
        OperationType(id=1, name='Расход'),
    ])

def delete_operation_types(apps, schema_editor):
    OperationType = apps.get_model('budgetwise', 'OperationType')
    OperationType.objects.filter(id__in=[0, 1]).delete()

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('budgetwise', 'Category')
    data = {
        'Без категории': 'Автоматически созданная категория',
        'Обязательные расходы': """\
Коммунальные платежи – это платежи предприятий, организаций и отдельных лиц за содержание и обслуживание жилья.
Плата за квартиру, телефон, электроэнергию, водоснабжение и т. д.
Образовательные платежи: содержание детей в детских садах, обучение в музыкальной школе, плата за высшее обучение и т. д.
Выплата кредитов, процентов по ссудам и т. д.
""",
        'Расходы на питание': """\
Приобретение продуктов в магазинах и на рынке, заготовка продуктов впрок.
Оплата питания в кафе, ресторанах, столовых.
""",
        'Расходы на хозяйственно-бытовые нужды': """\
Затраты на ремонт одежды, обуви, бытовой техники, квартиры, теле-радиоаппаратуры, химчистку, прачечную.
Покупка предметов личной гигиены.
""",
        'Расходы на предметы личного пользования': 'Верхняя одежда, белье, обувь, постельные принадлежности.',
        'Расходы на предметы быта': 'Мебель, светильники, ковровые изделия, картины, часы, хрусталь и т. д.',
        'Прочее': ''
    }
    for name, desc in data.items():
        Category.objects.update_or_create(
            name=name,
            defaults={'description': desc.strip(), 'parent': None}
        )

def delete_initial_categories(apps, schema_editor):
    Category = apps.get_model('budgetwise', 'Category')
    names = [
        'Без категории',
        'Обязательные расходы',
        'Расходы на питание',
        'Расходы на хозяйственно-бытовые нужды',
        'Расходы на предметы личного пользования',
        'Расходы на предметы быта',
        'Прочее'
    ]
    Category.objects.filter(name__in=names).delete()

def create_admin_user(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@mail.ru',
            password='admin'
        )

def delete_admin_user(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1) Category
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, help_text='Название категории')),
                ('description', models.TextField(blank=True, help_text='Подробное описание категории')),
                ('parent', models.ForeignKey(
                    to='budgetwise.Category',
                    on_delete=django.db.models.deletion.CASCADE,
                    null=True, blank=True,
                    related_name='subcategories',
                    help_text='Родительская категория (если это подкатегория)'
                )),
            ],
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),

        # 2) OperationType
        migrations.CreateModel(
            name='OperationType',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Тип операции',
                'verbose_name_plural': 'Типы операций',
            },
        ),

        # 3) Transaction (type → FK на OperationType, db_column='type')
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(help_text='Дата транзакции')),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Общая сумма чека (вводит пользователь)')),
                ('type', models.ForeignKey(
                    to='budgetwise.OperationType',
                    on_delete=django.db.models.deletion.PROTECT,
                    db_column='type',
                    related_name='transactions',
                    help_text='Ссылка на тип операции (0=Доход, 1=Расход)'
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Время создания записи')),
                ('category', models.ForeignKey(
                    to='budgetwise.Category',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='transactions',
                    help_text='Категория транзакции'
                )),
                ('user', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='transactions'
                )),
            ],
        ),

        # 4) Position
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, help_text='Наименование позиции')),
                ('quantity', models.PositiveIntegerField(help_text='Количество')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2, help_text='Цена за 1 шт.')),
                ('sum', models.DecimalField(max_digits=12, decimal_places=2, help_text='Сумма')),
                ('category', models.ForeignKey(
                    to='budgetwise.Category',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='positions',
                    help_text='Категория позиции'
                )),
                ('transaction', models.ForeignKey(
                    to='budgetwise.Transaction',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='positions'
                )),
            ],
        ),

        # 5) Balance
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Текущий баланс пользователя')),
                ('user', models.OneToOneField(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='balance'
                )),
            ],
        ),

        # Seed operation types, categories and superuser
        migrations.RunPython(create_operation_types, delete_operation_types),
        migrations.RunPython(create_initial_categories, delete_initial_categories),
        migrations.RunPython(create_admin_user, delete_admin_user),
    ]
