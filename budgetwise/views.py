from django.http import HttpResponse
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction, Position, Category
from .serializers import TransactionSerializer, PositionSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from .filters import TransactionFilter, PositionFilter, CategoryFilter

def index(request):
    return HttpResponse("Hello, it's homepage")

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TransactionFilter
    ordering_fields = ('date', 'created_at')
    ordering = ('-date',)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def positions(self, request, pk=None):
        txn = self.get_object()
        qs = txn.positions.all()
        search = request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        serializer = PositionSerializer(qs, many=True)
        return Response(serializer.data)

class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PositionFilter
    ordering_fields = ('quantity', 'price')
    ordering = ('-quantity',)

    def get_queryset(self):
        return Position.objects.filter(
            transaction__user=self.request.user
        )

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CategoryFilter
    ordering_fields = ('name',)
    ordering = ('name',)
