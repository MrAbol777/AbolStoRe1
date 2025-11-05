"""
مدل‌های مربوط به محصولات و کمبوها در Abol Store
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(_('نام دسته'), max_length=100, unique=True)
    slug = models.SlugField(_('اسلاگ دسته'), max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(_('توضیحات کوتاه'), blank=True, null=True)
    image = models.ImageField(_('تصویر دسته'), upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_('والد'))
    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.PositiveIntegerField(_('ترتیب نمایش'), default=0, help_text=_('ترتیب نمایش دسته در منوها'))
    meta_title = models.CharField(_('عنوان متا'), max_length=255, blank=True, null=True)
    meta_description = models.TextField(_('توضیحات متا'), blank=True, null=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')
        ordering = ['order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        if self.image:
            # Check if the image has changed
            if not self.pk or not Category.objects.get(pk=self.pk).image == self.image:
                # Generate WebP image
                img = Image.open(self.image)
                img_io = BytesIO()
                img.save(img_io, format='WEBP', quality=80)

                # Create a new ContentFile from the BytesIO object
                webp_name = os.path.splitext(self.image.name)[0] + '.webp'
                self.image.save(webp_name, ContentFile(img_io.getvalue()), save=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('store:category_detail', kwargs={'category_slug': self.slug})


class Product(models.Model):
    """
    مدل محصول (کمبو) برای فروشگاه
    """
    GUARANTEE_CHOICES = (
        ('metaK', 'متیک'),
        ('legend', 'لجند'),
        ('supertash', 'سوپرتاش'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name=_('دسته بندی'))
    name = models.CharField(_('نام محصول'), max_length=200)
    slug = models.SlugField(_('اسلاگ'), max_length=200, unique=True, allow_unicode=True)
    description = models.TextField(_('توضیحات'))
    price = models.PositiveIntegerField(_('قیمت (تومان)'))
    guarantee_type = models.CharField(_('نوع تضمین'), max_length=20, choices=GUARANTEE_CHOICES)
    stock = models.PositiveIntegerField(_('تعداد موجودی (پارت)'), default=1)
    image = models.ImageField(_('تصویر محصول'), upload_to='products/', blank=True, null=True)
    webp_image = models.ImageField(_('تصویر WebP محصول'), upload_to='products/webp/', blank=True, null=True)
    is_active = models.BooleanField(_('فعال'), default=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)
    sales_count = models.PositiveIntegerField(_('تعداد فروش'), default=0)
    
    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if self.image:
            # Check if the image has changed
            if not self.pk or not Product.objects.get(pk=self.pk).image == self.image:
                # Generate WebP image
                img = Image.open(self.image)
                img_io = BytesIO()
                img.save(img_io, format='WEBP', quality=80)

                # Create a new ContentFile from the BytesIO object
                webp_name = os.path.splitext(self.image.name)[0] + '.webp'
                # Assign the ContentFile to the webp_image field
                self.webp_image = ContentFile(img_io.getvalue(), name=webp_name)

        super().save(*args, **kwargs)
        print(f"super().save() executed for product: {self.name}")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('store:product_detail', kwargs={'slug': self.slug})
    
    @property
    def is_available(self):
        """بررسی موجودی محصول"""
        return self.is_active and self.stock > 0