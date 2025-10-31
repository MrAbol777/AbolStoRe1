# مسیرهای مربوط به محصولات و کمبوها
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # مسیرهای مدیریت محصولات (ادمین)
    path('admin/products/', views.product_list_admin, name='product_list_admin'),
    path('admin/products/create/', views.product_create, name='product_create'),
    path('admin/products/<int:pk>/update/', views.product_update, name='product_update'),
    path('admin/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]