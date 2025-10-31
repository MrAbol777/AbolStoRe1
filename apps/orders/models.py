"""
مدل‌های مربوط به سفارشات در Abol Store
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.store.models import Product
import os
import uuid


def get_receipt_upload_path(instance, filename):
    """مسیر امن برای ذخیره رسید با نام‌گذاری تصادفی"""
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    # محدود کردن پسوند به انواع مجاز
    allowed_exts = {'.jpg', '.jpeg', '.png', '.pdf'}
    if ext not in allowed_exts:
        # اگر پسوند نامعتبر بود، به pdf تغییر کند تا ذخیره‌سازی امن باقی بماند
        ext = '.pdf'
    random_name = uuid.uuid4().hex
    return os.path.join('receipts', f"{random_name}{ext}")

class Order(models.Model):
    """
    مدل سفارش برای خرید محصولات
    """
    STATUS_CHOICES = (
        ('pending', 'ثبت شده'),
        ('waiting', 'در انتظار تأیید'),
        ('confirmed', 'تأیید شده'),
        ('rejected', 'رد شده'),
        ('delivered', 'تحویل شده'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name=_('کاربر'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name=_('محصول'))
    quantity = models.PositiveIntegerField(_('تعداد'), default=1)
    total_price = models.PositiveIntegerField(_('قیمت کل (تومان)'))
    status = models.CharField(_('وضعیت'), max_length=20, choices=STATUS_CHOICES, default='pending')
    referral_code = models.CharField(_('کد معرف'), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)
    
    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارشات')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"سفارش {self.id} - {self.user.username}"

class Payment(models.Model):
    """
    مدل پرداخت برای سفارشات
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name=_('سفارش'))
    receipt = models.FileField(_('رسید پرداخت'), upload_to=get_receipt_upload_path)
    card_number = models.CharField(_('شماره کارت مقصد'), max_length=20)
    is_verified = models.BooleanField(_('تأیید شده'), default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments', verbose_name=_('تأیید کننده'))
    verified_at = models.DateTimeField(_('تاریخ تأیید'), null=True, blank=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('پرداخت')
        verbose_name_plural = _('پرداخت‌ها')
    
    def __str__(self):
        return f"پرداخت برای سفارش {self.order.id}"