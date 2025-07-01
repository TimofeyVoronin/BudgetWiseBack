from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MyModel, Transaction
from .serializers import MyModelSerializer, TransactionSerializer
from .permissions import IsOwnerOrReadOnly

def index(request):
    return HttpResponse("Hello, it's homepage")


class MyModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    @action(detail=False, methods=['get'], url_path='finance-page')
    def finance(self, request):
        return Response({
            "detail": "Вы видите защищённый ресурс!",
            "your_email": request.user.email,
        })
