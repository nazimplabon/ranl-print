from django.contrib import admin

from .models import FinishingOption, PaperOption, PrintOption, Product, QuantityPrice, SizeOption


class SizeInline(admin.TabularInline):
    model = SizeOption
    fields = ('name', 'active', 'sort_order')
    extra = 0


class PaperInline(admin.TabularInline):
    model = PaperOption
    fields = ('name', 'gsm', 'active', 'sort_order')
    extra = 0


class PrintInline(admin.TabularInline):
    model = PrintOption
    fields = ('name', 'active', 'sort_order')
    extra = 0


class FinishInline(admin.TabularInline):
    model = FinishingOption
    fields = ('name', 'active', 'sort_order')
    extra = 0


class QtyInline(admin.TabularInline):
    model = QuantityPrice
    fields = ('min_quantity', 'max_quantity', 'active')
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active', 'sort_order', 'updated_at')
    list_filter = ('category', 'active')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('active', 'sort_order')
    ordering = ('sort_order', 'name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product', {'fields': ('name', 'slug', 'category', 'description')}),
        ('Settings', {'fields': ('active', 'sort_order')}),
        ('System', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    inlines = [QtyInline, SizeInline, PaperInline, PrintInline, FinishInline]


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'active', 'sort_order')
    list_filter = ('active', 'product')
    search_fields = ('name', 'product__name')
    ordering = ('product', 'sort_order', 'name')


@admin.register(PaperOption)
class PaperOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'gsm', 'active', 'sort_order')
    list_filter = ('active', 'product')
    search_fields = ('name', 'product__name')
    ordering = ('product', 'sort_order', 'name')


@admin.register(PrintOption)
class PrintOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'active', 'sort_order')
    list_filter = ('active', 'product')
    search_fields = ('name', 'product__name')
    ordering = ('product', 'sort_order', 'name')


@admin.register(FinishingOption)
class FinishingOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'active', 'sort_order')
    list_filter = ('active', 'product')
    search_fields = ('name', 'product__name')
    ordering = ('product', 'sort_order', 'name')


@admin.register(QuantityPrice)
class QuantityPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'min_quantity', 'max_quantity', 'active')
    list_filter = ('active', 'product')
    search_fields = ('product__name',)
    ordering = ('product', 'min_quantity')
