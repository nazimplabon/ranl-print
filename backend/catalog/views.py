from decimal import Decimal, InvalidOperation

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import Product


def money(value):
    return f'{Decimal(value):.2f}'


def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'category': product.category,
        'description': product.description,
        'sizes': [
            {'id': x.id, 'name': x.name}
            for x in product.sizes.filter(active=True)
        ],
        'papers': [
            {'id': x.id, 'name': x.name, 'gsm': x.gsm}
            for x in product.papers.filter(active=True)
        ],
        'printing': [
            {'id': x.id, 'name': x.name}
            for x in product.printing_options.filter(active=True)
        ],
        'finishing': [
            {'id': x.id, 'name': x.name}
            for x in product.finishing_options.filter(active=True)
        ],
    }


@require_GET
def products(request):
    items = Product.objects.filter(active=True).prefetch_related(
        'sizes', 'papers', 'printing_options', 'finishing_options', 'quantity_prices'
    )
    return JsonResponse({'products': [serialize_product(p) for p in items]})


def calculate_price(product, quantity, size_id=None, paper_id=None, printing_id=None, finishing_ids=None):
    if quantity < 1:
        raise ValueError('Quantity must be at least 1.')

    bracket = (
        product.quantity_prices.filter(active=True, min_quantity__lte=quantity)
        .filter(models.Q(max_quantity__isnull=True) | models.Q(max_quantity__gte=quantity))
        .order_by('min_quantity')
        .last()
    )
    if not bracket:
        raise ValueError('No pricing rule exists for this quantity.')

    total = product.setup_fee + bracket.fixed_fee + bracket.unit_price * quantity

    if size_id:
        total += product.sizes.get(pk=size_id, active=True).price_delta
    if paper_id:
        total *= product.papers.get(pk=paper_id, active=True).multiplier
    if printing_id:
        total += product.printing_options.get(pk=printing_id, active=True).price_delta

    for finishing_id in finishing_ids or []:
        finish = product.finishing_options.get(pk=finishing_id, active=True)
        total += finish.fixed_fee + (finish.per_unit_fee * quantity)

    return total.quantize(Decimal('0.01'))


@require_POST
def calculate(request):
    # Compatibility response for older cached frontend bundles. Never calculate or return a price.
    return JsonResponse({
        'ok': True,
        'message': 'Our team will contact you with a price.',
        'price': None,
    }, status=200)
