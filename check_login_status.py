"""
بررسی وضعیت لاگین کاربر
"""
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from apps.accounts.models import User

# بررسی یوزرهایی که لاگین کردن
print("📋 بررسی یوزرهای فعال:")
for user in User.objects.filter(is_active=True):
    print(f"👤 {user.username} - Staff: {user.is_staff} - Superuser: {user.is_superuser}")

# تست لاگین با اطلاعات جدید
user = authenticate(username='aboladmin', password='1234')
if user:
    print(f"\n✅ لاگین موفق برای: {user.username}")
    print(f"🔑 ادمین: {user.is_staff}")
else:
    print("\n❌ لاگین ناموفق")