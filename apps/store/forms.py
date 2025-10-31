# فرم‌های مربوط به محصولات و کمبوها
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """فرم ایجاد و ویرایش محصول"""
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'guarantee_type', 'stock', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'stock': forms.NumberInput(attrs={'min': 0}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن کلاس‌های تیلویند به فرم
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500'
            })