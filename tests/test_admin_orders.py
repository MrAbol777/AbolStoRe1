import requests
import re

# Create a session
session = requests.Session()

# Step 1: Get the login page to extract CSRF token
print("Getting login page...")
response = session.get("http://127.0.0.1:8000/accounts/login/")
print(f"Login page status: {response.status_code}")

# Extract CSRF token
csrf_token = ""
if 'csrfmiddlewaretoken' in response.text:
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', response.text)
    if match:
        csrf_token = match.group(1)
        print(f"CSRF token: {csrf_token[:20]}...")

# Step 2: Login
print("\nLogging in...")
login_data = {
    "username": "aboladmin",
    "password": "1234",
    "csrfmiddlewaretoken": csrf_token
}

response = session.post("http://127.0.0.1:8000/accounts/login/", data=login_data)
print(f"Login status: {response.status_code}")
print(f"Response URL: {response.url}")

# Check if login was successful
if "login" not in response.url and response.status_code == 200:
    print("✓ Login successful!")
    
    # Step 3: Access admin orders page
    print("\nAccessing admin orders page...")
    response = session.get("http://127.0.0.1:8000/orders/admin/")
    print(f"Admin orders status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Admin orders page accessible!")
        
        # Check if we can see orders content
        if "سفارش" in response.text or "order" in response.text.lower():
            print("✓ Orders content found!")
        else:
            print("⚠ Orders content not found")
            print("Response snippet:", response.text[:500])
    else:
        print("✗ Admin orders page not accessible")
        
    # Step 4: Access admin dashboard
    print("\nAccessing admin dashboard...")
    response = session.get("http://127.0.0.1:8000/admin-panel/")
    print(f"Admin dashboard status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Admin dashboard accessible!")
        if "داشبورد" in response.text or "dashboard" in response.text.lower():
            print("✓ Dashboard content found!")
        else:
            print("⚠ Dashboard content not found")
    else:
        print("✗ Admin dashboard not accessible")
        
else:
    print("✗ Login failed")
    print("Response snippet:", response.text[:300])