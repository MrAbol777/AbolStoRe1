"""
مدل‌های مربوط به محصولات و کمبوها در Abol Store
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

class Product(models.Model):
    """
    مدل محصول (کمبو) برای فروشگاه
    """
    GUARANTEE_CHOICES = (
        ('metaK', 'متیک'),
        ('legend', 'لجند'),
        ('supertash', 'سوپرتاش'),
    )
    
    name = models.CharField(_('نام محصول'), max_length=200)
    description = models.TextField(_('توضیحات'))
    price = models.PositiveIntegerField(_('قیمت (تومان)'))
    guarantee_type = models.CharField(_('نوع تضمین'), max_length=20, choices=GUARANTEE_CHOICES)
    stock = models.PositiveIntegerField(_('تعداد موجودی (پارت)'), default=1)
    image = models.ImageField(_('تصویر محصول'), upload_to='products/', blank=True, null=True)
    webp_image = models.ImageField(_('تصویر WebP محصول'), upload_to='products/webp/', blank=True, null=True)
    is_active = models.BooleanField(_('فعال'), default=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)
    
    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if self.image:
            # Check if the image has changed
            if not self.pk or not Product.objects.get(pk=self.pk).image == self.image:
                # Generate WebP image
                img = Image.open(self.image)
                img_io = BytesIO()
                img.save(img_io, format='WEBP', quality=80)
                
                # Create a new ContentFile from the BytesIO object
                webp_name = os.path.splitext(self.image.name)[0] + '.webp'
                self.webp_image.save(webp_name, ContentFile(img_io.getvalue()), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def is_available(self):
        return self.stock > 0 and self.is_active