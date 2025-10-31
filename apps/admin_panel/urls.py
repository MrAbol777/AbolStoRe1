"""
URLهای پنل ادمین
"""
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.admin_users_list, name='users_list'),
    path('users/<int:user_id>/', views.admin_user_detail, name='user_detail'),
    path('users/edit/<int:user_id>/', views.admin_user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.admin_user_delete, name='user_delete'),
    path('products/', views.admin_products_list, name='products_list'),
    path('products/create/', views.admin_product_create, name='admin_product_create'),
    path('products/edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('products/delete/<int:product_id>/', views.admin_product_delete, name='admin_product_delete'),
    path('orders/', views.admin_orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.admin_order_detail, name='order_detail'),
    path('orders/edit/<int:order_id>/', views.admin_order_edit, name='order_edit'),
    path('orders/delete/<int:order_id>/', views.admin_order_delete, name='order_delete'),
    path('settings/', views.admin_settings, name='settings'),
    path('settings/update/', views.admin_update_settings, name='update_settings'),
    path('products/', views.admin_products_list, name='admin_products_list'),
    path('contact-messages/', views.admin_contact_messages, name='contact_messages'),
    path('contact-messages/delete/<int:message_id>/', views.admin_contact_message_delete, name='contact_message_delete'),
]