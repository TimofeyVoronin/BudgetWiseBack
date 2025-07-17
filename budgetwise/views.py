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
        # Показать только транзакции текущего пользователя
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='balance')
    def balance(self, request):
        # Возвращает текущий баланс пользователя
        bal_obj, _ = Balance.objects.get_or_create(user=request.user)
        return Response({'balance': bal_obj.amount})

    @action(
        detail=True,
        methods=['patch'],
        url_path='set-category',
        description="Меняет категорию транзакции по её ID"
    )
    def set_category(self, request, pk=None):
        """
        PATCH /api/transactions/{pk}/set-category/
        Body: { "category_id": <int> }
        """
        tx = self.get_object()
        cat_id = request.data.get('category_id')
        if cat_id is None:
            return Response(
                {"detail": "Нужно передать category_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            category = Category.objects.get(pk=cat_id)
        except Category.DoesNotExist:
            return Response(
                {"detail": f"Категория с id={cat_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
        tx.category = category
        tx.save(update_fields=['category'])
        out = TransactionDetailSerializer(tx, context={'request': request})
        return Response(out.data, status=status.HTTP_200_OK)


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
        # Только позиции транзакций текущего пользователя
        return super().get_queryset().filter(transaction__user=self.request.user)

    @action(
        detail=False,
        methods=['patch'],
        url_path='bulk-set-category',
        description="Меняет категории сразу у нескольких позиций"
    )
    def bulk_set_category(self, request):
        """
        PATCH /api/positions/bulk-set-category/
        Body: [
          { "position_id": 1, "category_id": 3 },
          { "position_id": 2, "category_id": 5 },
          …
        ]
        """
        payload = request.data
        if not isinstance(payload, list):
            return Response(
                {"detail": "Ожидается список объектов"},
                status=status.HTTP_400_BAD_REQUEST
            )

        to_update = []
        for idx, item in enumerate(payload):
            pos_id = item.get('position_id')
            cat_id = item.get('category_id')

            if pos_id is None or cat_id is None:
                return Response(
                    {"detail": f"В элементе #{idx} отсутствуют position_id или category_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                pos = Position.objects.get(pk=pos_id, transaction__user=request.user)
            except Position.DoesNotExist:
                return Response(
                    {"detail": f"Позиция с id={pos_id} не найдена или не принадлежит вам"},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                cat = Category.objects.get(pk=cat_id)
            except Category.DoesNotExist:
                return Response(
                    {"detail": f"Категория с id={cat_id} не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )

            pos.category = cat
            to_update.append(pos)

        Position.objects.bulk_update(to_update, ['category'])
        serializer = PositionSerializer(to_update, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CategoryFilter
    ordering_fields = ('name',)
    ordering = ('name',)


@extend_schema(
    tags=['Cheques'],
    request=ChequeUploadSerializer,
    responses={201: TransactionDetailSerializer},
    description="Загружает файл qrfile, парсит чек и создаёт транзакцию с позициями"
)
class ChequeViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def upload(self, request, transaction_pk=None):
        qrfile = request.FILES.get('qrfile')
        if not qrfile:
            return Response(
                {"error": "Нужно прислать файл под ключом qrfile"},
                status=status.HTTP_400_BAD_REQUEST
            )
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
                    quantity=qty,
                    price=Decimal(price_pc) / 100,
                    sum=Decimal(sum_pc) / 100
                )
            )
        Position.objects.bulk_create(position_objs)

        out = TransactionDetailSerializer(transaction, context={'request': request})
        return Response(out.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['OperationTypes'])
class OperationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationType.objects.all().order_by('id')
    serializer_class = OperationTypeSerializer
