"""
تست لاگین و دسترسی به داشبورد ادمین
"""
import requests
import os
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# آدرس سرور
base_url = "http://127.0.0.1:8000"

# تست لاگین
session = requests.Session()

# لاگین
login_data = {
    'username': 'aboladmin',
    'password': '1234'
}

print("🔄 در حال لاگین...")
response = session.post(f"{base_url}/accounts/login/", data=login_data)
print(f"وضعیت لاگین: {response.status_code}")

if response.status_code == 200:
    print("✅ لاگین موفق")
    
    # تست دسترسی به داشبورد
    print("🔄 در حال تست داشبورد...")
    dashboard_response = session.get(f"{base_url}/admin-panel/")
    print(f"وضعیت داشبورد: {dashboard_response.status_code}")
    
    if dashboard_response.status_code == 200:
        print("✅ دسترسی به داشبورد موفق")
        print(f"اندازه محتوا: {len(dashboard_response.text)} کاراکتر")
        
        # چک کردن محتوا
        if "داشبورد ادمین" in dashboard_response.text:
            print("✅ عنوان داشبورد پیدا شد")
        else:
            print("❌ عنوان داشبورد پیدا نشد")
            
        if "آمار فروش" in dashboard_response.text:
            print("✅ بخش آمار فروش پیدا شد")
        else:
            print("❌ بخش آمار فروش پیدا نشد")
            
    else:
        print(f"❌ خطا در دسترسی به داشبورد: {dashboard_response.status_code}")
else:
    print(f"❌ خطا در لاگین: {response.status_code}")
    print(response.text[:500])