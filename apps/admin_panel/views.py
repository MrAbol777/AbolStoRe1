"""
ویوهای ادمین برای داشبورد مدیریت
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os
import json

from apps.orders.models import Order, Payment
from apps.accounts.models import User, ContactMessage
from apps.store.models import Product, Category
from apps.telegram_bot.utils import send_telegram_notification
from dotenv import load_dotenv, set_key
from apps.store.forms import ProductForm, CategoryForm
from django.core.paginator import Paginator
from apps.accounts.forms import UserEditForm
from .forms import OrderEditForm
from django.contrib.auth import authenticate, login, logout
from apps.accounts.forms import CustomAuthenticationForm

# Decorators
def admin_required(view_func):
    @login_required(login_url='admin_panel:admin_login')
    @user_passes_test(lambda user: user.is_staff or user.is_superuser, login_url='admin_panel:admin_login')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


# Views
@admin_required
def admin_dashboard(request):
    """داشبورد اصلی ادمین با آمار فروش"""
    
    # آمار کلی
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_products = Product.objects.count()
    
    # سفارشات امروز
    today = timezone.now().date()
    new_orders_today = Order.objects.filter(created_at__date=today).count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    
    # فروش کل
    total_sales = Order.objects.filter(status='confirmed').aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # فروش امروز
    sales_today = Order.objects.filter(
        status='confirmed',
        created_at__date=today
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # سفارشات در انتظار تأیید
    pending_orders = Order.objects.filter(status='waiting').count()
    
    # سفارشات اخیر (آخرین 10)
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # آمار 7 روز اخیر
    last_7_days = timezone.now() - timedelta(days=7)
    daily_orders = Order.objects.filter(
        created_at__gte=last_7_days
    ).annotate(
        day=TruncDate('created_at')
    ).values('day').annotate(
        count=Count('id'),
        total=Sum('total_price')
    ).order_by('day')
    
    # محصولات پرفروش
    top_products = Product.objects.annotate(
        total_sold=Sum('orders__quantity', filter=Q(orders__status='confirmed'))
    ).filter(total_sold__isnull=False).order_by('-total_sold')[:10]
    
    # تنظیمات از فایل .env
    card_number = os.getenv('CARD_NUMBER', '')
    card_owner = os.getenv('CARD_OWNER', '')
    telegram_admin_chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID', '')
    
    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'new_orders_today': new_orders_today,
        'new_users_today': new_users_today,
        'total_sales': total_sales,
        'sales_today': sales_today,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'daily_orders': daily_orders,
        'top_products': top_products,
        'card_number': card_number,
        'card_owner': card_owner,
        'telegram_admin_chat_id': telegram_admin_chat_id,
        'title': 'داشبورد مدیریت',
    }
    return render(request, 'admin/dashboard.html', context)


@admin_required
def admin_users_list(request):
    """لیست کاربران برای ادمین"""
    users_list = User.objects.annotate(
        orders_count=Count('orders'),
        total_spent=Sum('orders__total_price', filter=Q(orders__status='confirmed'))
    ).order_by('-date_joined')
    
    # جستجو
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = users_list.filter(
            Q(phone_number__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )
    
    paginator = Paginator(users_list, 10)  # نمایش 10 کاربر در هر صفحه
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'admin/users_list.html', context)


@admin_required
def admin_user_edit(request, user_id):
    """ویرایش کاربر موجود"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'کاربر با موفقیت به‌روزرسانی شد.')
            return redirect('admin_panel:admin_users_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'admin/user_edit.html', {'form': form, 'user': user, 'title': 'ویرایش کاربر'})


@admin_required
def admin_user_delete(request, user_id):
    """حذف کاربر"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'کاربر با موفقیت حذف شد.')
        return redirect('admin_panel:admin_users_list')
    return render(request, 'admin/user_confirm_delete.html', {'user': user, 'title': 'حذف کاربر'})


@admin_required
def admin_user_detail(request, user_id):
    """نمایش جزئیات کاربر"""
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
        'title': 'جزئیات کاربر',
    }
    return render(request, 'admin/user_detail.html', context)


@admin_required
def admin_products_list(request):
    print("admin_products_list function called")
    """لیست محصولات برای ادمین"""
    products_list = Product.objects.annotate(
        total_sold=Sum('orders__quantity', filter=Q(orders__status='confirmed')),
        total_revenue=Sum(F('orders__quantity') * F('price'), filter=Q(orders__status='confirmed'))
    ).order_by('-created_at')
    print(f"Initial products_list count: {products_list.count()}")

    # جستجو
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    print(f"Products_list count after search filter: {products_list.count()}")

    paginator = Paginator(products_list, 10)  # نمایش 10 محصول در هر صفحه
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    print(f"Products count after pagination: {len(products)}")

    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'admin/products_list.html', context)


@admin_required
def admin_product_create(request):
    """ایجاد محصول جدید"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'محصول با موفقیت ایجاد شد.')
            return redirect('admin_panel:admin_products_list') # Changed redirect to admin_panel:admin_products_list
        else:
            print("Form is not valid. Errors:", form.errors)
            messages.error(request, 'خطا در ایجاد محصول. لطفا اطلاعات را بررسی کنید.')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form, 'title': 'ایجاد محصول جدید'})


