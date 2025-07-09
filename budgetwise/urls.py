from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    TransactionViewSet,
    PositionViewSet,
    CategoryViewSet,
    ChequeViewSet
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'categories', CategoryViewSet, basename='categories')
transactions_router = routers.NestedDefaultRouter(router, r'transactions', lookup='transaction')
transactions_router.register(r'positions', PositionViewSet, basename='transaction-positions')
transactions_router.register(r'cheque', ChequeViewSet, basename='transaction-cheque')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(transactions_router.urls)),
]
