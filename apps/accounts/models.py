"""
مدل‌های مربوط به کاربران در Abol Store
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    مدل کاربر سفارشی با فیلدهای اضافی برای شماره موبایل و آیدی تلگرام
    """
    full_name = models.CharField(_('نام کامل'), max_length=150, blank=True)
    phone_number = models.CharField(_('شماره موبایل'), max_length=15, blank=True, null=True, unique=True)
    telegram_id = models.CharField(_('آیدی تلگرام'), max_length=100, blank=True, null=True, unique=True)
    accepted_terms = models.BooleanField(_('پذیرش قوانین'), default=False)
    
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
    
    def __str__(self):
        return self.username

class ContactMessage(models.Model):
    """
    پیام‌های تماس کاربران
    """
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=150)
    telegram_id = models.CharField(_('آیدی تلگرام'), max_length=100, blank=True)
    phone_number = models.CharField(_('شماره موبایل'), max_length=15, blank=True)
    message = models.TextField(_('پیام کاربر'))
    created_at = models.DateTimeField(_('تاریخ ارسال'), auto_now_add=True)
    is_viewed = models.BooleanField(_('مشاهده شده توسط ادمین'), default=False)
    
    class Meta:
        verbose_name = _('پیام تماس')
        verbose_name_plural = _('پیام‌های تماس')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"پیام از {self.full_name} ({self.phone_number})"