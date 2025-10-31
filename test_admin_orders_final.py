import requests
import sys

def test_admin_access():
    """Test admin login and order management access"""
    session = requests.Session()
    
    # First, get the login page to extract CSRF token
    try:
        login_page = session.get('http://127.0.0.1:8000/accounts/login/')
        print(f"Login page status: {login_page.status_code}")
        
        if login_page.status_code != 200:
            print("Failed to load login page")
            return False
            
        # Look for CSRF token in the response
        csrf_token = None
        if 'csrfmiddlewaretoken' in login_page.text:
            import re
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', login_page.text)
            if match:
                csrf_token = match.group(1)
                print(f"Found CSRF token: {csrf_token[:20]}...")
        
        # Try to login
        login_data = {
            'username': 'aboladmin',
            'password': '1234'
        }
        
        if csrf_token:
            login_data['csrfmiddlewaretoken'] = csrf_token
            
        # Add headers to make it more realistic
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://127.0.0.1:8000/accounts/login/'
        }
        
        login_response = session.post('http://127.0.0.1:8000/accounts/login/', 
                                  data=login_data, headers=headers)
        print(f"Login POST status: {login_response.status_code}")
        
        # Check if login was successful (should redirect or show dashboard)
        if login_response.status_code in [200, 302]:
            print("Login attempt completed")
            
            # Try to access admin order management
            orders_response = session.get('http://127.0.0.1:8000/orders/admin/')
            print(f"Orders admin page status: {orders_response.status_code}")
            
            if orders_response.status_code == 200:
                print("SUCCESS: Can access order management!")
                if 'سفارش' in orders_response.text or 'order' in orders_response.text.lower():
                    print("SUCCESS: Order management page loaded correctly!")
                    return True
                else:
                    print("WARNING: Page loaded but may not be order management")
                    print("First 200 chars of response:", orders_response.text[:200])
                    return True
            elif orders_response.status_code == 302:
                print("INFO: Being redirected from orders admin - login required")
                redirect_url = orders_response.headers.get('Location', 'Unknown')
                print(f"Redirected to: {redirect_url}")
                return False
            else:
                print(f"ERROR: Cannot access order management (status {orders_response.status_code})")
                return False
        else:
            print(f"Login failed with status {login_response.status_code}")
            print("Response:", login_response.text[:200])
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        print("Make sure the server is running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_admin_access()
    sys.exit(0 if success else 1)