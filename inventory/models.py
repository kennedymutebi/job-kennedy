from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models import Sum, F

class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"
    
    @property
    def stock_value(self):
        """Calculate the total value of the inventory item"""
        return self.quantity * self.product.cost_price
    
    @property
    def needs_reorder(self):
        """Check if the item needs to be reordered"""
        return self.quantity <= self.reorder_level
    
    class Meta:
        ordering = ['product__name']

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()  # Can be negative for sales/adjustments
    reference = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inventory_transactions')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} - Qty: {self.quantity}"
    
    class Meta:
        ordering = ['-transaction_date']

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Purchase {self.reference_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total amount
        self.total_amount = self.items.aggregate(
            total=Sum(F('quantity') * F('unit_price'), default=0)
        )['total'] or 0
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-purchase_date']

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price
`
