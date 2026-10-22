from decimal import Decimal
from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    CATEGORY_CHOICES = [('print','Printing'),('photo','Photo'),('large','Large Format'),('custom','Custom')]
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='print')
    description = models.TextField(blank=True)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['sort_order', 'name']
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name

class SizeOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    name = models.CharField(max_length=100)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order','name']
    def __str__(self): return f'{self.product.name} — {self.name}'

class PaperOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='papers')
    name = models.CharField(max_length=100)
    gsm = models.PositiveIntegerField(null=True, blank=True)
    multiplier = models.DecimalField(max_digits=7, decimal_places=3, default=Decimal('1.000'))
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order','name']
    def __str__(self): return f'{self.product.name} — {self.name}'

class PrintOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='printing_options')
    name = models.CharField(max_length=100)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order','name']
    def __str__(self): return f'{self.product.name} — {self.name}'

class FinishingOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='finishing_options')
    name = models.CharField(max_length=100)
    fixed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    per_unit_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order','name']
    def __str__(self): return f'{self.product.name} — {self.name}'

class QuantityPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quantity_prices')
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    fixed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    active = models.BooleanField(default=True)
    class Meta: ordering = ['min_quantity']
    def __str__(self): return f'{self.product.name}: {self.min_quantity}+' 
