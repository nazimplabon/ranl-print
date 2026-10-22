from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET, require_POST

from .models import ContactMessage


@require_GET
def csrf(request):
    return JsonResponse({'ok': True, 'csrfToken': get_token(request)})


@require_POST
def create_contact(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()

    if len(name) < 2:
        return JsonResponse({'ok': False, 'error': 'Please enter your name.'}, status=400)
    if len(phone) < 6:
        return JsonResponse({'ok': False, 'error': 'Please enter a valid phone number.'}, status=400)
    if len(message) < 5:
        return JsonResponse({'ok': False, 'error': 'Please enter a message.'}, status=400)

    item = ContactMessage.objects.create(
        name=name, phone=phone, email=email, message=message,
    )
    return JsonResponse({'ok': True, 'message_id': item.id})
