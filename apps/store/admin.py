from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'guarantee_type')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    date_hierarchy = 'created_at'
    ordering = ('is_active', '-created_at')
