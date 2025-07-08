import requests
import sys
import time
from datetime import datetime
import random
import uuid

def get_random_user_agent():
    # List các User-Agent phổ biến
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
    ]
    return random.choice(user_agents)

def get_random_referrer():
    # Các Referrer phổ biến
    referrers = [
        'https://www.google.com/',
        'https://github.com/',
        'https://render.com/docs',
        None  # Một số request không có referrer
    ]
    return random.choice(referrers)

def get_session_id():
    # Tạo session ID giống browser thật
    return str(uuid.uuid4())

def ping_endpoint():
    base_url = "https://telegram-template-bot.onrender.com/health"
    
    # Thêm các tham số để giống request thật
    params = {
        't': int(time.time()),  # Timestamp
        '_': int(time.time() * 1000),  # Milliseconds timestamp (thường thấy trong AJAX requests)
        'sid': get_session_id(),  # Session ID
        'v': '1.0',  # Version
        'r': random.randint(1000000, 9999999)  # Random number
    }
    
    # Headers giống browser thật
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }
    
    # Thêm Referrer header nếu có
    referrer = get_random_referrer()
    if referrer:
        headers['Referer'] = referrer
    
    try:
        # Thêm delay ngẫu nhiên từ 0.5 đến 2 giây để giống hành vi người dùng
        time.sleep(random.uniform(0.5, 2))
        
        # Tạo session để giữ cookies và có thể tái sử dụng connection
        with requests.Session() as session:
            start_time = time.time()
            
            # Thực hiện request với retry logic
            for attempt in range(3):  # Tối đa 3 lần thử
                try:
                    response = session.get(
                        base_url,
                        params=params,
                        headers=headers,
                        timeout=30,
                        allow_redirects=True,
                        verify=True
                    )
                    response_time = round((time.time() - start_time) * 1000)
                    
                    if response.status_code == 200:
                        print(f"200 OK (Phản hồi: {response_time}ms)")
                        return True
                    elif response.status_code == 429:  # Too Many Requests
                        if attempt < 2:  # Nếu chưa phải lần thử cuối
                            time.sleep(random.uniform(2, 5))  # Đợi thêm 2-5 giây
                            continue
                        print(f"Lỗi 429: Too Many Requests")
                        return False
                    else:
                        print(f"Lỗi {response.status_code}")
                        return False
                        
                except requests.exceptions.Timeout:
                    if attempt < 2:
                        continue
                    print("Timeout sau 30s")
                    return False
                except Exception as e:
                    if attempt < 2:
                        continue
                    print(f"Lỗi: {str(e)}")
                    return False
                
    except Exception as e:
        print(f"Lỗi không xác định: {str(e)}")
        return False

if __name__ == "__main__":
    success = ping_endpoint()
    sys.exit(0 if success else 1)
