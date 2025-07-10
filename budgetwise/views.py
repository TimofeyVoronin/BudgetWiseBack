import os
import tempfile
from decimal import Decimal

from django.http import HttpResponse
from django.utils.dateparse import parse_datetime

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction, Position, Category
from .serializers import (
    TransactionCreateSerializer,
    TransactionDetailSerializer,
    PositionSerializer,
    CategorySerializer
)
from .permissions import IsOwnerOrReadOnly
from .filters import TransactionFilter, PositionFilter, CategoryFilter
from .chequeInfo import ChequeInfo


def index(request):
    return HttpResponse("Hello, it's homepage")


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


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CategoryFilter
    ordering_fields = ('name',)
    ordering = ('name',)


class ChequeViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def upload(self, request, transaction_pk=None):
        qrfile = request.FILES.get('qrfile')
        if not qrfile:
            return Response(
                {"error": "Нужно прислать файл под ключом qrfile"},
                status=status.HTTP_400_BAD_REQUEST
            )
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(qrfile.name)[1])
        for chunk in qrfile.chunks():
            tmp.write(chunk)
        tmp.close()
        parser = ChequeInfo()
        try:
            parser.setQRImage(tmp.name)
            data = parser.getDistProducts()
        except Exception as e:
            os.remove(tmp.name)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)

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
            type=1,
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