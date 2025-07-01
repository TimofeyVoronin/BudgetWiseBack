from rest_framework import serializers
from rest_framework.fields import HiddenField
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import CurrentUserDefault
from .models import MyModel, Transaction

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'date', 'category', 'type', 'user',)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительным числом.")
        return value
    
