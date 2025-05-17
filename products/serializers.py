from rest_framework import serializers
from products.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    profit_margin = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'category', 'category_name', 'description', 
                 'price', 'cost_price', 'profit_margin', 'image', 'is_active', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

