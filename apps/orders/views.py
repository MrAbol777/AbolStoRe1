# نمایش‌ها و کنترلرهای مربوذ به سفارش و پرداخت
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
import csv
from datetime import datetime
from django.utils import timezone

from .models import Order, Payment
from .forms import OrderForm, PaymentForm
from apps.telegram_bot.utils import send_telegram_notification

@login_required
def create_order(request):
    """ایجاد سفارش جدید"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            # محاسبه قیمت کل
            product = order.product
            order.total_price = product.price * order.quantity
            
            # اعمال تخفیف در صورت وجود کد معرف (مثلا 10 درصد)
            if order.referral_code:
                discount = order.total_price * 0.1
                order.total_price -= discount
                
            order.save()
            
            # ارسال اعلان به تلگرام (فقط برای سفارش‌ها)
            message = f"📦 سفارش جدید ثبت شد!\n\n👤 مشتری: {order.user.phone_number}\n🛍️ محصول: {product.name}\n📊 تعداد: {order.quantity}\n💰 مبلغ کل: {order.total_price:,} تومان\n\n✅ لطفاً جهت بررسی به پنل ادمین مراجعه کنید."
            send_telegram_notification(message, chat_id=order.user.telegram_id, user=order.user, order=order)
            
            messages.success(request, "سفارش شما با موفقیت ثبت شد. لطفا پرداخت را انجام دهید.")
            return redirect('orders:order_payment', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'orders/create_order.html', {'form': form})

@login_required
def order_payment(request, order_id):
    """صفحه پرداخت سفارش"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # اگر سفارش قبلا پرداخت شده باشد
    if hasattr(order, 'payment'):
        return redirect('orders:order_detail', order_id=order.id)
    
    # دریافت شماره کارت از تنظیمات
    card_number = getattr(settings, 'CARD_NUMBER', '6037-9981-9893-7616')
    card_owner = getattr(settings, 'CARD_OWNER', 'ابوالفضل دوست‌گل')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.card_number = card_number
            payment.save()
            
            # تغییر وضعیت سفارش به در انتظار تایید
            order.status = 'waiting'
            order.save()
            
            # ارسال اعلان به تلگرام (فقط برای سفارش‌ها)
            message = f"📄 رسید پرداخت آپلود شد!\n\n👤 مشتری: {order.user.phone_number}\n🛍️ محصول: {order.product.name}\n💰 مبلغ: {order.total_price:,} تومان\n\n⏳ لطفاً جهت بررسی و تایید به پنل ادمین مراجعه کنید."
            send_telegram_notification(message, chat_id=order.user.telegram_id, user=order.user, order=order)
            
            messages.success(request, "رسید پرداخت شما با موفقیت آپلود شد. منتظر تأیید ادمین باشید.")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = PaymentForm()
    
    return render(request, 'orders/payment.html', {
        'form': form,
        'order': order,
        'card_number': card_number,
        'card_owner': card_owner
    })

@login_required
def order_detail(request, order_id):
    """نمایش جزئیات سفارش"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    """نمایش لیست سفارشات کاربر"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

# نمایش‌های مدیریت سفارش (ادمین)

@login_required
def admin_order_list(request):
    """نمایش لیست سفارشات برای ادمین"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    
    # فیلتر بر اساس وضعیت
    status = request.GET.get('status', '')
    if status:
        orders = Order.objects.filter(status=status).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')
    
    return render(request, 'orders/admin/order_list.html', {'orders': orders, 'current_status': status})

@login_required
def admin_order_detail(request, order_id):
    """نمایش جزئیات سفارش برای ادمین"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            # تایید سفارش
            if hasattr(order, 'payment'):
                order.status = 'confirmed'
                order.save()
                
                # تغییر وضعیت پرداخت
                payment = order.payment
                payment.is_verified = True
                payment.verified_by = request.user
                payment.verified_at = timezone.now()
                payment.save()
                
                # کاهش موجودی محصول
                product = order.product
                product.stock -= order.quantity
                product.save()
                
                # ارسال اعلان به تلگرام (فقط برای سفارش‌ها)
                message = f"✅ سفارش تایید شد!\n\n👤 مشتری: {order.user.phone_number}\n🛍️ محصول: {order.product.name}\n📊 تعداد: {order.quantity}\n💰 مبلغ: {order.total_price:,} تومان\n\n📦 سفارش آماده ارسال است."
                send_telegram_notification(message, chat_id=order.user.telegram_id, user=order.user, order=order)
                
                messages.success(request, "سفارش با موفقیت تایید شد.")
            else:
                messages.error(request, "این سفارش هنوز پرداخت نشده است.")
        
        elif action == 'reject':
            # رد سفارش
            if hasattr(order, 'payment'):
                order.status = 'rejected'
                order.save()
                
                # تغییر وضعیت پرداخت
                payment = order.payment
                payment.is_verified = False
                payment.verified_by = request.user
                payment.verified_at = timezone.now()
                payment.save()
                
                # ارسال اعلان به تلگرام (فقط برای سفارش‌ها)
                message = f"❌ سفارش رد شد!\n\n👤 مشتری: {order.user.phone_number}\n🛍️ محصول: {order.product.name}\n💰 مبلغ: {order.total_price:,} تومان\n\n❗️ دلیل: عدم تطابق اطلاعات پرداخت یا رسید نامعتبر"
                send_telegram_notification(message, chat_id=order.user.telegram_id, user=order.user, order=order)
                
                messages.success(request, "سفارش با موفقیت رد شد.")
            else:
                messages.error(request, "این سفارش هنوز پرداخت نشده است.")
    
    return render(request, 'orders/admin/order_detail.html', {'order': order})

@login_required
def export_orders_csv(request):
    """خروجی CSV از سفارشات"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="orders-{datetime.now().strftime("%Y-%m-%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['شناسه', 'کاربر', 'محصول', 'تعداد', 'قیمت کل', 'کد معرف', 'وضعیت', 'تاریخ ایجاد'])
    
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        writer.writerow([
            order.id,
            order.user.phone_number,
            order.product.name,
            order.quantity,
            order.total_price,
            order.referral_code or '',
            order.get_status_display(),
            order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response