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
from django.http import JsonResponse
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import ContactForm

def register_view(request):
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
                
                # Handle AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'ثبت‌نام با موفقیت انجام شد',
                        'redirect': reverse('store:home')
                    })
                
                return redirect('store:home')
            else:
                # Handle form errors
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        field_label = form.fields[field].label or field
                        errors.append(f'{field_label}: {error}')
                
                # Handle AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': errors
                    })
                
                # Handle regular request
                for error in errors:
                    messages.error(request, error)
        except Exception as e:
            error_msg = 'خطایی رخ داد. لطفاً دوباره تلاش کنید.'
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                })
            
            messages.error(request, error_msg)
        
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
            error_msg = 'تلاش‌های ورود بیش از حد. لطفاً بعداً دوباره تلاش کنید.'
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                })
            
            messages.error(request, error_msg)
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
                success_msg = f'خوش آمدید {username}!'
                
                # Handle AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': success_msg,
                        'redirect': reverse('store:home')
                    })
                
                messages.success(request, success_msg)
                
                # احترام به پارامتر next با بررسی امن بودن URL
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                # افزایش شمارنده تلاش‌ها در صورت شکست
                cache.set(key, (attempts + 1, timezone.now()), timeout=600)
                error_msg = 'نام کاربری یا رمز عبور اشتباه است.'
                
                # Handle AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    })
                
                messages.error(request, error_msg)
        else:
            cache.set(key, (attempts + 1, timezone.now()), timeout=600)
            error_msg = 'نام کاربری یا رمز عبور اشتباه است.'
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                })
            
            messages.error(request, error_msg)
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
    return redirect('store:home')

@login_required
def profile_view(request):
    """
    نمایش پروفایل کاربر
    """
    return render(request, 'accounts/profile.html')

def contact_view(request):
    """
    صفحه تماس با ما: دریافت اطلاعات و ذخیره پیام کاربر
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_msg = 'پیام شما دریافت شد. به زودی پاسخ داده می‌شود.'
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_msg,
                    'redirect': reverse('store:home')
                })
            
            messages.success(request, success_msg)
            return redirect('store:home')
        else:
            # Handle form errors
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    field_label = form.fields[field].label or field
                    errors.append(f'{field_label}: {error}')
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'خطا در ارسال پیام',
                    'errors': errors
                })
            
            # Handle regular request
            for error in errors:
                messages.error(request, error)
    else:
        form = ContactForm()
    return render(request, 'accounts/contact.html', {'form': form})