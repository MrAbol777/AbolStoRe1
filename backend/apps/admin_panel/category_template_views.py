from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.store.models import Category
from .forms import CategoryForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_categories_list(request):
    categories = Category.objects.all().order_by('order')
    context = {
        'categories': categories
    }
    return render(request, 'admin_panel/admin_categories_list.html', context)

@staff_member_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی با موفقیت ایجاد شد.')
            return redirect('admin_panel:admin_categories_list')
        else:
            messages.error(request, 'خطا در ایجاد دسته بندی.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'ایجاد دسته بندی جدید'
    }
    return render(request, 'admin_panel/admin_category_form.html', context)

@staff_member_required
def admin_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی با موفقیت ویرایش شد.')
            return redirect('admin_panel:admin_categories_list')
        else:
            messages.error(request, 'خطا در ویرایش دسته بندی.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'title': f'ویرایش دسته بندی: {category.name}'
    }
    return render(request, 'admin_panel/admin_category_form.html', context)

@staff_member_required
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'دسته بندی با موفقیت حذف شد.')
        return redirect('admin_panel:admin_categories_list')
    
    context = {
        'category': category,
        'title': f'حذف دسته بندی: {category.name}'
    }
    return render(request, 'admin_panel/admin_category_confirm_delete.html', context)
