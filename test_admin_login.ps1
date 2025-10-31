# تست لاگین ادمین با PowerShell

Write-Host "شروع تست لاگین ادمین..." -ForegroundColor Green

# گرفتن صفحه لاگین
try {
    Write-Host "در حال گرفتن صفحه لاگین..." -ForegroundColor Yellow
    $loginPage = Invoke-WebRequest -Uri "http://127.0.0.1:8000/accounts/login/" -Method GET -TimeoutSec 10 -SessionVariable session
    
    Write-Host "✓ صفحه لاگین گرفته شد!" -ForegroundColor Green
    Write-Host "کد وضعیت: $($loginPage.StatusCode)"
    
    # پیدا کردن CSRF token
    $csrfToken = $null
    if ($loginPage.Content -match 'name="csrfmiddlewaretoken" value="([^"]+)"') {
        $csrfToken = $Matches[1]
        Write-Host "✓ CSRF Token پیدا شد: $($csrfToken.Substring(0, 10))..." -ForegroundColor Green
    }
    
    if ($csrfToken) {
        # ارسال فرم لاگین
        Write-Host "در حال ارسال فرم لاگین..." -ForegroundColor Yellow
        
        $loginForm = @{
            'csrfmiddlewaretoken' = $csrfToken
            'username' = 'aboladmin'
            'password' = '1234'
            'next' = '/admin-panel/'
        }
        
        $loginResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/accounts/login/" `
                                          -Method POST `
                                          -Body $loginForm `
                                          -WebSession $session `
                                          -TimeoutSec 10
        
        Write-Host "نتایج لاگین:" -ForegroundColor Cyan
        Write-Host "کد وضعیت: $($loginResponse.StatusCode)"
        
        if ($loginResponse.StatusCode -eq 200 -or $loginResponse.StatusCode -eq 302) {
            Write-Host "✓ لاگین موفق بود!" -ForegroundColor Green
            
            # تست دسترسی به پنل ادمین
            Write-Host "در حال تست دسترسی به پنل ادمین..." -ForegroundColor Yellow
            $adminResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin-panel/" `
                                             -Method GET `
                                             -WebSession $session `
                                             -TimeoutSec 10
            
            Write-Host "دسترسی به پنل ادمین: $($adminResponse.StatusCode)"
            if ($adminResponse.StatusCode -eq 200) {
                Write-Host "✓ پنل ادمین در دسترسه!" -ForegroundColor Green
            } else {
                Write-Host "⚠ پنل ادمین در دسترس نیست" -ForegroundColor Yellow
            }
            
            # تست صفحه مدیریت سفارش‌ها
            Write-Host "در حال تست صفحه مدیریت سفارش‌ها..." -ForegroundColor Yellow
            $ordersResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders/admin/" `
                                              -Method GET `
                                              -WebSession $session `
                                              -TimeoutSec 10
            
            Write-Host "دسترسی به مدیریت سفارش‌ها: $($ordersResponse.StatusCode)"
            if ($ordersResponse.StatusCode -eq 200) {
                Write-Host "✓ مدیریت سفارش‌ها در دسترسه!" -ForegroundColor Green
                
                # نمایش اطلاعات سفارش‌ها
                if ($ordersResponse.Content -match 'سفارش') {
                    Write-Host "✓ صفحه شامل اطلاعات سفارش‌هاست!" -ForegroundColor Green
                }
            } else {
                Write-Host "⚠ مدیریت سفارش‌ها در دسترس نیست" -ForegroundColor Yellow
            }
            
        } else {
            Write-Host "❌ لاگین ناموفق بود" -ForegroundColor Red
            Write-Host "محتوای پاسخ: $($loginResponse.Content.Substring(0, 200))..."
        }
    } else {
        Write-Host "❌ نتونستم CSRF token پیدا کنم" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ خطا در اتصال: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "تست تموم شد!" -ForegroundColor Green