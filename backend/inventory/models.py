from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from orders.models import Order
from production.models import JobCard

class Supplier(models.Model):
    name=models.CharField(max_length=160)
    phone=models.CharField(max_length=40,blank=True)
    email=models.EmailField(blank=True)
    address=models.TextField(blank=True)
    notes=models.TextField(blank=True)
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Material(models.Model):
    UNIT=[('sheet','Sheet'),('ream','Ream'),('meter','Meter'),('sqft','Sq Ft'),('roll','Roll'),('piece','Piece'),('kg','Kg'),('liter','Liter'),('unit','Unit')]
    name=models.CharField(max_length=160)
    sku=models.CharField(max_length=60,unique=True,null=True,blank=True)
    category=models.CharField(max_length=80,blank=True)
    unit=models.CharField(max_length=20,choices=UNIT,default='piece')
    current_stock=models.DecimalField(max_digits=14,decimal_places=3,default=Decimal('0'))
    reorder_level=models.DecimalField(max_digits=14,decimal_places=3,default=Decimal('0'))
    average_cost=models.DecimalField(max_digits=14,decimal_places=4,default=Decimal('0'))
    active=models.BooleanField(default=True)
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['name']
    def __str__(self): return f'{self.name} ({self.unit})'

class Purchase(models.Model):
    STATUS=[('draft','Draft'),('received','Received'),('cancelled','Cancelled')]
    supplier=models.ForeignKey(Supplier,on_delete=models.PROTECT,related_name='purchases')
    invoice_number=models.CharField(max_length=100,blank=True)
    purchase_date=models.DateField(default=timezone.localdate)
    status=models.CharField(max_length=20,choices=STATUS,default='draft')
    notes=models.TextField(blank=True)
    total=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal('0'))
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'PUR-{self.pk or "NEW"} — {self.supplier.name}'

class PurchaseItem(models.Model):
    purchase=models.ForeignKey(Purchase,on_delete=models.CASCADE,related_name='items')
    material=models.ForeignKey(Material,on_delete=models.PROTECT,related_name='purchase_items')
    quantity=models.DecimalField(max_digits=14,decimal_places=3)
    unit_cost=models.DecimalField(max_digits=14,decimal_places=4)
    total_cost=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal('0'))
    def save(self,*args,**kwargs):
        self.total_cost=(self.quantity*self.unit_cost).quantize(Decimal('0.01'))
        super().save(*args,**kwargs)
        self.purchase.total=self.purchase.items.aggregate(v=models.Sum('total_cost'))['v'] or Decimal('0')
        self.purchase.save(update_fields=['total'])

class StockMovement(models.Model):
    TYPES=[('purchase','Purchase'),('usage','Production Usage'),('adjustment','Adjustment'),('return','Return')]
    material=models.ForeignKey(Material,on_delete=models.PROTECT,related_name='movements')
    movement_type=models.CharField(max_length=20,choices=TYPES)
    quantity=models.DecimalField(max_digits=14,decimal_places=3)
    unit_cost=models.DecimalField(max_digits=14,decimal_places=4,default=Decimal('0'))
    purchase=models.ForeignKey(Purchase,null=True,blank=True,on_delete=models.SET_NULL,related_name='stock_movements')
    order=models.ForeignKey(Order,null=True,blank=True,on_delete=models.SET_NULL,related_name='stock_movements')
    job_card=models.ForeignKey(JobCard,null=True,blank=True,on_delete=models.SET_NULL,related_name='stock_movements')
    note=models.CharField(max_length=255,blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.material.name} {self.movement_type} {self.quantity}'

class MaterialUsage(models.Model):
    job_card=models.ForeignKey(JobCard,on_delete=models.CASCADE,related_name='material_usages')
    material=models.ForeignKey(Material,on_delete=models.PROTECT,related_name='usages')
    quantity=models.DecimalField(max_digits=14,decimal_places=3)
    unit_cost=models.DecimalField(max_digits=14,decimal_places=4)
    total_cost=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal('0'))
    note=models.CharField(max_length=255,blank=True)
    posted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.unit_cost: self.unit_cost=self.material.average_cost
        self.total_cost=(self.quantity*self.unit_cost).quantize(Decimal('0.01'))
        super().save(*args,**kwargs)
    def __str__(self): return f'{self.job_card} — {self.material.name}'
