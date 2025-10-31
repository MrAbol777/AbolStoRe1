# آبول استور - فروشگاه کمبوهای گیمینگ

فروشگاه آنلاین برای فروش کمبوها و اکانت‌های گیمینگ با سیستم پرداخت کارت به کارت و ارسال خودکار از طریق تلگرام.

## ویژگی‌ها

- رابط کاربری شیک و ریسپانسیو با Tailwind CSS
- پنل ادمین اختصاصی برای مدیریت محصولات و سفارشات
- سیستم پرداخت کارت به کارت با آپلود رسید
- اتصال به تلگرام برای ارسال اعلان‌ها و محصولات
- مدیریت کاربران، محصولات و سفارشات
- خروجی CSV از سفارشات

## پیش‌نیازها

- Python 3.8+
- pip
- virtualenv
- SQLite (یا PostgreSQL برای محیط تولید)

## نصب و راه‌اندازی محلی

1. کلون کردن مخزن:
```bash
git clone https://github.com/yourusername/abolstore.git
cd abolstore
```

2. ایجاد محیط مجازی و نصب وابستگی‌ها:
```bash
python -m venv venv
# در ویندوز
venv\Scripts\activate
# در لینوکس/مک
source venv/bin/activate

pip install -r requirements.txt
```

3. ایجاد فایل `.env` از روی نمونه:
```bash
cp .env.example .env
# سپس فایل .env را ویرایش کنید و مقادیر مورد نیاز را وارد کنید
```

4. اجرای مایگریشن‌ها و ایجاد کاربر ادمین:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. اجرای سرور توسعه:
```bash
python manage.py runserver
```

حالا می‌توانید به آدرس `http://127.0.0.1:8000` مراجعه کنید.

## نصب روی سرور (VPS)

### 1. آماده‌سازی سرور

```bash
# به‌روزرسانی پکیج‌ها
sudo apt update
sudo apt upgrade -y

# نصب پیش‌نیازها
sudo apt install -y python3-pip python3-venv nginx git

# ایجاد کاربر برای اجرای برنامه
sudo useradd -m abolstore
sudo usermod -aG www-data abolstore
```

### 2. کلون کردن پروژه

```bash
sudo mkdir -p /var/www/abolstore
sudo chown abolstore:www-data /var/www/abolstore
sudo -u abolstore git clone https://github.com/yourusername/abolstore.git /var/www/abolstore
```

### 3. نصب وابستگی‌ها

```bash
cd /var/www/abolstore
sudo -u abolstore python3 -m venv venv
sudo -u abolstore venv/bin/pip install -r requirements.txt
sudo -u abolstore venv/bin/pip install gunicorn
```

### 4. تنظیم فایل محیطی

```bash
sudo -u abolstore cp .env.example .env
# ویرایش فایل .env و وارد کردن مقادیر واقعی
sudo nano /var/www/abolstore/.env
```

### 5. اجرای مایگریشن‌ها و جمع‌آوری فایل‌های استاتیک

```bash
cd /var/www/abolstore
sudo -u abolstore venv/bin/python manage.py migrate
sudo -u abolstore venv/bin/python manage.py collectstatic --noinput
sudo -u abolstore venv/bin/python manage.py createsuperuser
```

### 6. تنظیم Gunicorn

```bash
sudo cp /var/www/abolstore/deploy/abolstore.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start abolstore
sudo systemctl enable abolstore
```

### 7. تنظیم Nginx

```bash
sudo cp /var/www/abolstore/deploy/nginx.conf /etc/nginx/sites-available/abolstore
sudo ln -s /etc/nginx/sites-available/abolstore /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. تنظیم فایروال (اختیاری)

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## نصب در Termux (اندروید)

```bash
# نصب پیش‌نیازها
pkg update
pkg install python git

# کلون کردن مخزن
git clone https://github.com/yourusername/abolstore.git
cd abolstore

# ایجاد محیط مجازی و نصب وابستگی‌ها
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# تنظیم فایل محیطی
cp .env.example .env
# ویرایش فایل .env

# اجرای مایگریشن‌ها
python manage.py migrate
python manage.py createsuperuser

# اجرای سرور
python manage.py runserver 0.0.0.0:8000
```

## توصیه‌های امنیتی

1. **تغییر SECRET_KEY**: حتماً مقدار `SECRET_KEY` را در فایل `.env` تغییر دهید.
2. **استفاده از HTTPS**: برای محیط تولید، حتماً از HTTPS استفاده کنید. می‌توانید از Let's Encrypt برای دریافت گواهی SSL رایگان استفاده کنید.
3. **محدود کردن دسترسی به فایل‌ها**: اطمینان حاصل کنید که فایل‌های آپلود شده فقط توسط کاربران مجاز قابل دسترسی هستند.
4. **به‌روزرسانی منظم**: سیستم و وابستگی‌ها را به طور منظم به‌روزرسانی کنید.
5. **پشتیبان‌گیری**: به طور منظم از دیتابیس و فایل‌های مهم پشتیبان‌گیری کنید.

## نمونه‌های API

### ثبت سفارش جدید

```bash
curl -X POST http://localhost:8000/api/orders/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"product_id": 1, "quantity": 1, "referral_code": ""}'
```

### دریافت لیست سفارشات

```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## مشارکت

درخواست‌های pull برای بهبود پروژه پذیرفته می‌شود. برای تغییرات بزرگ، لطفاً ابتدا یک issue باز کنید تا در مورد تغییرات مورد نظر بحث کنیم.

## مجوز

[MIT](https://choosealicense.com/licenses/mit/)