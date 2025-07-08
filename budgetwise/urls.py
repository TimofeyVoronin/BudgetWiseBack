from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, PositionViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'positions', PositionViewSet, basename='positions')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]
