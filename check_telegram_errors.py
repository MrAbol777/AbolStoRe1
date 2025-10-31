#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.telegram_bot.models import TelegramMessage

def check_telegram_errors():
    print("بررسی پیام‌های تلگرام ارسال نشده:")
    print("=" * 60)
    
    messages = TelegramMessage.objects.filter(is_sent=False)
    
    if not messages:
        print("هیچ پیام ارسال نشده‌ای پیدا نشد.")
        return
    
    for m in messages:
        print(f"ID: {m.id}")
        print(f"متن پیام: {m.message_text[:100]}...")
        print(f"وضعیت ارسال: {m.is_sent}")
        print(f"زمان ایجاد: {m.created_at}")
        print(f"وضعیت: {'ارسال نشده' if not m.is_sent else 'ارسال شده'}")
        if m.message_id:
            print(f"شناسه تلگرام: {m.message_id}")
        else:
            print("شناسه تلگرام: ندارد")
        print("-" * 60)

if __name__ == "__main__":
    check_telegram_errors()