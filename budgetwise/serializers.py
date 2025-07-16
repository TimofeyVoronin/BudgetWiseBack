from rest_framework import serializers
from rest_framework.fields import HiddenField
from rest_framework.serializers import CurrentUserDefault
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Transaction, Position, Category, OperationType

@extend_schema_serializer(
    component_name='OperationType',
    examples=[
        OpenApiExample(
            'Тип операции',
            summary='Пример объекта OperationType',
            value={'id': 0, 'name': 'Доход'},
            response_only=True
        )
    ]
)
class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = ('id', 'name')


@extend_schema_serializer(
    component_name='TransactionCreate',
    examples=[
        OpenApiExample(
            'Запрос на создание транзакции',
            summary='Create Transaction',
            value={
                "date": "2025-07-16",
                "category": 3,
                "amount": "1500.00",
                "type": 1
            },
            request_only=True
        ),
        OpenApiExample(
            'Ответ после создания',
            summary='Created Transaction',
            value={
                "id": 10,
                "date": "2025-07-16",
                "category": 3,
                "amount": "1500.00",
                "type": 1,
                "created_at": "2025-07-16T08:30:00Z",
                "user": 5
            },
            response_only=True
        )
    ]
)
class TransactionCreateSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'category', 'amount', 'type', 'created_at', 'user')
        read_only_fields = ('created_at',)


@extend_schema_serializer(
    component_name='Position',
    examples=[
        OpenApiExample(
            'Позиция чека',
            summary='Пример позиции',
            value={
                "id": 1,
                "transaction": 10,
                "category": 3,
                "name": "Хлеб",
                "quantity": 2,
                "price": "50.00",
                "sum": "100.00"
            },
            response_only=True
        )
    ]
)
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'transaction', 'category', 'name', 'quantity', 'price', 'sum')
        read_only_fields = ('sum',)


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


@extend_schema_serializer(
    component_name='CategoryDetail',
    examples=[
        OpenApiExample(
            'Детальная категория',
            summary='Category Detail',
            value={
                "id": 3,
                "name": "Продукты",
                "description": "Еда и напитки",
                "parent": None,
                "subcategories": [
                    {"id": 4, "name": "Овощи"},
                    {"id": 5, "name": "Фрукты"}
                ]
            },
            response_only=True
        )
    ]
)
class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )
    subcategories = SimpleCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'subcategories')


@extend_schema_serializer(
    component_name='TransactionDetail',
    examples=[
        OpenApiExample(
            'Детальная транзакция',
            summary='Transaction Detail',
            value={
                "id": 10,
                "user": "ivan@example.com",
                "date": "2025-07-16",
                "category": {"id": 3, "name": "Продукты"},
                "amount": "1500.00",
                "type": 1,
                "created_at": "2025-07-16T08:30:00Z",
                "positions": [
                    {
                        "id": 1,
                        "transaction": 10,
                        "category": 3,
                        "name": "Хлеб",
                        "quantity": 2,
                        "price": "50.00",
                        "sum": "100.00"
                    }
                ]
            },
            response_only=True
        )
    ]
)
class TransactionDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    category = SimpleCategorySerializer(read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'date', 'category', 'amount', 'type', 'created_at', 'positions')
        read_only_fields = ('created_at',)
