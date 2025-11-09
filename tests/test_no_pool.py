import requests

# ساختن سشن با تنظیمات خاص
session = requests.Session()

# غیرفعال کردن کانکشن پولینگ
session.keep_alive = False

# هدر ساده
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Connection': 'close'  # مهم: بستن کانکشن بعد از هر درخواست
}

print("تست با تنظیمات خاص...")
try:
    response = session.get('http://127.0.0.1:8000/', headers=headers, timeout=10)
    print(f"کد وضعیت: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ موفق بود!")
        print(f"طول محتوا: {len(response.text)} کاراکتر")
    else:
        print(f"کد وضعیت: {response.status_code}")
        print("محتوا:", response.text[:100] if response.text else "خالی")
        
except Exception as e:
    print(f"❌ خطا: {e}")
    print(f"نوع خطا: {type(e)}")

# حالا تست با urllib ساده
print("\nتست با urllib...")
import urllib.request
import urllib.error

try:
    req = urllib.request.Request('http://127.0.0.1:8000/')
    response = urllib.request.urlopen(req, timeout=10)
    print(f"کد وضعیت urllib: {response.getcode()}")
    content = response.read().decode('utf-8')
    print(f"طول محتوا: {len(content)} کاراکتر")
    print("✓ urllib هم کار کرد!")
except Exception as e:
    print(f"❌ خطا در urllib: {e}")