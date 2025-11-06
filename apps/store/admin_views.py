# نمایش‌ها و کنترلرهای مربوذ به پنل ادمین برای محصولات و دسته‌بندی‌ها
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Category
from .forms import ProductForm, CategoryForm
import json

@login_required
def product_list_admin(request):
    """نمایش لیست محصولات برای ادمین"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/admin/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت ایجاد شد.')
            return redirect('store:product_list_admin')
    else:
        form = ProductForm()
    
    return render(request, 'store/admin/product_form.html', {'form': form, 'title': 'ایجاد محصول جدید'})

@login_required
def product_update(request, pk):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت بروزرسانی شد.')
            return redirect('store:product_list_admin')
        else:
            messages.error(request, 'خطا در بروزرسانی محصول. لطفا اطلاعات را بررسی کنید.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/admin/product_form.html', {'form': form, 'product': product})

@login_required
def product_delete(request, pk):
    """حذف محصول"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
        
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد.')
        return redirect('store:product_list_admin')
    
    return render(request, 'store/admin/product_confirm_delete.html', {'product': product})


# Admin Category Views
@login_required
def admin_category_list(request):
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    categories = Category.objects.all().order_by('order', 'name')
    return render(request, 'store/admin/categories.html', {'categories': categories})

@login_required
def admin_category_create(request):
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی با موفقیت ایجاد شد.')
            return redirect('store:admin_category_list')
    else:
        form = CategoryForm()
    return render(request, 'store/admin/category_form.html', {'form': form, 'title': 'ایجاد دسته بندی جدید'})

@login_required
def admin_category_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی با موفقیت بروزرسانی شد.')
            return redirect('store:admin_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/admin/category_form.html', {'form': form, 'title': 'ویرایش دسته بندی', 'category': category})

@login_required
@require_POST
def admin_category_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('store:home')
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'دسته بندی با موفقیت حذف شد.')
    return redirect('store:admin_category_list')

@login_required
@require_POST
def admin_category_reorder(request):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'شما دسترسی به این بخش را ندارید.'})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_ids = data.get('category_ids', [])
            for index, category_id in enumerate(category_ids):
                Category.objects.filter(id=category_id).update(order=index)
            return JsonResponse({'status': 'success', 'message': 'ترتیب دسته بندی ها با موفقیت بروزرسانی شد.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

