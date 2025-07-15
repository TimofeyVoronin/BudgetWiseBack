from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    TransactionViewSet,
    PositionViewSet,
    CategoryViewSet,
    ChequeViewSet,
    OperationTypeViewSet
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'categories', CategoryViewSet, basename='categories')
transactions_router = routers.NestedDefaultRouter(router, r'transactions', lookup='transaction')
transactions_router.register(r'positions', PositionViewSet, basename='transaction-positions')
router.register(r'cheques', ChequeViewSet, basename='cheques')
router.register(r'operation-types', OperationTypeViewSet, basename='operation-types')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(transactions_router.urls)),
]
