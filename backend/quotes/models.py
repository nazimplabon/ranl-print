import uuid
from django.core.validators import FileExtensionValidator
from django.db import models
from catalog.models import Product

class Quote(models.Model):
    STATUS = [('new','New'),('reviewing','Reviewing'),('quoted','Quoted'),('approved','Approved'),('closed','Closed')]
    quote_number = models.CharField(max_length=30, unique=True, editable=False)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='quotes')
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=120, blank=True)
    paper = models.CharField(max_length=120, blank=True)
    printing = models.CharField(max_length=120, blank=True)
    finishing = models.JSONField(default=list, blank=True)
    artwork = models.FileField(upload_to='quote-artwork/%Y/%m/', blank=True, null=True,
        validators=[FileExtensionValidator(['pdf','jpg','jpeg','png','ai','psd'])])
    notes = models.TextField(blank=True)
    estimated_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if not self.quote_number:
            self.quote_number = 'RANL-' + uuid.uuid4().hex[:8].upper()
        super().save(*args,**kwargs)
    def __str__(self): return self.quote_number
