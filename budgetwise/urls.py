from django.urls import path
from .views import MyModelListCreateAPIView, MyModelRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('items/', MyModelListCreateAPIView.as_view(), name='items-list-create'),
    path('items/<int:pk>/', MyModelRetrieveUpdateDestroyAPIView.as_view(), name='items-detail'),
]
