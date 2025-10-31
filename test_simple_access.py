import requests

# Test simple access to login page
print("Testing login page access...")
try:
    response = requests.get("http://127.0.0.1:8000/accounts/login/", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    if "login" in response.text.lower():
        print("✓ Login page content found")
    else:
        print("⚠ Login page content not recognized")
        print("First 200 chars:", response.text[:200])
except Exception as e:
    print(f"✗ Error: {e}")

# Test admin panel access (should redirect)
print("\nTesting admin panel access...")
try:
    response = requests.get("http://127.0.0.1:8000/admin-panel/", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Final URL: {response.url}")
    if response.status_code == 302:
        print("✓ Redirected to login as expected")
    elif response.status_code == 200:
        print("✓ Admin panel accessible")
    else:
        print(f"⚠ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test orders admin access (should redirect)
print("\nTesting orders admin access...")
try:
    response = requests.get("http://127.0.0.1:8000/orders/admin/", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Final URL: {response.url}")
    if response.status_code == 302:
        print("✓ Redirected to login as expected")
    elif response.status_code == 200:
        print("✓ Orders admin accessible")
    else:
        print(f"⚠ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")