# مسیرهای مربوط به محصولات و کمبوها
from django.urls import path, register_converter
from . import views
from . import admin_views

# Converter سفارشی برای Persian slug
class PersianSlugConverter:
    regex = r'[-\w\u0600-\u06FF]+'
    
    def to_python(self, value):
        return value
    
    def to_url(self, value):
        return value

register_converter(PersianSlugConverter, 'persian_slug')

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.HomeView.as_view(), name='product_list'),
    path('products/type/<str:product_type>/', views.ProductListView.as_view(), name='product_list_by_type'),
    path('product/<persian_slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<persian_slug:category_slug>/', views.CategoryDetailView.as_view(), name='product_list_by_category'),

    # مسیرهای مدیریت محصولات (ادمین)
    path('admin/products/', admin_views.product_list_admin, name='product_list_admin'),
    path('admin/products/create/', admin_views.product_create, name='product_create'),
    path('admin/products/<int:pk>/update/', admin_views.product_update, name='product_update'),
    path('admin/products/<int:pk>/delete/', admin_views.product_delete, name='product_delete'),

    # مسیرهای مدیریت دسته بندی ها (ادمین)
    path('admin/categories/', admin_views.admin_category_list, name='admin_category_list'),
    path('admin/categories/create/', admin_views.admin_category_create, name='admin_category_create'),
    path('admin/categories/<int:pk>/edit/', admin_views.admin_category_edit, name='admin_category_edit'),
    path('admin/categories/<int:pk>/delete/', admin_views.admin_category_delete, name='admin_category_delete'),
    path('admin/categories/reorder/', admin_views.admin_category_reorder, name='admin_category_reorder'),
]