from decimal import Decimal
from django.conf import settings
from django.db import models
from orders.models import Order

class Payment(models.Model):
    METHOD = [('cash','Cash'),('bkash','bKash'),('nagad','Nagad'),('bank','Bank Transfer'),('card','Card'),('other','Other')]
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD, default='cash')
    reference = models.CharField(max_length=120, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=255, blank=True)
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        total_paid = self.order.payments.exclude(pk=self.pk).aggregate(v=models.Sum('amount'))['v'] or Decimal('0')
        self.order.paid_amount = total_paid + self.amount
        self.order.save(update_fields=['paid_amount','payment_status','due_amount','updated_at'])
    def __str__(self): return f'{self.order.order_number} — {self.amount}'

class Expense(models.Model):
    CATEGORY = [('material','Materials'),('ink','Ink/Toner'),('paper','Paper'),('delivery','Delivery'),('salary','Salary'),('rent','Rent'),('utility','Utilities'),('marketing','Marketing'),('maintenance','Maintenance'),('other','Other')]
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=30, choices=CATEGORY, default='other')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense_date = models.DateField()
    vendor = models.CharField(max_length=160, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-expense_date','-id']
    def __str__(self): return f'{self.title} — {self.amount}'
