import os
import tempfile
from decimal import Decimal

from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.db.models import Sum, Case, When, F, DecimalField

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction, Position, Category, Balance, OperationType
from .serializers import (
    TransactionCreateSerializer,
    TransactionDetailSerializer,
    PositionSerializer,
    CategorySerializer,
    OperationTypeSerializer,
    ChequeUploadSerializer
)
from .permissions import IsOwnerOrReadOnly
from .filters import TransactionFilter, PositionFilter, CategoryFilter
from .chequeInfo import ChequeInfo
from drf_spectacular.utils import extend_schema


def index(request):
    return HttpResponse("Hello, it's homepage")

@extend_schema(tags=['Transactions'])
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = TransactionCreateSerializer
    queryset = Transaction.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TransactionFilter
    ordering_fields = ('date', 'created_at')
    ordering = ('-date',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='balance')
    def balance(self, request):
        qs = self.get_queryset()
        agg = qs.aggregate(
            balance=Sum(
                Case(
                    When(type=0, then=F('amount')),
                    When(type=1, then=-F('amount')),
                    output_field=DecimalField()
                )
            )
        )
        balance = agg['balance'] or 0

        return Response({'balance': balance})
    
    @action(detail=False, methods=['get'], url_path='balance')
    def balance(self, request):
        bal_obj, _ = Balance.objects.get_or_create(user=request.user)
        return Response({'balance': bal_obj.amount})

@extend_schema(tags=['Positions'])
class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PositionFilter
    ordering_fields = ('quantity', 'price')
    ordering = ('-quantity',)

    def get_queryset(self):
        return super().get_queryset().filter(transaction__user=self.request.user)

@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CategoryFilter
    ordering_fields = ('name',)
    ordering = ('name',)

@extend_schema(tags=['Cheques'],
    request=ChequeUploadSerializer,
    responses={201: TransactionDetailSerializer},
    description="Загружает файл qrfile, парсит чек и создаёт транзакцию с позициями")
class ChequeViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def upload(self, request, transaction_pk=None):
        qrfile = request.FILES.get('qrfile')
        if not qrfile:
            return Response(
                {"error": "Нужно прислать файл под ключом qrfile"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qrfile = request.FILES["qrfile"]
        raw = qrfile.read()
        parser = ChequeInfo()
        try:
            parser.setQRImageFromBytes(raw, qrfile.name)
            data = parser.getDistProducts()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        dt = parse_datetime(data.get('data'))
        total_sum = sum(item.get('sum', 0) for item in data.get('items', []))
        total_amount = Decimal(total_sum) / 100
        default_cat, _ = Category.objects.get_or_create(
            name='Без категории',
            defaults={'description': 'Автоматически созданная категория'}
        )

        transaction = Transaction.objects.create(
            user=request.user,
            date=dt.date() if dt else None,
            category=default_cat,
            amount=total_amount,
            type_id=1,
        )
                
        position_objs = []
        for item in data.get('items', []):
            price_pc = item.get('price', 0) or 0
            qty = item.get('quantity', 0) or 0
            sum_pc = item.get('sum', price_pc * qty)
            position_objs.append(
                Position(
                    transaction=transaction,
                    category=default_cat,
                    name=item.get('name', '') or '',
                    quantity=item.get('quantity', 0) or 0,
                    price=Decimal(price_pc) / 100,
                    sum = Decimal(sum_pc) / 100
                )
            )
        Position.objects.bulk_create(position_objs)
        
         

        out = TransactionDetailSerializer(transaction)
        return Response(out.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['OperationTypes'])
class OperationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationType.objects.all().order_by('id')
    serializer_class = OperationTypeSerializer
