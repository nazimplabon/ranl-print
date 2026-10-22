from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('catalog','0001_initial')]
    operations = [migrations.CreateModel(name='Quote', fields=[
        ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
        ('quote_number',models.CharField(editable=False,max_length=30,unique=True)),('name',models.CharField(max_length=120)),('phone',models.CharField(max_length=30)),('email',models.EmailField(blank=True,max_length=254)),('quantity',models.PositiveIntegerField()),('size',models.CharField(blank=True,max_length=120)),('paper',models.CharField(blank=True,max_length=120)),('printing',models.CharField(blank=True,max_length=120)),('finishing',models.JSONField(blank=True,default=list)),('artwork',models.FileField(blank=True,null=True,upload_to='quote-artwork/%Y/%m/',validators=[django.core.validators.FileExtensionValidator(['pdf','jpg','jpeg','png','ai','psd'])])),('notes',models.TextField(blank=True)),('estimated_price',models.DecimalField(blank=True,decimal_places=2,max_digits=12,null=True)),('status',models.CharField(choices=[('new','New'),('reviewing','Reviewing'),('quoted','Quoted'),('approved','Approved'),('closed','Closed')],default='new',max_length=20)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('product',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='quotes',to='catalog.product')),
    ])]
