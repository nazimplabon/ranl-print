from django.contrib import admin
from .models import ContactMessage

admin.site.site_header = 'RANL PRINT — Business Management'
admin.site.site_title = 'RANL PRINT Admin'
admin.site.index_title = 'Operations & Business Management'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