@admin_required
def admin_product_edit(request, product_id):
    """ویرایش محصول موجود"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت به‌روزرسانی شد.')
            return redirect('admin_panel:admin_products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form, 'title': 'ویرایش محصول', 'product': product})


@admin_required
def admin_product_delete(request, product_id):
    """حذف محصول"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد.')
        return redirect('admin_panel:admin_products_list')
    return render(request, 'admin/product_confirm_delete.html', {'product': product, 'title': 'حذف محصول'})


@admin_required
def admin_orders_list(request):
    """لیست سفارشات برای ادمین"""
    orders_list = Order.objects.select_related('user', 'product').order_by('-created_at')
    
    # فیلتر بر اساس وضعیت
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders_list = orders_list.filter(status=status_filter)
    
    # جستجو
    search_query = request.GET.get('search', '')
    if search_query:
        orders_list = orders_list.filter(
            Q(user__username__icontains=search_query) |
            Q(user__phone_number__icontains=search_query) |
            Q(product__name__icontains=search_query)
        )
    
    paginator = Paginator(orders_list, 10)  # نمایش 10 سفارش در هر صفحه
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'admin/orders_list.html', context)


@admin_required
def admin_order_edit(request, order_id):
    """ویرایش سفارش موجود"""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'سفارش با موفقیت به‌روزرسانی شد.')
            return redirect('admin_panel:admin_orders_list')
    else:
        form = OrderEditForm(instance=order)
    return render(request, 'admin/order_edit.html', {'form': form, 'order': order, 'title': 'ویرایش سفارش'})


@admin_required
def admin_order_delete(request, order_id):
    """حذف سفارش"""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'سفارش با موفقیت حذف شد.')
        return redirect('admin_panel:admin_orders_list')
    return render(request, 'admin/order_confirm_delete.html', {'order': order, 'title': 'حذف سفارش'})


@admin_required
def admin_order_detail(request, order_id):
    """نمایش جزئیات سفارش با اطلاعات کامل"""
    order = get_object_or_404(Order.objects.select_related('user', 'product'), id=order_id)
    
    # محاسبه اطلاعات آماری
    user_orders = Order.objects.filter(user=order.user)
    user_total_orders = user_orders.count()
    user_completed_orders = user_orders.filter(status='delivered').count()
    user_total_spent = user_orders.filter(status='delivered').aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # تاریخچه وضعیت‌ها
    status_history = []
    if order.status != 'waiting':
        status_history.append({
            'status': 'waiting',
            'display': 'در انتظار پرداخت',
            'date': order.created_at,
            'active': order.status == 'waiting'
        })
    if order.status in ['paid', 'confirmed', 'sent', 'delivered']:
        if order.payment_receipt_uploaded_at:
            status_history.append({
                'status': 'paid',
                'display': 'پرداخت شده',
                'date': order.payment_receipt_uploaded_at,
                'active': order.status == 'paid'
            })
    if order.status in ['confirmed', 'sent', 'delivered']:
        status_history.append({
            'status': 'confirmed',
            'display': 'تأیید شده',
            'date': order.updated_at,
            'active': order.status == 'confirmed'
        })
    if order.status in ['sent', 'delivered']:
        status_history.append({
            'status': 'sent',
            'display': 'ارسال شده',
            'date': order.updated_at,
            'active': order.status == 'sent'
        })
    if order.status == 'delivered':
        status_history.append({
            'status': 'delivered',
            'display': 'تحویل داده شده',
            'date': order.updated_at,
            'active': order.status == 'delivered'
        })

    context = {
        'order': order,
        'title': f'جزئیات سفارش #{order.id}',
        'user_total_orders': user_total_orders,
        'user_completed_orders': user_completed_orders,
        'user_total_spent': user_total_spent,
        'status_history': status_history,
    }
    return render(request, 'admin/order_detail.html', context)


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:admin_dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید.')
                return redirect('admin_panel:admin_dashboard')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        else:
            messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'admin/login.html', {'form': form, 'title': 'ورود به پنل مدیریت'})


