from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('catalog', '0001_initial'),
        ('quotes', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('company', models.CharField(blank=True, max_length=160)),
                ('address', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=30, unique=True)),
                ('status', models.CharField(choices=[('pending','Pending'),('confirmed','Confirmed'),('production','In Production'),('quality','Quality Check'),('ready','Ready for Delivery'),('delivered','Delivered'),('cancelled','Cancelled')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('unpaid','Unpaid'),('partial','Partially Paid'),('paid','Paid'),('refunded','Refunded')], default='unpaid', max_length=20)),
                ('delivery_status', models.CharField(choices=[('not_ready','Not Ready'),('ready','Ready'),('dispatched','Dispatched'),('delivered','Delivered')], default='not_ready', max_length=20)),
                ('subtotal', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('discount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('due_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('delivery_address', models.TextField(blank=True)),
                ('tracking_number', models.CharField(blank=True, max_length=80)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.customer')),
                ('quote', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='quotes.quote')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=4, max_digits=12)),
                ('total_price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('selected_options', models.JSONField(blank=True, default=dict)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.product')),
            ],
        ),
    ]
