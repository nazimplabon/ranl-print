from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model=OrderItem; extra=0
    fields=('product','description','quantity','unit_price','total_price','selected_options')
    readonly_fields=('total_price',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('name','company','phone','email','created_at')
    search_fields=('name','company','phone','email'); ordering=('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('order_number','customer','status','payment_status','delivery_status','total','paid_amount','due_amount','due_date','invoice_link','created_at')
    list_filter=('status','payment_status','delivery_status','due_date','created_at')
    search_fields=('order_number','customer__name','customer__phone','tracking_number','notes')
    readonly_fields=('order_number','total','due_amount','created_at','updated_at')
    list_editable=('status','payment_status','delivery_status'); date_hierarchy='created_at'; ordering=('-created_at',); inlines=[OrderItemInline]
    fieldsets=(('Order',{'fields':('order_number','customer','quote','status')}),('Money',{'fields':('subtotal','discount','delivery_fee','total','paid_amount','due_amount','payment_status')}),('Delivery',{'fields':('delivery_status','due_date','delivery_address','tracking_number')}),('Notes',{'fields':('notes',)}),('System',{'fields':('created_at','updated_at'),'classes':('collapse',)}))
    def invoice_link(self,obj):
        if not obj.pk:return '-'
        url=reverse('invoice',args=[obj.pk]); return format_html('<a href="{}" target="_blank">Invoice</a>',url)
    invoice_link.short_description='Invoice'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=('order','product','quantity','unit_price','total_price')
    search_fields=('order__order_number','product__name')
