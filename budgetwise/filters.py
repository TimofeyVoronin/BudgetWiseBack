import django_filters
from django.db.models import Q
from .models import Transaction, Position, Category

class TransactionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    category = django_filters.NumberFilter(field_name='category__id', lookup_expr='exact')
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact')
    search = django_filters.CharFilter(method='filter_search', label='Поиск')

    class Meta:
        model = Transaction
        fields = ['date', 'category', 'type', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(positions__name__icontains=value) |
            Q(category__name__icontains=value)
        ).distinct()


class PositionFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id', lookup_expr='exact')
    product_type = django_filters.CharFilter(field_name='product_type', lookup_expr='exact')
    search = django_filters.CharFilter(method='filter_search', label='Поиск')

    class Meta:
        model = Position
        fields = ['category', 'product_type', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(product_type__icontains=value)
        )


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Название содержит')
    parent = django_filters.NumberFilter(field_name='parent__id', lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['name', 'parent']