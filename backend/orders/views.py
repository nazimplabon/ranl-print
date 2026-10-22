from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET
from .models import Order

def _can(request):
    return request.user.has_perm("orders.view_order")

def _order_payload(order):
    return {
        'id': order.id, 'order_number': order.order_number, 'customer': order.customer.name,
        'phone': order.customer.phone, 'status': order.status, 'payment_status': order.payment_status,
        'delivery_status': order.delivery_status, 'total': str(order.total), 'paid': str(order.paid_amount),
        'due': str(order.due_amount), 'due_date': order.due_date.isoformat() if order.due_date else None,
        'created_at': order.created_at.isoformat(),
    }

@staff_member_required
@require_GET
def order_list(request):
    if not _can(request): return HttpResponseForbidden('You do not have permission to view orders.')
    qs = Order.objects.select_related('customer').order_by('-created_at')
    status = request.GET.get('status')
    if status: qs = qs.filter(status=status)
    return JsonResponse({'results': [_order_payload(o) for o in qs[:100]]})


from django.views.decorators.http import require_POST

@require_POST
def track_order(request):
    order_number = request.POST.get('order_number', '').strip().upper()
    phone = request.POST.get('phone', '').strip()
    if not order_number or len(phone) < 6:
        return JsonResponse({'ok': False, 'error': 'Enter your order number and phone number.'}, status=400)
    try:
        order = Order.objects.select_related('customer').get(order_number=order_number, customer__phone=phone)
    except Order.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'No matching order was found.'}, status=404)
    return JsonResponse({'ok': True, 'order': {
        'order_number': order.order_number,
        'customer': order.customer.name,
        'status': order.get_status_display(),
        'payment_status': order.get_payment_status_display(),
        'delivery_status': order.get_delivery_status_display(),
        'total': str(order.total),
        'paid': str(order.paid_amount),
        'due': str(order.due_amount),
        'due_date': order.due_date.isoformat() if order.due_date else None,
        'tracking_number': order.tracking_number or '',
        'created_at': order.created_at.date().isoformat(),
    }})
