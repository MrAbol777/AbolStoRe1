from django import forms
from apps.orders.models import Order
from apps.store.models import Product, Category

class OrderEditForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[('card', 'کارت به کارت'), ('online', 'پرداخت آنلاین')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='روش پرداخت'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label='یادداشت‌ها'
    )
    
    class Meta:
        model = Order
        fields = ['status', 'quantity', 'total_price', 'payment_method', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image', 'parent', 'is_active', 'order', 'meta_title', 'meta_description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'image': forms.ClearableFileInput(),
        }
