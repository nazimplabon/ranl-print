from django.db import models
from orders.models import Order
class JobCard(models.Model):
    STATUS=[('queued','Queued'),('printing','Printing'),('finishing','Finishing'),('qc','Quality Check'),('complete','Complete')]
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name='job_card')
    status=models.CharField(max_length=20,choices=STATUS,default='queued')
    assigned_to=models.CharField(max_length=120,blank=True)
    machine=models.CharField(max_length=120,blank=True)
    material=models.CharField(max_length=160,blank=True)
    quantity=models.PositiveIntegerField(default=1)
    due_date=models.DateField(null=True,blank=True)
    notes=models.TextField(blank=True)
    started_at=models.DateTimeField(null=True,blank=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return f'JOB-{self.order.order_number}'
