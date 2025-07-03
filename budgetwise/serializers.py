from rest_framework import serializers
from rest_framework.fields import HiddenField
from rest_framework.serializers import CurrentUserDefault
from .models import Transaction, Position, Category


class CategorySerializer(serializers.ModelSerializer):
    # Отдаём родительскую категорию по её ID (или None)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    # Генерируем поле subcategories из related_name
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'subcategories')

    def get_subcategories(self, obj):
        # возвращаем упрощённый список {id, name} дочерних категорий
        return [{'id': c.id, 'name': c.name} for c in obj.subcategories.all()]


class PositionSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Position
        fields = ('id', 'transaction', 'category', 'name', 'product_type', 'quantity', 'price', 'sum')
        read_only_fields = ('sum',)


class TransactionSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    positions = PositionSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'category', 'type', 'created_at', 'user', 'positions')

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        txn = Transaction.objects.create(**validated_data)
        for pos in positions_data:
            Position.objects.create(transaction=txn, **pos)
        return txn

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.positions.all().delete()
        for pos in positions_data:
            Position.objects.create(transaction=instance, **pos)
        return instance
