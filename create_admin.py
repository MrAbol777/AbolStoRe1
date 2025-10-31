"""
اسکریپت ساخت ادمین برای تست داشبورد
"""
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User

# ساخت یوزر ادمین - ابتدا بررسی کنیم که وجود نداره
admin_exists = User.objects.filter(username='admin').exists()
if not admin_exists:
    admin_user = User.objects.create(
        username='admin',
        full_name='مدیر فروشگاه',
        phone_number='09123456789',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True,
    )
    admin_user.set_password('admin1234')
    admin_user.save()
    print(f"✅ ادمین با موفقیت ساخته شد: {admin_user.username}")
    print(f"📱 نام کاربری: admin")
    print(f"🔑 رمز عبور: admin1234")
else:
    print(f"ℹ️ ادمین قبلاً وجود دارد: admin")

# ساخت یوزر معمولی برای تست - ابتدا بررسی کنیم که وجود نداره
user_exists = User.objects.filter(username='user1').exists()
if not user_exists:
    test_user = User.objects.create(
        username='user1',
        full_name='کاربر تست',
        phone_number='09123456780',
        email='user1@example.com',
    )
    test_user.set_password('1234')
    test_user.save()
    print(f"✅ کاربر تست ساخته شد: {test_user.username}")
    print(f"📱 نام کاربری: user1")
    print(f"🔑 رمز عبور: 1234")
else:
    print(f"ℹ️ کاربر تست قبلاً وجود دارد: user1")