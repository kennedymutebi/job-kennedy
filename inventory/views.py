from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from inventory.models import (
    InventoryItem, InventoryTransaction, 
    Supplier, Purchase, PurchaseItem
)
from inventory.serializers import (
    InventoryItemSerializer, InventoryTransactionSerializer,
    SupplierSerializer, PurchaseSerializer, PurchaseItemSerializer
)
from core.permissions import IsManager, IsSalesperson

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['product__name', 'product__sku']
    filterset_fields = ['product__category']
    
    def get_permissions(self):
        """Allow salespeople to view inventory but not modify it