def admin_logout(request):
    logout(request)
    messages.success(request, 'شما با موفقیت از سیستم خارج شدید.')
    return redirect('admin_panel:admin_login')


@admin_required
def admin_settings(request):
    """تنظیمات ادمین"""
    # بارگذاری تنظیمات موجود
    card_number = os.getenv('CARD_NUMBER', '')
    card_owner = os.getenv('CARD_OWNER', '')

    context = {
        'title': 'تنظیمات',
        'card_number': card_number,
        'card_owner': card_owner,
    }
    return render(request, 'admin/settings.html', context)

@admin_required
def admin_update_settings(request):
    """به‌روزرسانی تنظیمات ادمین"""
    if request.method == 'POST':
        card_number = request.POST.get('card_number', '')
        card_owner = request.POST.get('card_owner', '')

        # به‌روزرسانی فایل .env
        load_dotenv()
        set_key('.env', 'CARD_NUMBER', card_number)
        set_key('.env', 'CARD_OWNER', card_owner)

        messages.success(request, 'تنظیمات با موفقیت ذخیره شد.')
    return redirect('admin_panel:admin_settings')


@admin_required
def admin_contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/contact_messages.html', {'page_obj': page_obj, 'title': 'پیام‌های تماس'})


@admin_required
def admin_contact_message_delete(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'پیام تماس با موفقیت حذف شد.')
        return redirect('admin_panel:admin_contact_messages')
    return render(request, 'admin/contact_message_confirm_delete.html', {'message': message, 'title': 'حذف پیام تماس'})


