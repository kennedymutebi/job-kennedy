from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from core.permissions import IsManager, IsSalesperson

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'sku', 'description']
    filterset_fields = ['category', 'is_active']
    
    def get_permissions(self):
        """Allow salespeople to view products but not modify them"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsSalesperson]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Return products with low stock levels"""
        from inventory.models import InventoryItem
        
        # Get products where stock level is below threshold
        low_stock_items = InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level')
        ).select_related('product')
        
        products = [item.product for item in low_stock_items]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

