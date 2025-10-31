# فرم‌های مربوط به سفارش و پرداخت
from django import forms
from .models import Order, Payment

class OrderForm(forms.ModelForm):
    """فرم ایجاد سفارش جدید"""
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'referral_code']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500'}),
            'referral_code': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500'})
        }

class PaymentForm(forms.ModelForm):
    """فرم ثبت اطلاعات پرداخت"""
    class Meta:
        model = Payment
        fields = ['receipt']
        widgets = {
            'receipt': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500'})
        }
        
    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            # بررسی نوع فایل
            allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
            if receipt.content_type not in allowed_types:
                raise forms.ValidationError('فقط فایل‌های JPG، PNG و PDF مجاز هستند.')
            
            # بررسی حجم فایل (حداکثر 5MB)
            if receipt.size > 5 * 1024 * 1024:
                raise forms.ValidationError('حجم فایل نباید بیشتر از 5 مگابایت باشد.')
                
        return receipt