from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.store.models import Product

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['home', 'accounts:register', 'accounts:login', 'accounts:contact']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at