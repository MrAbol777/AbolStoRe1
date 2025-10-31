"""
مدل‌های مربوط به ربات تلگرام در Abol Store
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.orders.models import Order

class TelegramMessage(models.Model):
    """
    مدل پیام‌های ارسال شده به تلگرام
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='telegram_messages', verbose_name=_('کاربر'), null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='telegram_messages', verbose_name=_('سفارش'), null=True, blank=True)
    message_id = models.CharField(_('شناسه پیام تلگرام'), max_length=100, blank=True, null=True)
    message_text = models.TextField(_('متن پیام'))
    is_sent = models.BooleanField(_('ارسال شده'), default=False)
    sent_at = models.DateTimeField(_('تاریخ ارسال'), null=True, blank=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('پیام تلگرام')
        verbose_name_plural = _('پیام‌های تلگرام')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"پیام تلگرام برای {self.user.username}"