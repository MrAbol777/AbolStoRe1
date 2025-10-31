#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import User

def create_test_user():
    print("ساخت کاربر تست با پسورد ساده...")
    
    try:
        # حذف کاربر قبلی اگر وجود داشت
        if User.objects.filter(username='testuser').exists():
            User.objects.filter(username='testuser').delete()
            print("کاربر قبلی حذف شد")
        
        # ساخت کاربر جدید با پسورد ساده
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='1234',  # پسورد خیلی ساده
            phone_number='09123456789',
            telegram_id='@testuser'
        )
        
        print(f"✅ کاربر ساخته شد!")
        print(f"نام کاربری: {user.username}")
        print(f"ایمیل: {user.email}")
        print(f"پسورد: 1234")
        print("\nحالا می‌تونید با این اطلاعات وارد شید:")
        print("نام کاربری: testuser")
        print("پسورد: 1234")
        
    except Exception as e:
        print(f"❌ خطا در ساخت کاربر: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_user()