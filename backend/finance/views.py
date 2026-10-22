from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from orders.models import Order
from inventory.models import MaterialUsage
from .models import Expense, Payment

@staff_member_required
@require_GET
def financial_summary(request):
    if not request.user.has_perm('finance.view_expense') or not request.user.has_perm('finance.view_payment'):
        return HttpResponseForbidden('You do not have finance access.')
    active = Order.objects.exclude(status='cancelled')
    sales = active.aggregate(v=Sum('total'))['v'] or Decimal('0')
    collected = Payment.objects.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    expenses = Expense.objects.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    material_cost = MaterialUsage.objects.filter(job_card__order__in=active).aggregate(v=Sum('total_cost'))['v'] or Decimal('0')
    return JsonResponse({'sales':str(sales),'collected':str(collected),'expenses':str(expenses),'material_cost':str(material_cost),'gross_profit':str(sales-material_cost),'net_profit':str(sales-material_cost-expenses),'cash_flow_after_expenses':str(collected-expenses),'receivable':str(active.aggregate(v=Sum('due_amount'))['v'] or 0)})

@staff_member_required
def invoice(request, order_id):
    if not request.user.has_perm('orders.view_order'):
        return HttpResponseForbidden('You do not have permission to view invoices.')
    order=get_object_or_404(Order.objects.select_related('customer').prefetch_related('items__product','payments'),pk=order_id)
    return render(request,'invoice.html',{'order':order,'payments':order.payments.order_by('paid_at')})
