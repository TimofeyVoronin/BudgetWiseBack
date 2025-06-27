from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MyModel
from .serializers import MyModelSerializer

def index(request):
    return HttpResponse("Hello, it's homepage")

class MyModelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

class MyModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
