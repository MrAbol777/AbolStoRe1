# مسیرهای مربوط به سفارش و پرداخت
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # مسیرهای کاربر
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/payment/', views.order_payment, name='order_payment'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('', views.order_list, name='order_list'),
    
    # مسیرهای ادمین
    path('admin/', views.admin_order_list, name='admin_order_list'),
    path('admin/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/export/csv/', views.export_orders_csv, name='export_orders_csv'),
]