import requests

# اول صفحه لاگین رو بگیریم تا CSRF token رو پیدا کنیم
session = requests.Session()

# گرفتن صفحه لاگین
try:
    login_page = session.get('http://127.0.0.1:8000/accounts/login/', timeout=10)
    print(f"صفحه لاگین: {login_page.status_code}")
    
    if login_page.status_code == 200:
        # پیدا کردن CSRF token
        csrf_token = None
        if 'csrfmiddlewaretoken' in login_page.text:
            import re
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
            if match:
                csrf_token = match.group(1)
                print(f"✓ CSRF Token پیدا شد: {csrf_token[:10]}...")
        
        if csrf_token:
            # ارسال فرم لاگین
            login_data = {
                'csrfmiddlewaretoken': csrf_token,
                'username': 'aboladmin',
                'password': '1234',
                'next': '/admin-panel/'
            }
            
            login_response = session.post('http://127.0.0.1:8000/accounts/login/', 
                                        data=login_data, 
                                        headers={'Referer': 'http://127.0.0.1:8000/accounts/login/'},
                                        timeout=10)
            
            print(f"نتایج لاگین: {login_response.status_code}")
            
            if login_response.status_code == 302 or login_response.status_code == 200:
                print("✓ لاگین موفق بود!")
                
                # حالا تست دسترسی به پنل ادمین
                admin_response = session.get('http://127.0.0.1:8000/admin-panel/', timeout=10)
                print(f"دسترسی به پنل ادمین: {admin_response.status_code}")
                
                if admin_response.status_code == 200:
                    print("✓ پنل ادمین در دسترسه!")
                else:
                    print(f"مشکل در دسترسی به پنل ادمین: {admin_response.status_code}")
                    
                # تست صفحه مدیریت سفارش‌ها
                orders_response = session.get('http://127.0.0.1:8000/orders/admin/', timeout=10)
                print(f"دسترسی به مدیریت سفارش‌ها: {orders_response.status_code}")
                
                if orders_response.status_code == 200:
                    print("✓ مدیریت سفارش‌ها در دسترسه!")
                else:
                    print(f"مشکل در دسترسی به مدیریت سفارش‌ها: {orders_response.status_code}")
                    
            else:
                print(f"❌ لاگین ناموفق بود. کد وضعیت: {login_response.status_code}")
                print("محتوای پاسخ:", login_response.text[:200])
        else:
            print("❌ نتونستم CSRF token پیدا کنم")
            
    else:
        print(f"❌ نتونستم صفحه لاگین رو بگیرم. کد وضعیت: {login_page.status_code}")
        
except Exception as e:
    print(f"❌ خطا در اتصال: {e}")