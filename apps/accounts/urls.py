"""
مسیرهای URL مربوط به کاربران در Abol Store
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    # تماس با ما
    path('contact/', views.contact, name='contact'),
]