import requests

def simple_test():
    """Simple test to check server response"""
    try:
        # Test main page
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        print(f"Main page: {response.status_code}")
        
        # Test login page
        response = requests.get('http://127.0.0.1:8000/accounts/login/', timeout=5)
        print(f"Login page: {response.status_code}")
        
        # Test orders admin page (should redirect)
        response = requests.get('http://127.0.0.1:8000/orders/admin/', timeout=5, allow_redirects=False)
        print(f"Orders admin (no redirect): {response.status_code}")
        if response.status_code == 302:
            print(f"Redirected to: {response.headers.get('Location', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    simple_test()