import requests
import sys

# Test login with the admin user we created
session = requests.Session()

# First get the login page to get CSRF token
login_url = "http://127.0.0.1:8000/accounts/login/"
try:
    response = session.get(login_url)
    print(f"Login page status: {response.status_code}")
    
    # Extract CSRF token from the form
    if 'csrfmiddlewaretoken' in response.text:
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"CSRF token found: {csrf_token[:20]}...")
        else:
            print("CSRF token not found in form")
            csrf_token = ""
    else:
        print("No CSRF token in response")
        csrf_token = ""
    
    # Try to login
    login_data = {
        "username": "aboladmin",
        "password": "1234",
        "csrfmiddlewaretoken": csrf_token
    }
    
    response = session.post(login_url, data=login_data)
    print(f"Login POST status: {response.status_code}")
    print(f"Response URL: {response.url}")
    
    # Check if login was successful (should redirect to home or dashboard)
    if response.status_code == 200 and "login" not in response.url:
        print("✓ Login successful!")
        
        # Now try to access admin dashboard
        admin_url = "http://127.0.0.1:8000/admin-panel/"
        response = session.get(admin_url)
        print(f"Admin dashboard status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Admin dashboard accessible!")
            if "داشبورد ادمین" in response.text or "admin" in response.text.lower():
                print("✓ Admin dashboard content found!")
            else:
                print("⚠ Admin dashboard content not recognized")
        else:
            print("✗ Admin dashboard not accessible")
            
    else:
        print("✗ Login failed")
        print("Response snippet:", response.text[:500])
        
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to server - make sure it's running on port 8000")
except Exception as e:
    print(f"✗ Error: {e}")