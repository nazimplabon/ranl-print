from decimal import Decimal
from django.db import models
from catalog.models import Product
from quotes.models import Quote

class Customer(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return f'{self.name} — {self.phone}'

class Order(models.Model):
    STATUS = [
        ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('production', 'In Production'),
        ('quality', 'Quality Check'), ('ready', 'Ready for Delivery'), ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS = [('unpaid','Unpaid'),('partial','Partially Paid'),('paid','Paid'),('refunded','Refunded')]
    DELIVERY_STATUS = [('not_ready','Not Ready'),('ready','Ready'),('dispatched','Dispatched'),('delivered','Delivered')]
    order_number = models.CharField(max_length=30, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    quote = models.OneToOneField(Quote, on_delete=models.SET_NULL, null=True, blank=True, related_name='order')
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='not_ready')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    due_date = models.DateField(null=True, blank=True)
    delivery_address = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = 'RANL-' + uuid.uuid4().hex[:8].upper()
        self.total = max(Decimal('0'), self.subtotal - self.discount + self.delivery_fee)
        self.due_amount = max(Decimal('0'), self.total - self.paid_amount)
        if self.total and self.due_amount == 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        super().save(*args, **kwargs)
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=4)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    selected_options = models.JSONField(default=dict, blank=True)
    def save(self, *args, **kwargs):
        self.total_price = (self.unit_price * self.quantity).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.product.name} × {self.quantity}'
