#!/bin/bash
# اسکریپت نصب و راه‌اندازی آبول استور
# این اسکریپت برای نصب و راه‌اندازی آبول استور در سرور لینوکس استفاده می‌شود

set -e

# رنگ‌ها برای خروجی
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== شروع نصب آبول استور ===${NC}"

# بررسی پیش‌نیازها
echo -e "${YELLOW}بررسی و نصب پیش‌نیازها...${NC}"
apt update
apt install -y python3-pip python3-venv nginx git

# ایجاد کاربر برای اجرای برنامه
echo -e "${YELLOW}ایجاد کاربر برای اجرای برنامه...${NC}"
useradd -m abolstore 2>/dev/null || echo "کاربر از قبل وجود دارد"
usermod -aG www-data abolstore

# ایجاد دایرکتوری نصب
echo -e "${YELLOW}ایجاد دایرکتوری نصب...${NC}"
mkdir -p /var/www/abolstore
chown abolstore:www-data /var/www/abolstore

# کلون کردن مخزن
echo -e "${YELLOW}کلون کردن مخزن...${NC}"
if [ -d "/var/www/abolstore/.git" ]; then
    echo "مخزن از قبل کلون شده است. در حال به‌روزرسانی..."
    cd /var/www/abolstore
    sudo -u abolstore git pull
else
    sudo -u abolstore git clone https://github.com/yourusername/abolstore.git /var/www/abolstore
fi

# ایجاد محیط مجازی و نصب وابستگی‌ها
echo -e "${YELLOW}ایجاد محیط مجازی و نصب وابستگی‌ها...${NC}"
cd /var/www/abolstore
sudo -u abolstore python3 -m venv venv
sudo -u abolstore venv/bin/pip install -r requirements.txt
sudo -u abolstore venv/bin/pip install gunicorn

# تنظیم فایل محیطی
echo -e "${YELLOW}تنظیم فایل محیطی...${NC}"
if [ ! -f "/var/www/abolstore/.env" ]; then
    sudo -u abolstore cp .env.example .env
    echo -e "${GREEN}فایل .env ایجاد شد. لطفاً آن را ویرایش کنید:${NC}"
    echo "sudo nano /var/www/abolstore/.env"
else
    echo "فایل .env از قبل وجود دارد."
fi

# اجرای مایگریشن‌ها و جمع‌آوری فایل‌های استاتیک
echo -e "${YELLOW}اجرای مایگریشن‌ها و جمع‌آوری فایل‌های استاتیک...${NC}"
cd /var/www/abolstore
sudo -u abolstore venv/bin/python manage.py migrate
sudo -u abolstore venv/bin/python manage.py collectstatic --noinput

# ایجاد کاربر ادمین (اختیاری)
echo -e "${YELLOW}آیا می‌خواهید کاربر ادمین ایجاد کنید؟ (y/n)${NC}"
read -r create_admin
if [ "$create_admin" = "y" ]; then
    sudo -u abolstore venv/bin/python manage.py createsuperuser
fi

# تنظیم Gunicorn
echo -e "${YELLOW}تنظیم Gunicorn...${NC}"
cp /var/www/abolstore/deploy/abolstore.service /etc/systemd/system/
systemctl daemon-reload
systemctl start abolstore
systemctl enable abolstore

# تنظیم Nginx
echo -e "${YELLOW}تنظیم Nginx...${NC}"
cp /var/www/abolstore/deploy/nginx.conf /etc/nginx/sites-available/abolstore
ln -sf /etc/nginx/sites-available/abolstore /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

echo -e "${GREEN}=== نصب آبول استور با موفقیت انجام شد ===${NC}"
echo -e "می‌توانید با مراجعه به آدرس دامنه خود به برنامه دسترسی داشته باشید."
echo -e "برای بررسی وضعیت سرویس: ${YELLOW}systemctl status abolstore${NC}"
echo -e "برای مشاهده لاگ‌ها: ${YELLOW}journalctl -u abolstore${NC}"