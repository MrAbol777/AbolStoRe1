import requests

# هدر واقعی مرورگر
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# تست با هدر واقعی
try:
    response = requests.get('http://127.0.0.1:8000/', headers=headers, timeout=10)
    print(f"صفحه اصلی با هدر مرورگر: {response.status_code}")
    if response.status_code == 200:
        print("✓ با هدر مرورگر کار کرد!")
        print(f"طول محتوا: {len(response.text)} کاراکتر")
    else:
        print(f"کد وضعیت: {response.status_code}")
except Exception as e:
    print(f"❌ خطا: {e}")

# حالا تست لاگین
try:
    response = requests.get('http://127.0.0.1:8000/accounts/login/', headers=headers, timeout=10)
    print(f"صفحه لاگین با هدر مرورگر: {response.status_code}")
    if response.status_code == 200:
        print("✓ صفحه لاگین هم با هدر مرورگر کار کرد!")
    else:
        print(f"کد وضعیت لاگین: {response.status_code}")
except Exception as e:
    print(f"❌ خطا در لاگین: {e}")