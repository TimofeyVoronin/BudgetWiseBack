from django.db import migrations

def populate_descriptions(apps, schema_editor):
    Category = apps.get_model('budgetwise', 'Category')
    mapping = {
        'Обязательные расходы': """Коммунальные платежи – это платежи предприятий, организаций и отдельных лиц за содержание и обслуживание жилья.
Плата за квартиру, телефон, электроэнергию, водоснабжение и т. д.
Образовательные платежи: содержание детей в детских садах, обучение в музыкальной школе, плата за высшее обучение и т. д.
Выплата кредитов, процентов по ссудам и т. д.""",

        'Расходы на питание': """Приобретение продуктов в магазинах и на рынке, заготовка продуктов впрок.
Оплата питания в кафе, ресторанах, столовых.""",

        'Расходы на хозяйственно-бытовые нужды': """Затраты на ремонт одежды, обуви, бытовой техники, квартиры, теле-радиоаппаратуры, химчистку, прачечную.
Покупка предметов личной гигиены.""",

        'Расходы на предметы личного пользования': """Верхняя одежда, белье, обувь, постельные принадлежности.""",

        'Расходы на предметы быта': """Мебель, светильники, ковровые изделия, картины, часы, хрусталь и т. д.""",
    }

    for name, desc in mapping.items():
        try:
            cat = Category.objects.get(name=name)
            cat.description = desc
            cat.save()
        except Category.DoesNotExist:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('budgetwise', '0012_alter_category_parent'),
    ]

    operations = [
        migrations.RunPython(populate_descriptions, reverse_code=migrations.RunPython.noop),
    ]
