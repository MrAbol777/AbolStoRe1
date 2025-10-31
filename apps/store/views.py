# نمایش‌ها و کنترلرهای مربوط به محصولات و کمبوها
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from apps.orders.forms import OrderForm

class HomeView(ListView):
    """نمایش صفحه اصلی و لیست محصولات"""
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        # فقط محصولات فعال را نمایش می‌دهد
        return Product.objects.filter(is_active=True)

class ProductDetailView(DetailView):
    """نمایش جزئیات محصول"""
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن فرم سفارش به صفحه جزئیات محصول
        context['order_form'] = OrderForm(initial={'product': self.object, 'quantity': 1})
        return context

@login_required
def product_list_admin(request):
    """نمایش لیست محصولات برای ادمین"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/admin/product_list.html', {'products': products})

@login_required
def product_create(request):
    """ایجاد محصول جدید"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('home')
        
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت ایجاد شد.')
            return redirect('product_list_admin')
    else:
        form = ProductForm()
    
    return render(request, 'store/admin/product_form.html', {'form': form, 'title': 'ایجاد محصول جدید'})

@login_required
def product_update(request, pk):
    """ویرایش محصول"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('home')
        
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت بروزرسانی شد.')
            return redirect('product_list_admin')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/admin/product_form.html', {'form': form, 'title': 'ویرایش محصول', 'product': product})

@login_required
def product_delete(request, pk):
    """حذف محصول"""
    if not request.user.is_staff:
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('home')
        
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد.')
        return redirect('product_list_admin')
    
    return render(request, 'store/admin/product_confirm_delete.html', {'product': product})