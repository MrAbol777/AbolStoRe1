"""
بررسی وضعیت لاگین یوزر
"""
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from apps.accounts.models import User

# تست لاگین
user = authenticate(username='MrAbol777', password='1234')
if user:
    print(f"✅ لاگین موفق: {user.username}")
    print(f"👤 نام: {user.full_name}")
    print(f"📱 شماره: {user.phone_number}")
    print(f"🔑 ادمین: {user.is_staff}")
else:
    print("❌ لاگین ناموفق")

# بررسی یوزرهای ادمین
print("\n👥 یوزرهای ادمین:")
for user in User.objects.filter(is_staff=True):
    print(f"👤 {user.username} - {user.full_name} - {user.phone_number}")