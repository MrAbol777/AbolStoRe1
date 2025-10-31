#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.telegram_bot.utils import send_telegram_notification
from django.contrib.auth import get_user_model

User = get_user_model()

def test_telegram():
    print("تست ارسال پیام تلگرام...")
    
    try:
        # پیدا کردن یک کاربر برای تست
        user = User.objects.first()
        if user:
            print(f"ارسال پیام تست برای کاربر: {user.username}")
            result = send_telegram_notification(
                "🔔 این یک پیام تست از فروشگاه ابول استور است!",
                user=user
            )
            print(f"نتیجه ارسال: {'موفق' if result else 'ناموفق'}")
        else:
            print("هیچ کاربری پیدا نشد!")
            
    except Exception as e:
        print(f"خطا در تست: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_telegram()