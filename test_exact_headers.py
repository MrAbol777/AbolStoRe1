import requests

# هدر دقیق مثل مرورگر Trae
headers = {
    'Host': '127.0.0.1:8000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

# تست ساده بدون سشن
print("تست با هدر دقیق...")
try:
    response = requests.get('http://127.0.0.1:8000/', headers=headers, timeout=10, allow_redirects=True)
    print(f"کد وضعیت: {response.status_code}")
    print(f"طول محتوا: {len(response.text)} کاراکتر")
    
    if response.status_code == 200:
        print("✓ موفق بود!")
        print("اولین 100 کاراکتر:", response.text[:100])
    else:
        print(f"سرور پاسخ داد ولی با کد: {response.status_code}")
        print("محتوا:", response.text[:200] if response.text else "خالی")
        
except requests.exceptions.RequestException as e:
    print(f"❌ خطا در درخواست: {e}")
    print(f"نوع خطا: {type(e)}")

# حالا تست لاگین
print("\nتست صفحه لاگین...")
try:
    response = requests.get('http://127.0.0.1:8000/accounts/login/', headers=headers, timeout=10)
    print(f"کد وضعیت لاگین: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ صفحه لاگین هم درسته!")
    else:
        print(f"مشکل در لاگین: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ خطا در لاگین: {e}")