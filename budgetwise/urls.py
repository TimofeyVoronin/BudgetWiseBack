from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .chequeInfo import ChequeInfo
from .views import TransactionViewSet, PositionViewSet, CategoryViewSet, ChequeViewSet


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'positions', PositionViewSet, basename='positions')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'cheque',ChequeViewSet,basename='cheque')

urlpatterns = [
    path('', include(router.urls)),
]
