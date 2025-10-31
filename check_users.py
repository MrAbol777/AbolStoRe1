"""
بررسی یوزرهای موجود
"""
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User

print("📋 لیست کاربران موجود:")
for user in User.objects.all():
    print(f"👤 {user.username} - {user.full_name} - {user.phone_number} - Staff: {user.is_staff}")

print(f"\n📊 تعداد کل کاربران: {User.objects.count()}")