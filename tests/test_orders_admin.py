"""
تست دسترسی به مدیریت سفارش‌ها
"""
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import Order
from apps.accounts.models import User

print("📋 بررسی سفارش‌ها:")
print(f"تعداد کل سفارش‌ها: {Order.objects.count()}")

# نمایش چند سفارش اول
orders = Order.objects.all()[:5]
for order in orders:
    print(f"📝 سفارش #{order.id}: {order.product.name} - کاربر: {order.user.phone_number} - وضعیت: {order.get_status_display()}")

# بررسی سفارشات در انتظار تأیید
waiting_orders = Order.objects.filter(status='waiting')
print(f"\n📋 سفارشات در انتظار تأیید: {waiting_orders.count()}")

for order in waiting_orders[:3]:
    print(f"⏳ سفارش #{order.id}: {order.product.name} - {order.user.phone_number}")
    
# بررسی ادمین‌ها
admin_users = User.objects.filter(is_staff=True)
print(f"\n👥 تعداد ادمین‌ها: {admin_users.count()}")
for admin in admin_users:
    print(f"🔑 {admin.username} - {admin.phone_number}")