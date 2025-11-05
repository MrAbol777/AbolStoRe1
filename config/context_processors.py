"""
Context processors for Abol Store
"""
from apps.orders.models import Order
from apps.store.models import Category

def cart_count(request):
    """
    Add cart count to all templates
    """
    cart_count = 0
    
    if request.user.is_authenticated:
        # Count pending orders (orders that are not completed)
        cart_count = Order.objects.filter(
            user=request.user,
            status__in=['pending', 'waiting']
        ).count()
    
    return {'cart_count': cart_count}

def categories_context(request):
    """
    Add all active categories to all templates
    """
    categories = Category.objects.filter(is_active=True).order_by('name')
    return {'categories': categories}