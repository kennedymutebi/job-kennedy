from rest_framework import serializers
from inventory.models import (
    InventoryItem, InventoryTransaction, 
    Supplier, Purchase, PurchaseItem
)

class InventoryItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    stock_value = serializers.ReadOnlyField()
    needs_reorder = serializers.ReadOnlyField()
    
    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'product_name', 'quantity', 'reorder_level', 
                 'stock_value', 'needs_reorder', 'last_updated']
        read_only_fields = ['last_updated']

class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    performed_by_username = serializers.ReadOnlyField(source='performed_by.username')
    
    class Meta:
        model = InventoryTransaction
        fields = ['id', 'product', 'product_name', 'transaction_type', 'quantity',
                 'reference', 'transaction_date', 'performed_by', 'performed_by_username', 'notes']
        read_only_fields = ['transaction_date']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'email', 'phone', 'address', 
                 'is_active', 'created_at']
        read_only_fields = ['created_at']

class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = PurchaseItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'total_price']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Purchase
        fields = ['id', 'supplier', 'supplier_name', 'purchase_date', 'reference_number',
                 'created_by', 'created_by_username', 'notes', 'total_amount', 'items']
        read_only_fields = ['purchase_date', 'total_amount', 'created_by']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['created_by'] = self.context['request'].user
        
        purchase = Purchase.objects.create(**validated_data)
        
        # Create purchase items
        for item_data in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item_data)
            
            # Update inventory
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Update or create inventory item
            inventory_item, created = InventoryItem.objects.get_or_create(
                product=product,
                defaults={'quantity': 0}
            )
            inventory_item.quantity += quantity
            inventory_item.save()
            
            # Create inventory transaction
            InventoryTransaction.objects.create(
                product=product,
                transaction_type='purchase',
                quantity=quantity,
                reference=f"Purchase #{purchase.reference_number}",
                performed_by=self.context['request'].user,
                notes=f"Purchase from {purchase.supplier.name}"
            )
        
        return purchase

