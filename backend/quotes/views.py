from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Quote


@require_POST
def create_quote(request):
    try:
        product = Product.objects.get(slug=request.POST.get('product'), active=True)
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        quantity = int(request.POST.get('quantity', '0'))

        if len(name) < 2:
            raise ValueError('Please enter your name.')
        if len(phone) < 6:
            raise ValueError('Please enter a valid phone number.')
        if quantity < 1:
            raise ValueError('Quantity must be at least 1.')

        artwork = request.FILES.get('artwork')
        max_bytes = int(getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 20 * 1024 * 1024))
        if artwork and artwork.size > max_bytes:
            raise ValueError('Artwork is too large.')

        finishing_ids = request.POST.getlist('finishing')
        finish_names = list(
            product.finishing_options.filter(id__in=finishing_ids, active=True)
            .values_list('name', flat=True)
        )
        quote = Quote.objects.create(
            name=name,
            phone=phone,
            email=email,
            product=product,
            quantity=quantity,
            size=request.POST.get('size', ''),
            paper=request.POST.get('paper', ''),
            printing=request.POST.get('printing', ''),
            finishing=finish_names,
            artwork=artwork,
            notes=request.POST.get('notes', '').strip(),
        )
        return JsonResponse({
            'ok': True,
            'quote_number': quote.quote_number,
        })
    except (Product.DoesNotExist, ValueError, ValidationError, ObjectDoesNotExist) as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=400)
