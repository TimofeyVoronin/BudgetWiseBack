from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction, Position, Category
from .serializers import (
    TransactionCreateSerializer,
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
    serializer_class   = TransactionCreateSerializer
    queryset           = Transaction.objects.all()
    filter_backends    = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class    = TransactionFilter
    ordering_fields    = ('date', 'created_at')
    ordering           = ('-date',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class   = PositionSerializer
    queryset           = Position.objects.all()
    filter_backends    = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class    = PositionFilter
    ordering_fields    = ('quantity', 'price')
    ordering           = ('-quantity',)

    def get_queryset(self):
        return super().get_queryset().filter(transaction__user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class   = CategorySerializer
    queryset           = Category.objects.all()
    filter_backends    = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class    = CategoryFilter
    ordering_fields    = ('name',)
    ordering           = ('name',)


class ChequeViewSet(viewsets.ViewSet):
    """
    Примитивный ViewSet для обработки чеков:
      - POST /api/cheque/upload/ — загрузить изображение QR-кода и получить данные
      - GET  /api/cheque/last/   — вернуть последний распознанный чек
    """
    last_data = {}

    @action(detail=False, methods=['post'])
    def upload(self, request):
        qrfile = request.FILES.get('qrfile')
        if not qrfile:
            return Response(
                {"error": "Нужно прислать файл под ключом qrfile"},
                status=status.HTTP_400_BAD_REQUEST
            )

        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(qrfile.name)[1])
        for chunk in qrfile.chunks():
            tmp.write(chunk)
        tmp.close()
        print("Hello")
        parser = ChequeInfo()
        try:
            parser.setQRImage(tmp.name)
            data = parser.getDistProducts()
        except Exception as e:
            os.remove(tmp.name)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        os.remove(tmp.name)
        ChequeViewSet.last_data = data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def last(self, request):
        if not ChequeViewSet.last_data:
            return Response({"detail": "Нет распознанных чеков"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ChequeViewSet.last_data, status=status.HTTP_200_OK)