@admin_required
def admin_order_detail_api(request, order_id):
    """API برای دریافت اطلاعات کامل سفارش"""
    try:
        order = get_object_or_404(Order.objects.select_related('user', 'product', 'payment'), id=order_id)
        
        # محاسبه اطلاعات آماری کاربر
        user_orders = Order.objects.filter(user=order.user)
        user_total_orders = user_orders.count()
        user_completed_orders = user_orders.filter(status='delivered').count()
        user_total_spent = user_orders.filter(status='delivered').aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # ایجاد timeline وضعیت
        status_timeline = []
        if order.status != 'waiting':
            status_timeline.append({
                'status': 'waiting',
                'title': 'در انتظار پرداخت',
                'date': order.created_at.strftime('%Y/%m/%d - %H:%M'),
                'description': 'سفارش ثبت شده و در انتظار پرداخت است'
            })
        
        # وضعیت‌های بعدی رو اضافه کن
        status_order = ['waiting', 'paid', 'confirmed', 'sent', 'delivered']
        current_status_index = status_order.index(order.status) if order.status in status_order else -1
        
        for i, status in enumerate(status_order):
            if i <= current_status_index and status != 'waiting':
                status_timeline.append({
                    'status': status,
                    'title': order.get_status_display(),
                    'date': order.updated_at.strftime('%Y/%m/%d - %H:%M'),
                    'description': f'سفارش به وضعیت {order.get_status_display()} تغییر یافت'
                })
        
        # اطلاعات سفارش - با ساختار مورد انتظار JavaScript
        # اضافه کردن اطلاعات رسید پرداخت
        payment_receipt_url = order.payment.receipt.url if hasattr(order, 'payment') and order.payment.receipt else None
        
        order_data = {
            'id': order.id,
            'user': {
                'id': order.user.id,
                'username': order.user.username,
                'phone_number': order.user.phone_number,
                'email': order.user.email,
            },
            'product': {
                'id': order.product.id,
                'name': order.product.name,
                'image': order.product.image.url if order.product.image else None,
                'price': str(order.product.price),
            },
            'quantity': order.quantity,
            'total_price': str(order.total_price),
            'status': order.status,
            'status_display': order.get_status_display(),
            'created_at': order.created_at.strftime('%Y/%m/%d - %H:%M'),
            'updated_at': order.updated_at.strftime('%Y/%m/%d - %H:%M'),
            'payment_receipt': payment_receipt_url, # اضافه کردن payment_receipt
            'status_timeline': status_timeline,
            'user_stats': {
                'total_orders': user_total_orders,
                'completed_orders': user_completed_orders,
                'total_spent': str(user_total_spent),
            }
        }
        
        return JsonResponse({'success': True, 'order': order_data})
    except Http404:
        return JsonResponse({'success': False, 'error': 'سفارش یافت نشد.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@admin_required
@require_POST
def admin_approve_order(request, order_id):
    """تأیید سفارش"""
    try:
        order = get_object_or_404(Order, id=order_id)
        message_text = request.POST.get('message', '')
        
        # تغییر وضعیت سفارش
        order.status = 'confirmed'
        order.save()
        
        # ارسال پیام به کاربر
        if message_text:
            # اینجا می‌توانید از سیستم پیام‌رسانی خود استفاده کنید
            # برای حالا فقط لاگ می‌کنیم
            print(f"پیام به کاربر {order.user.username}: {message_text}")
        
        # ارسال نوتیفیکیشن تلگرام
        try:
            telegram_message = f"""
✅ سفارش شماره {order.id} تأیید شد!

📋 جزئیات سفارش:
• محصول: {order.product.name}
• مبلغ: {order.total_price:,} تومان
• تعداد: {order.quantity}

💬 پیام ادمین: {message_text if message_text else 'سفارش شما تأیید شد. ممنون از خریدتون!'}
            """
            # ارسال به تلگرام (در صورت فعال بودن)
            # send_telegram_notification(order.user.telegram_id, telegram_message)
        except:
            pass
        
        return JsonResponse({
            'success': True, 
            'message': 'سفارش با موفقیت تأیید شد.',
            'new_status': 'confirmed',
            'new_status_display': 'تأیید شده'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@admin_required
@require_POST
def admin_reject_order(request, order_id):
    """رد سفارش"""
    try:
        order = get_object_or_404(Order, id=order_id)
        reason = request.POST.get('reason', '')
        
        # تغییر وضعیت سفارش
        order.status = 'rejected'
        order.save()
        
        # ارسال پیام به کاربر
        if reason:
            # اینجا می‌توانید از سیستم پیام‌رسانی خود استفاده کنید
            print(f"پیام رد سفارش به کاربر {order.user.username}: {reason}")
        
        # ارسال نوتیفیکیشن تلگرام
        try:
            telegram_message = f"""
❌ سفارش شماره {order.id} رد شد!

📋 جزئیات سفارش:
• محصول: {order.product.name}
• مبلغ: {order.total_price:,} تومان

💬 دلیل رد: {reason if reason else 'سفارش شما بررسی شد و متأسفانه قابل تأیید نمی‌باشد.'}

📞 برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.
            """
            # send_telegram_notification(order.user.telegram_id, telegram_message)
        except:
            pass
        
        return JsonResponse({
            'success': True, 
            'message': 'سفارش با موفقیت رد شد.',
            'new_status': 'rejected',
            'new_status_display': 'رد شده'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@admin_required
@require_POST
def admin_send_order_message(request, order_id):
    """ارسال پیام به خریدار"""
    try:
        order = get_object_or_404(Order, id=order_id)
        message_text = request.POST.get('message', '')
        
        if not message_text:
            return JsonResponse({'success': False, 'error': 'متن پیام نمی‌تواند خالی باشد.'})
        
        # اینجا می‌توانید از سیستم پیام‌رسانی خود استفاده کنید
        print(f"پیام ارسال شده به کاربر {order.user.username}: {message_text}")
        
        # ارسال نوتیفیکیشن تلگرام
        try:
            telegram_message = f"""
💬 پیام از ادمین:

{message_text}

📋 مربوط به سفارش شماره {order.id}
🛍️ محصول: {order.product.name}
            """
            # send_telegram_notification(order.user.telegram_id, telegram_message)
        except:
            pass
        
        return JsonResponse({
            'success': True, 
            'message': 'پیام با موفقیت ارسال شد.'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})