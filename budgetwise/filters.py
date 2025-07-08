import django_filters
from django_filters import DateFromToRangeFilter
from django.db.models import Q
from .models import Transaction, Position, Category

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class TransactionFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter(
        field_name='date',
        label='Дата (диапазон)'
    )
    category = NumberInFilter(
        field_name='category__id', 
        lookup_expr='in', 
        label='Категория (несколько через запятую)'
    )
    type = NumberInFilter(
        field_name='type', 
        lookup_expr='in', 
        label='Типы (несколько через запятую)'
    )
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Поиск по позициям/категориям'
    )

    class Meta:
        model  = Transaction
        fields = ('date', 'category', 'type')

    def filter_search(self, queryset, name, value):
        qs = queryset.select_related('category', 'user') \
                .prefetch_related('positions', 'positions__category')
        return qs.filter(
            Q(positions__name__icontains=value) |
            Q(category__name__icontains=value)
        ).distinct()

class PositionFilter(django_filters.FilterSet):
    category = NumberInFilter(
        field_name='category__id', 
        lookup_expr='in', 
        label='Категории (несколько через запятую)'
    )
    product_type = django_filters.CharFilter(
        field_name='product_type', 
        lookup_expr='exact', 
        label='Тип продукта'
    )
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Поиск по названию/типу'
    )

    class Meta:
        model = Position
        fields = ('category', 'product_type')

    def filter_search(self, queryset, name, value):
        qs = queryset.select_related('category', 'transaction') \
                     .prefetch_related('transaction__category')

        return qs.filter(
            Q(name__icontains=value) |
            Q(product_type__icontains=value)
        )


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', 
        lookup_expr='icontains', 
        label='Название содержит'
    )
    parent = NumberInFilter(
        field_name='parent__id', 
        lookup_expr='in', 
        label='Родительские категории (несколько через запятую)'
    )

    class Meta:
        model = Category
        fields = ('name', 'parent')