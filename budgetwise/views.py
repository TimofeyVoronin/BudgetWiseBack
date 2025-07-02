from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Transaction, Position
from .serializers import TransactionSerializer, PositionSerializer
from .permissions import IsOwnerOrReadOnly

def index(request):
    return HttpResponse("Hello, it's homepage")

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    @action(detail=True, methods=['get'])
    def positions(self, request, pk=None):
        txn = self.get_object()
        serializer = PositionSerializer(txn.positions.all(), many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PositionSerializer

    def get_queryset(self):
        return Position.objects.filter(
            transaction__user=self.request.user
        )
