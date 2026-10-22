import csv
from datetime import date, datetime
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET

from orders.models import Order, OrderItem, Customer
from finance.models import Payment, Expense
from inventory.models import MaterialUsage


def _range(request):
    today = date.today()
    try:
        start = datetime.strptime(request.GET.get('start', ''), '%Y-%m-%d').date() if request.GET.get('start') else today.replace(day=1)
        end = datetime.strptime(request.GET.get('end', ''), '%Y-%m-%d').date() if request.GET.get('end') else today
    except ValueError:
        start, end = today.replace(day=1), today
    if start > end:
        start, end = end, start
    return start, end


def _allowed(user):
    return user.is_staff and user.has_perm('orders.view_order')


@staff_member_required
@require_GET
def report_summary(request):
    if not _allowed(request.user):
        return HttpResponseForbidden('You do not have report access.')
    start, end = _range(request)
    orders = Order.objects.exclude(status='cancelled').filter(created_at__date__range=(start, end))
    payments = Payment.objects.filter(paid_at__date__range=(start, end))
    expenses = Expense.objects.filter(expense_date__range=(start, end))
    usage = MaterialUsage.objects.filter(created_at__date__range=(start, end))

    sales = orders.aggregate(v=Sum('total'))['v'] or Decimal('0')
    collected = payments.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    expense_total = expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    material_cost = usage.aggregate(v=Sum('total_cost'))['v'] or Decimal('0')

    product_rows = (OrderItem.objects.filter(order__in=orders)
        .values('product__id', 'product__name')
        .annotate(quantity=Sum('quantity'), revenue=Sum('total_price'))
        .order_by('-revenue')[:10])
    customer_rows = (orders.values('customer__id', 'customer__name', 'customer__phone')
        .annotate(orders=Count('id'), revenue=Sum('total'))
        .order_by('-revenue')[:10])
    expense_rows = (expenses.values('category').annotate(total=Sum('amount')).order_by('-total'))
    monthly = (orders.annotate(month=TruncMonth('created_at')).values('month').annotate(sales=Sum('total'), orders=Count('id')).order_by('month'))

    return JsonResponse({
        'start': str(start), 'end': str(end),
        'sales': str(sales), 'collected': str(collected), 'expenses': str(expense_total),
        'material_cost': str(material_cost),
        'gross_profit': str(sales - material_cost),
        'net_profit': str(sales - material_cost - expense_total),
        'cash_flow_after_expenses': str(collected - expense_total),
        'outstanding': str(orders.aggregate(v=Sum('due_amount'))['v'] or Decimal('0')),
        'order_count': orders.count(),
        'average_order': str((sales / orders.count()).quantize(Decimal('0.01')) if orders.count() else Decimal('0')),
        'products': [{**r, 'quantity': int(r['quantity'] or 0), 'revenue': str(r['revenue'] or 0)} for r in product_rows],
        'customers': [{**r, 'orders': int(r['orders']), 'revenue': str(r['revenue'] or 0)} for r in customer_rows],
        'expense_breakdown': [{**r, 'total': str(r['total'] or 0)} for r in expense_rows],
        'monthly': [{'month': r['month'].strftime('%b %Y'), 'sales': str(r['sales'] or 0), 'orders': int(r['orders'])} for r in monthly],
    })


@staff_member_required
@require_GET
def report_export(request):
    if not _allowed(request.user):
        return HttpResponseForbidden('You do not have report access.')
    start, end = _range(request)
    report = request.GET.get('type', 'orders')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="rnl_{report}_{start}_{end}.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)

    if report == 'orders':
        writer.writerow(['Order', 'Date', 'Customer', 'Phone', 'Status', 'Total', 'Paid', 'Due'])
        qs = Order.objects.exclude(status='cancelled').filter(created_at__date__range=(start, end)).select_related('customer')
        for o in qs.order_by('-created_at'):
            writer.writerow([o.order_number, o.created_at.date(), o.customer.name, o.customer.phone, o.get_status_display(), o.total, o.paid_amount, o.due_amount])
    elif report == 'expenses':
        writer.writerow(['Date', 'Title', 'Category', 'Vendor', 'Amount', 'Note'])
        for e in Expense.objects.filter(expense_date__range=(start, end)).order_by('-expense_date'):
            writer.writerow([e.expense_date, e.title, e.get_category_display(), e.vendor, e.amount, e.note])
    elif report == 'customers':
        writer.writerow(['Customer', 'Phone', 'Company', 'Orders', 'Revenue', 'Due'])
        for c in Customer.objects.annotate(order_count=Count('orders', filter=Q(orders__created_at__date__range=(start, end))), revenue=Coalesce(Sum('orders__total', filter=Q(orders__created_at__date__range=(start, end))), Decimal('0')), due=Coalesce(Sum('orders__due_amount', filter=Q(orders__created_at__date__range=(start, end))), Decimal('0'))).order_by('-revenue'):
            writer.writerow([c.name, c.phone, c.company, c.order_count, c.revenue, c.due])
    elif report == 'materials':
        writer.writerow(['Date', 'Job', 'Order', 'Material', 'Quantity', 'Unit Cost', 'Total Cost'])
        qs = MaterialUsage.objects.filter(created_at__date__range=(start, end)).select_related('job_card__order', 'material')
        for u in qs.order_by('-created_at'):
            writer.writerow([u.created_at.date(), u.job_card_id, u.job_card.order.order_number if u.job_card.order else '', u.material.name, u.quantity, u.unit_cost, u.total_cost])
    else:
        return HttpResponse('Unknown report type.', status=400)
    return response
