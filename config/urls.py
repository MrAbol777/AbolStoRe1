"""
تنظیمات URL های اصلی پروژه Abol Store
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.store.sitemaps import StaticSitemap, ProductSitemap

sitemaps = {
    'static': StaticSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    # ابتدا مسیرهای سفارشی فروشگاه تا مسیرهای خاص admin/products قبل از جنگو ادمین مچ شوند
    path('', include(('apps.store.urls', 'store'), namespace='store')),
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('orders/', include(('apps.orders.urls', 'orders'), namespace='orders')),
    path('admin-panel/', include('apps.admin_panel.urls', namespace='admin_panel')),
    path('contact-us/', include(('apps.contact.urls', 'contact'), namespace='contact')),
    # سپس پنل کلاسیک جنگو
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)