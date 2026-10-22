from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[('orders','0001_initial')]
    operations=[migrations.CreateModel(name='JobCard',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('status',models.CharField(choices=[('queued','Queued'),('printing','Printing'),('finishing','Finishing'),('qc','Quality Check'),('complete','Complete')],default='queued',max_length=20)),('assigned_to',models.CharField(blank=True,max_length=120)),('machine',models.CharField(blank=True,max_length=120)),('material',models.CharField(blank=True,max_length=160)),('quantity',models.PositiveIntegerField(default=1)),('due_date',models.DateField(blank=True,null=True)),('notes',models.TextField(blank=True)),('started_at',models.DateTimeField(blank=True,null=True)),('completed_at',models.DateTimeField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('order',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name='job_card',to='orders.order'))])]
