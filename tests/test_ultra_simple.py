import requests

# تست ساده دسترسی به صفحه اصلی
try:
    response = requests.get('http://127.0.0.1:8000/', timeout=5)
    print(f"صفحه اصلی: {response.status_code}")
    if response.status_code == 200:
        print("✓ سرور درسته و صفحه اصلی لود میشه!")
    else:
        print(f"کد وضعیت غیرمنتظره: {response.status_code}")
except Exception as e:
    print(f"❌ خطا در اتصال: {e}")

# حالا تست صفحه لاگین
try:
    response = requests.get('http://127.0.0.1:8000/accounts/login/', timeout=5)
    print(f"صفحه لاگین: {response.status_code}")
    if response.status_code == 200:
        print("✓ صفحه لاگین هم درسته!")
    else:
        print(f"کد وضعیت غیرمنتظره برای لاگین: {response.status_code}")
except Exception as e:
    print(f"❌ خطا در اتصال به لاگین: {e}")