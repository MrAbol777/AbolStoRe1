"""
تنظیمات URL های اصلی پروژه Abol Store
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ابتدا مسیرهای سفارشی فروشگاه تا مسیرهای خاص admin/products قبل از جنگو ادمین مچ شوند
    path('', include('apps.store.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('orders/', include(('apps.orders.urls', 'orders'), namespace='orders')),
    path('admin-panel/', include('apps.admin_panel.urls', namespace='admin_panel')),
    # سپس پنل کلاسیک جنگو
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)