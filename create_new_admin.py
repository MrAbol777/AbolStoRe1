"""
ساخت یوزر ادمین جدید با رمز مشخص
"""
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User

# ساخت یوزر ادمین جدید
admin_user = User.objects.create(
    username='aboladmin',
    full_name='مدیر فروشگاه ابوالفضل',
    phone_number='09120000000',
    email='abol@example.com',
    is_staff=True,
    is_superuser=True,
)
admin_user.set_password('1234')
admin_user.save()

print(f"✅ ادمین جدید ساخته شد:")
print(f"📱 نام کاربری: {admin_user.username}")
print(f"🔑 رمز عبور: 1234")
print(f"👤 نام: {admin_user.full_name}")
print(f"📞 شماره: {admin_user.phone_number}")
print(f"🔑 ادمین: {admin_user.is_staff}")