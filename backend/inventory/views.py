from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from orders.models import Order
from .models import Material, MaterialUsage

def allowed(user):
    return user.is_superuser or user.has_perm('inventory.view_material') or user.groups.filter(name__in=['Owner','Manager','Accounts','Production']).exists()

@staff_member_required
def order_cost(request,order_id):
    if not allowed(request.user): return JsonResponse({'detail':'Forbidden'},status=403)
    order=get_object_or_404(Order,pk=order_id)
    usages=MaterialUsage.objects.filter(job_card__order=order).select_related('material')
    material_cost=sum((u.total_cost for u in usages),Decimal('0'))
    revenue=order.total
    profit=revenue-material_cost
    return JsonResponse({'order':order.order_number,'revenue':str(revenue),'material_cost':str(material_cost),'gross_profit_before_overheads':str(profit),'margin_percent':str(((profit/revenue)*100).quantize(Decimal('0.01')) if revenue else Decimal('0')),'materials':[{'name':u.material.name,'quantity':str(u.quantity),'unit':u.material.unit,'cost':str(u.total_cost)} for u in usages]})
