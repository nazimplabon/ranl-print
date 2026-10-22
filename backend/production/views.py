from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from .models import JobCard

@staff_member_required
@require_GET
def job_list(request):
    if not request.user.has_perm('production.view_jobcard'):
        return HttpResponseForbidden('You do not have production access.')
    qs=JobCard.objects.select_related('order__customer').order_by('due_date','-created_at')[:100]
    return JsonResponse({'results':[{'id':j.id,'order':j.order.order_number,'customer':j.order.customer.name,'status':j.status,'machine':j.machine,'assigned_to':j.assigned_to,'quantity':j.quantity,'due_date':j.due_date.isoformat() if j.due_date else None} for j in qs]})
