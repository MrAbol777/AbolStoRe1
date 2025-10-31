"""
ویوهای مربوط به کاربران در Abol Store
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import ContactForm

def register(request):
    """
    ثبت‌نام کاربر جدید
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد.')
                return redirect('home')
        except Exception as e:
            messages.error(request, 'خطایی رخ داد. لطفاً دوباره تلاش کنید.')
        
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def _throttle_key(request):
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    return f"login_attempts:{ip}"

def login_view(request):
    """
    ورود کاربر
    """
    if request.method == 'POST':
        # محدودسازی تلاش‌های ورود: حداکثر 5 تلاش در 10 دقیقه
        key = _throttle_key(request)
        attempts, expires = cache.get(key, (0, None)) or (0, None)
        if attempts >= 5:
            messages.error(request, 'تلاش‌های ورود بیش از حد. لطفاً بعداً دوباره تلاش کنید.')
            form = CustomAuthenticationForm(request, data=request.POST)
            next_url = request.POST.get('next') or request.GET.get('next', '')
            return render(request, 'accounts/login.html', {'form': form, 'next': next_url})
        
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید {username}!')
                # احترام به پارامتر next با بررسی امن بودن URL
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                # افزایش شمارنده تلاش‌ها در صورت شکست
                cache.set(key, (attempts + 1, timezone.now()), timeout=600)
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        else:
            cache.set(key, (attempts + 1, timezone.now()), timeout=600)
    else:
        form = CustomAuthenticationForm()
    # عبور دادن next به قالب برای درج ورودی مخفی
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    """
    خروج کاربر
    """
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('home')

@login_required
def profile(request):
    """
    نمایش پروفایل کاربر
    """
    return render(request, 'accounts/profile.html')

def contact(request):
    """
    صفحه تماس با ما: دریافت اطلاعات و ذخیره پیام کاربر
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما دریافت شد. به زودی پاسخ داده می‌شود.')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'accounts/contact.html', {'form': form})