from django.contrib import admin, messages
from django.db import transaction
from decimal import Decimal

from .models import Quote
from orders.models import Customer, Order, OrderItem


def create_order_from_quote(quote):
    """Create one draft order for an approved quote, without inventing a price."""
    existing = Order.objects.filter(quote=quote).first()
    if existing:
        return existing, False

    customer, _ = Customer.objects.get_or_create(
        phone=quote.phone,
        defaults={
            "name": quote.name,
            "email": quote.email or "",
        },
    )
    # Keep existing customer contact details current when a quote is approved.
    changed = []
    if quote.name and customer.name != quote.name:
        customer.name = quote.name
        changed.append("name")
    if quote.email and customer.email != quote.email:
        customer.email = quote.email
        changed.append("email")
    if changed:
        customer.save(update_fields=changed + ["updated_at"])

    with transaction.atomic():
        order = Order.objects.create(
            customer=customer,
            quote=quote,
            status="pending",
            subtotal=Decimal("0.00"),
            discount=Decimal("0.00"),
            delivery_fee=Decimal("0.00"),
            paid_amount=Decimal("0.00"),
            notes=(
                f"Created from approved quote {quote.quote_number}. "
                "Price not entered yet; confirm price with customer."
            ),
        )
        OrderItem.objects.create(
            order=order,
            product=quote.product,
            description=(
                f"Quote {quote.quote_number} | Size: {quote.size or '-'} | "
                f"Paper/GSM: {quote.paper or '-'} | Printing: {quote.printing or '-'} | "
                f"Finishing: {', '.join(quote.finishing or []) or '-'}"
            ),
            quantity=quote.quantity,
            unit_price=Decimal("0.0000"),
            selected_options={
                "size": quote.size,
                "paper": quote.paper,
                "printing": quote.printing,
                "finishing": quote.finishing or [],
                "quote_number": quote.quote_number,
            },
        )
    return order, True


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Simple quote workflow. Approving a quote creates a draft order."""
    list_display = (
        "quote_number", "name", "phone", "product", "quantity",
        "status", "linked_order", "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("quote_number", "name", "phone", "email", "product__name")
    readonly_fields = ("quote_number", "created_at", "updated_at", "linked_order")
    list_editable = ("status",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25
    actions = ("create_orders_for_approved_quotes",)

    fieldsets = (
        ("Request Status", {"fields": ("quote_number", "status", "linked_order")}),
        ("Customer Contact", {"fields": ("name", "phone", "email")}),
        ("Print Requirements", {"fields": (
            "product", "quantity", "size", "paper", "printing",
            "finishing", "artwork", "notes",
        )}),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Order")
    def linked_order(self, obj):
        if not obj or not obj.pk:
            return "-"
        order = getattr(obj, "order", None)
        if not order:
            return "Not created"
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse("admin:orders_order_change", args=[order.pk])
        return format_html('<a href="{}">{}</a>', url, order.order_number)

    def save_model(self, request, obj, form, change):
        was_approved = False
        if change and obj.pk:
            old_status = Quote.objects.filter(pk=obj.pk).values_list("status", flat=True).first()
            was_approved = old_status == "approved"
        super().save_model(request, obj, form, change)
        if obj.status == "approved":
            try:
                order, created = create_order_from_quote(obj)
                if created:
                    messages.success(
                        request,
                        f"Order {order.order_number} created from quote {obj.quote_number}. "
                        "Add the agreed price in the order before invoicing.",
                    )
            except Exception as exc:
                messages.error(request, f"Quote was saved, but order creation failed: {exc}")

    @admin.action(description="Create orders for selected approved quotes")
    def create_orders_for_approved_quotes(self, request, queryset):
        created_count = 0
        existing_count = 0
        for quote in queryset.filter(status="approved"):
            try:
                _, created = create_order_from_quote(quote)
                if created:
                    created_count += 1
                else:
                    existing_count += 1
            except Exception as exc:
                self.message_user(
                    request,
                    f"Could not create order for {quote.quote_number}: {exc}",
                    level=messages.ERROR,
                )
        self.message_user(
            request,
            f"Created {created_count} order(s); {existing_count} already had an order.",
            level=messages.SUCCESS,
        )
