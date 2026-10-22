from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[('orders','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
      migrations.CreateModel(name='Payment',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('amount',models.DecimalField(decimal_places=2,max_digits=12)),('method',models.CharField(choices=[('cash','Cash'),('bkash','bKash'),('nagad','Nagad'),('bank','Bank Transfer'),('card','Card'),('other','Other')],default='cash',max_length=20)),('reference',models.CharField(blank=True,max_length=120)),('paid_at',models.DateTimeField(auto_now_add=True)),('note',models.CharField(blank=True,max_length=255)),('order',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='payments',to='orders.order')),('received_by',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name='Expense',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=160)),('category',models.CharField(choices=[('material','Materials'),('ink','Ink/Toner'),('paper','Paper'),('delivery','Delivery'),('salary','Salary'),('rent','Rent'),('utility','Utilities'),('marketing','Marketing'),('maintenance','Maintenance'),('other','Other')],default='other',max_length=30)),('amount',models.DecimalField(decimal_places=2,max_digits=12)),('expense_date',models.DateField()),('vendor',models.CharField(blank=True,max_length=160)),('note',models.TextField(blank=True)),('created_at',models.DateTimeField(auto_now_add=True))]),
    ]
