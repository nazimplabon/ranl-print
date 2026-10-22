from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

def site_home(request):
    return render(request, 'site/index.html')


urlpatterns = [
    path('', site_home, name='site-home'),
    path('admin/', admin.site.urls),
    path('track/', lambda request: render(request, 'track_order.html'), name='track-order'),
    path('api/', include('core.urls')),
    path('api/', include('catalog.urls')),
    path('api/', include('quotes.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/production/', include('production.urls')),
    path('api/inventory/', include('inventory.urls')),

]

if settings.DEBUG:
    # Explicitly serve both media and project static files during local development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
