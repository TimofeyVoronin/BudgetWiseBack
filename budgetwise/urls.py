from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, PositionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'positions', PositionViewSet, basename='positions')

urlpatterns = [
    path('', include(router.urls)),
]
