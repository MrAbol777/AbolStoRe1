import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.store.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile

def debug_product_edit():
    print("--- Starting Product Debug Script ---")

    # 1. Create a dummy category if it doesn't exist
    category, created = Category.objects.get_or_create(name='Debug Category', slug='debug-category')
    if created:
        print(f"Created new category: {category.name}")
    else:
        print(f"Using existing category: {category.name}")

    # 2. Create a new product
    try:
        # Create a dummy image file
        dummy_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'
        dummy_image = SimpleUploadedFile("dummy_image.png", dummy_image_content, content_type="image/png")

        product = Product.objects.create(
            category=category,
            name='Test Product for Debugging',
            description='This is a test product created for debugging purposes.',
            price=10000,
            guarantee_type='metaK',
            stock=10,
            image=dummy_image,
            is_active=True
        )
        print(f"Successfully created product: {product.name} (PK: {product.pk})")
    except Exception as e:
        print(f"Error creating product: {e}")
        return

    # 3. Attempt to update the created product
    try:
        product.name = 'Updated Test Product Name'
        product.price = 15000
        product.save()
        print(f"Successfully updated product: {product.name} (PK: {product.pk})")
    except Exception as e:
        print(f"Error updating product: {e}")

    print("--- Product Debug Script Finished ---")

if __name__ == '__main__':
    debug_product_edit()