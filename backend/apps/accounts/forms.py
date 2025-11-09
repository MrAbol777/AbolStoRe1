"""
فرم‌های مربوط به کاربران در Abol Store
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from .models import User, ContactMessage

PHONE_REGEX = re.compile(r"^(\+?98|0)?9\d{9}$")
TELEGRAM_REGEX = re.compile(r"^@?[A-Za-z0-9_]{5,32}$")

class CustomUserCreationForm(UserCreationForm):
    """
    فرم ثبت‌نام کاربر با فیلدهای اضافی
    """
    phone_number = forms.CharField(label=_('شماره موبایل'), max_length=15, required=True,
                                   widget=forms.TextInput(attrs={'dir': 'rtl', 'placeholder': 'مثلاً 0912xxxxxxx', 'pattern': PHONE_REGEX.pattern}))
    telegram_id = forms.CharField(label=_('آیدی تلگرام'), max_length=100, required=True,
                                  widget=forms.TextInput(attrs={'dir': 'rtl', 'placeholder': '@testuser', 'pattern': TELEGRAM_REGEX.pattern}))
    accepted_terms = forms.BooleanField(label=_('قوانین و مقررات را می‌پذیرم'), required=True)
    
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'telegram_id', 'password1', 'password2', 'accepted_terms')
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if not PHONE_REGEX.match(phone):
            raise ValidationError(_('شماره موبایل معتبر وارد کنید.'))
        # نرمال‌سازی به فرمت 09xxxxxxxxx
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        elif phone.startswith('98'):
            phone = '0' + phone[2:]
        # بررسی عدم تکراری بودن
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError(_('این شماره موبایل قبلاً ثبت شده است.'))
        return phone
    
    def clean_telegram_id(self):
        tg = self.cleaned_data.get('telegram_id', '').strip()
        if not TELEGRAM_REGEX.match(tg):
            raise ValidationError(_('آیدی تلگرام معتبر وارد کنید.'))
        # حذف @ ابتدای آیدی
        if tg.startswith('@'):
            tg = tg[1:]
        if User.objects.filter(telegram_id=tg).exists():
            raise ValidationError(_('این آیدی تلگرام قبلاً ثبت شده است.'))
        return tg

class CustomAuthenticationForm(AuthenticationForm):
    """
    فرم ورود کاربر با استایل سفارشی
    """
    username = forms.CharField(label=_('نام کاربری'), widget=forms.TextInput(attrs={'class': 'form-input', 'dir': 'rtl'}))
    password = forms.CharField(label=_('رمز عبور'), widget=forms.PasswordInput(attrs={'class': 'form-input', 'dir': 'rtl'}))

class ContactForm(forms.ModelForm):
    """
    فرم تماس با ما
    """
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'telegram_id', 'phone_number', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'dir': 'rtl'}),
            'telegram_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'dir': 'rtl', 'placeholder': '@username'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'dir': 'rtl', 'placeholder': '0912xxxxxxx'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'rows': 4, 'dir': 'rtl'})
        }
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if phone and not PHONE_REGEX.match(phone):
            raise ValidationError(_('شماره موبایل معتبر وارد کنید.'))
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        elif phone.startswith('98'):
            phone = '0' + phone[2:]
        return phone
    
    def clean_telegram_id(self):
        tg = self.cleaned_data.get('telegram_id', '').strip()
        if tg and not TELEGRAM_REGEX.match(tg):
            raise ValidationError(_('آیدی تلگرام معتبر وارد کنید.'))
        if tg.startswith('@'):
            tg = tg[1:]
        return tg


class UserEditForm(forms.ModelForm):
    """فرم ویرایش کاربر برای پنل ادمین"""
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'telegram_id', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'phone_number': forms.TextInput(attrs={'dir': 'rtl', 'placeholder': 'مثلاً 0912xxxxxxx'}),
            'telegram_id': forms.TextInput(attrs={'dir': 'rtl', 'placeholder': '@testuser'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500'
            })

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if not PHONE_REGEX.match(phone):
            raise ValidationError(_('شماره موبایل معتبر وارد کنید.'))
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        elif phone.startswith('98'):
            phone = '0' + phone[2:]
        # بررسی عدم تکراری بودن برای کاربران دیگر
        if User.objects.filter(phone_number=phone).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_('این شماره موبایل قبلاً توسط کاربر دیگری ثبت شده است.'))
        return phone

    def clean_telegram_id(self):
        tg = self.cleaned_data.get('telegram_id', '').strip()
        if not TELEGRAM_REGEX.match(tg):
            raise ValidationError(_('آیدی تلگرام معتبر وارد کنید.'))
        if tg.startswith('@'):
            tg = tg[1:]
        # بررسی عدم تکراری بودن برای کاربران دیگر
        if User.objects.filter(telegram_id=tg).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_('این آیدی تلگرام قبلاً توسط کاربر دیگری ثبت شده است.'))
        return tg