import requests
import sys
import time
from datetime import datetime

def ping_endpoint():
    base_url = "https://telegram-template-bot.onrender.com/health"
    # Thêm timestamp để tránh cache
    url = f"{base_url}?t={int(time.time())}"
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=60)
        response_time = round((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            print(f"200 OK (Phản hồi: {response_time}ms)")
            return True
        else:
            print(f"Lỗi {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("Timeout sau 60s")
        return False
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return False

if __name__ == "__main__":
    success = ping_endpoint()
    sys.exit(0 if success else 1)
