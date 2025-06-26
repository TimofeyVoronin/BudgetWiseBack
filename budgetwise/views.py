from rest_framework import generics
from django.shortcuts import render
from .models import MyModel
from .serializers import MyModelSerializer
from django.http import HttpResponse  

def index(request):
    return HttpResponse("Hello, it's homepage")
class MyModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

class MyModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
