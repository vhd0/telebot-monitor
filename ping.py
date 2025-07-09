import requests
import sys
import time
from datetime import datetime
import random
import uuid

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
    ]
    return random.choice(user_agents)

def get_session_id():
    return str(uuid.uuid4())

def format_error_message(status_code, error_text="", attempt=0, max_attempts=5):
    error_messages = {
        503: "Service Unavailable (Render đang khởi động lại)",
        429: "Too Many Requests (Rate limit)",
        500: "Internal Server Error",
        502: "Bad Gateway",
        504: "Gateway Timeout"
    }
    base_message = error_messages.get(status_code, f"HTTP {status_code}")
    if attempt < max_attempts:
        return f"{base_message} (Thử lại {attempt+1}/{max_attempts})"
    return base_message

def ping_endpoint():
    base_url = "https://telegram-template-bot.onrender.com/health"
    MAX_ATTEMPTS = 5  # Tăng số lần thử cho Render spin up
    INITIAL_WAIT = 5  # Thời gian chờ ban đầu (giây)
    MAX_WAIT = 30    # Thời gian chờ tối đa (giây)
    
    params = {
        't': int(time.time()),
        '_': int(time.time() * 1000),
        'sid': get_session_id(),
        'v': '1.0',
        'r': random.randint(1000000, 9999999)
    }
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    
    try:
        with requests.Session() as session:
            start_time = time.time()
            wait_time = INITIAL_WAIT
            
            for attempt in range(MAX_ATTEMPTS):
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
                        if attempt > 0:
                            print(f"200 OK (Khởi động thành công sau {attempt+1} lần thử, phản hồi: {response_time}ms)")
                        else:
                            print(f"200 OK (Phản hồi: {response_time}ms)")
                        return True
                    
                    elif response.status_code == 503:
                        if attempt < MAX_ATTEMPTS - 1:
                            wait_time = min(wait_time * 1.5, MAX_WAIT)
                            print(f"{format_error_message(503, attempt=attempt, max_attempts=MAX_ATTEMPTS)}, đợi {round(wait_time)}s...")
                            time.sleep(wait_time)
                            continue
                        print(f"Service không khởi động được sau {MAX_ATTEMPTS} lần thử")
                        return False
                    
                    else:
                        error_msg = format_error_message(response.status_code, attempt=attempt, max_attempts=MAX_ATTEMPTS)
                        if attempt < MAX_ATTEMPTS - 1:
                            print(f"{error_msg}, đợi {round(wait_time)}s...")
                            time.sleep(wait_time)
                            continue
                        print(error_msg)
                        return False
                        
                except requests.exceptions.Timeout:
                    if attempt < MAX_ATTEMPTS - 1:
                        print(f"Timeout (Thử lại {attempt+1}/{MAX_ATTEMPTS}), đợi {round(wait_time)}s...")
                        time.sleep(wait_time)
                        continue
                    print(f"Timeout sau {MAX_ATTEMPTS} lần thử")
                    return False
                except requests.exceptions.ConnectionError as e:
                    if attempt < MAX_ATTEMPTS - 1:
                        print(f"Lỗi kết nối (Thử lại {attempt+1}/{MAX_ATTEMPTS}), đợi {round(wait_time)}s...")
                        time.sleep(wait_time)
                        continue
                    print(f"Không thể kết nối sau {MAX_ATTEMPTS} lần thử")
                    return False
                except Exception as e:
                    if attempt < MAX_ATTEMPTS - 1:
                        print(f"Lỗi không xác định (Thử lại {attempt+1}/{MAX_ATTEMPTS}), đợi {round(wait_time)}s...")
                        time.sleep(wait_time)
                        continue
                    print(f"Lỗi: {str(e)}")
                    return False
                
    except Exception as e:
        print(f"Lỗi không xác định: {str(e)}")
        return False

if __name__ == "__main__":
    success = ping_endpoint()
    sys.exit(0 if success else 1)
