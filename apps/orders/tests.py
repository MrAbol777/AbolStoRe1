# تست‌های مربوط به سیستم سفارشات و پرداخت
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.store.models import Product
from apps.orders.models import Order, Payment

User = get_user_model()

class OrderTestCase(TestCase):
    def setUp(self):
        # ایجاد کاربر تست
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            phone_number='09123456789',
            telegram_id='@testuser'
        )
        
        # ایجاد محصول تست
        self.product = Product.objects.create(
            name='کمبو تست',
            description='این یک کمبو تست است',
            price=250000,
            guarantee_type='MetaK',
            stock=5,
            is_active=True
        )
        
        # ایجاد کلاینت و لاگین کردن
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
    
    def test_create_order(self):
        """تست ایجاد سفارش جدید"""
        url = reverse('create_order')
        data = {
            'product': self.product.id,
            'quantity': 1,
            'referral_code': ''
        }
        
        response = self.client.post(url, data)
        
        # بررسی ریدایرکت به صفحه پرداخت
        self.assertEqual(response.status_code, 302)
        
        # بررسی ایجاد سفارش در دیتابیس
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 1)
        self.assertEqual(order.status, 'pending')
    
    def test_payment_upload(self):
        """تست آپلود رسید پرداخت"""
        # ایجاد سفارش
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            total_price=self.product.price,
            status='pending'
        )
        
        url = reverse('payment', args=[order.id])
        
        # ایجاد فایل تست
        image = SimpleUploadedFile(
            "receipt.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        data = {
            'receipt': image
        }
        
        response = self.client.post(url, data)
        
        # بررسی ریدایرکت به صفحه جزئیات سفارش
        self.assertEqual(response.status_code, 302)
        
        # بررسی ایجاد پرداخت و تغییر وضعیت سفارش
        self.assertEqual(Payment.objects.count(), 1)
        order.refresh_from_db()
        self.assertEqual(order.status, 'pending_verification')
    
    def test_order_approval(self):
        """تست تأیید سفارش توسط ادمین"""
        # ایجاد کاربر ادمین
        admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword123',
            phone_number='09111111111',
            telegram_id='@admin',
            is_staff=True
        )
        
        # ایجاد سفارش در وضعیت در انتظار تأیید
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            total_price=self.product.price,
            status='pending_verification'
        )
        
        # ایجاد پرداخت
        payment = Payment.objects.create(
            order=order,
            receipt='receipts/test.jpg'
        )
        
        # لاگین با کاربر ادمین
        self.client.login(username='admin', password='adminpassword123')
        
        url = reverse('approve_order', args=[order.id])
        response = self.client.post(url)
        
        # بررسی ریدایرکت
        self.assertEqual(response.status_code, 302)
        
        # بررسی تغییر وضعیت سفارش
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')