# نمایش‌ها و کنترلرهای مربوذ به محصولات و کمبوها
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from apps.orders.forms import OrderForm
import json

class HomeView(ListView):
    """نمایش صفحه اصلی و لیست محصولات"""
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        # فقط محصولات فعال را نمایش می‌دهد و بر اساس تعداد فروش مرتب می‌کند
        return Product.objects.filter(is_active=True).order_by('-sales_count', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
        context['categories'] = categories
        return context

class ProductDetailView(DetailView):
    """نمایش جزئیات محصول"""
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن فرم سفارش به صفحه جزئیات محصول
        context['order_form'] = OrderForm(initial={'product': self.object, 'quantity': 1})
        return context

class CategoryDetailView(ListView):
    """نمایش محصولات بر اساس دسته بندی"""
    model = Product
    template_name = 'store/category_detail.html' # این فایل را باید ایجاد کنیم
    context_object_name = 'products'
    paginate_by = 10 # تعداد محصولات در هر صفحه

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        if self.category.slug == "all-products":
            return Product.objects.filter(is_active=True).order_by('-sales_count', '-created_at')
        return Product.objects.filter(category=self.category, is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ProductListView(ListView):
    """نمایش محصولات بر اساس نوع (مثلاً کمبو، اکانت، سی پی)"""
    model = Product
    template_name = 'store/home.html'  # می‌توانید از همان قالب home.html استفاده کنید یا یک قالب جدید بسازید
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category=self.category, is_active=True).order_by('-created_at')