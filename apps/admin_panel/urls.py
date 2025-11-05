"""
URLهای پنل ادمین
"""
from django.urls import path, include
from . import views
from . import category_views
from . import category_template_views

app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users_list, name='admin_users_list'),
    path('users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('users/edit/<int:user_id>/', views.admin_user_edit, name='admin_user_edit'),
    path('users/delete/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),
    path('products/', views.admin_products_list, name='admin_products_list'),
    path('products/create/', views.admin_product_create, name='admin_product_create'),
    path('products/edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('products/delete/<int:product_id>/', views.admin_product_delete, name='admin_product_delete'),
    path('orders/', views.admin_orders_list, name='admin_orders_list'),
    path('orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('orders/edit/<int:order_id>/', views.admin_order_edit, name='admin_order_edit'),
    path('orders/delete/<int:order_id>/', views.admin_order_delete, name='admin_order_delete'),
    path('orders/api/<int:order_id>/', views.admin_order_detail_api, name='admin_order_detail_api'),
    path('orders/approve/<int:order_id>/', views.admin_approve_order, name='admin_approve_order'),
    path('orders/reject/<int:order_id>/', views.admin_reject_order, name='admin_reject_order'),
    path('orders/message/<int:order_id>/', views.admin_send_order_message, name='admin_send_order_message'),
    path('settings/', views.admin_settings, name='admin_settings'),
    path('settings/update/', views.admin_update_settings, name='admin_update_settings'),
    path('contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('contact-messages/delete/<int:message_id>/', views.admin_contact_message_delete, name='admin_contact_message_delete'),
    path('categories/', category_template_views.admin_categories_list, name='admin_categories_list'),
    path('categories/create/', category_template_views.admin_category_create, name='admin_category_create'),
    path('categories/edit/<int:category_id>/', category_template_views.admin_category_edit, name='admin_category_edit'),
    path('categories/delete/<int:category_id>/', category_template_views.admin_category_delete, name='admin_category_delete'),
    path('api/categories/', category_views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('api/categories/<slug:slug>/', category_views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]