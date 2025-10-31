# توابع کمکی برای ارسال پیام به تلگرام
import logging
import requests
from django.conf import settings
from django.utils import timezone

from .models import TelegramMessage

logger = logging.getLogger(__name__)

def _send_message(chat_id, text):
    """ارسال پیام به تلگرام با استفاده از requests"""
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                return result['result']['message_id']
            else:
                logger.error(f"خطا در ارسال پیام: {result.get('description')}")
                return None
        else:
            logger.error(f"خطای HTTP: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"خطا در ارسال پیام به تلگرام: {e}")
        return None

def send_telegram_notification(text, chat_id=None, user=None, order=None):
    """ارسال اعلان به تلگرام"""
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    admin_chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
    
    # بررسی اینکه آیا توکن معتبر هست یا نه
    if not token or token == 'your_telegram_bot_token':
        logger.warning("توکن بات تلگرام تنظیم نشده یا نامعتبر است، ارسال پیام نادیده گرفته شد")
        return True  # بازگشت True برای ادامه فرآیند بدون خطا
    
    # اگر chat_id مشخص نشده باشد، از chat_id ادمین استفاده می‌کنیم
    if not chat_id:
        chat_id = admin_chat_id
    
    if not chat_id or chat_id == 'your_admin_chat_id':
        logger.warning("شناسه چت تلگرام تنظیم نشده یا نامعتبر است، ارسال پیام نادیده گرفته شد")
        return True  # بازگشت True برای ادامه فرآیند بدون خطا
    
    try:
        # ارسال پیام
        message_id = _send_message(chat_id, text)
        
        # ذخیره پیام در دیتابیس
        if message_id:
            TelegramMessage.objects.create(
                user=user,
                order=order,
                message_id=message_id,
                message_text=text,
                is_sent=True,
                sent_at=timezone.now()
            )
            return True
        else:
            TelegramMessage.objects.create(
                user=user,
                order=order,
                message_text=text,
                is_sent=False
            )
            return False
            
    except Exception as e:
        logger.error(f"خطا در ارسال پیام به تلگرام: {e}")
        
        # ذخیره پیام با وضعیت خطا
        TelegramMessage.objects.create(
            user=user,
            order=order,
            message_text=text,
            is_sent=False
        )
        return False