from rest_framework import serializers
from rest_framework.fields import HiddenField
from rest_framework.serializers import CurrentUserDefault
from .models import Transaction, Position, Category, OperationType

class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = ('id', 'name')


class TransactionCreateSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'category', 'amount', 'type', 'created_at', 'user')
        read_only_fields = ('created_at',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'transaction', 'category', 'name', 'quantity', 'price', 'sum')
        read_only_fields = ('sum',)


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    subcategories = SimpleCategorySerializer(many=True, read_only=True)

    class Meta:
        model  = Category
        fields = ('id', 'name', 'description', 'parent', 'subcategories')

class TransactionDetailSerializer(serializers.ModelSerializer):
    user      = serializers.CharField(source='user.username', read_only=True)
    category  = SimpleCategorySerializer(read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model  = Transaction
        fields = ('id', 'user', 'date', 'category', 'amount', 'type', 'created_at', 'positions')
        read_only_fields = ('created_at',)
