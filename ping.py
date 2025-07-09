import requests
import sys
import time
import random

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
    ]
    return random.choice(user_agents)

def ping_endpoint():
    base_url = "https://telegram-template-bot.onrender.com/health"
    MAX_ATTEMPTS = 5
    INITIAL_WAIT = 5
    MAX_WAIT = 30
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': '*/*',
        'Cache-Control': 'no-cache'
    }
    
    try:
        with requests.Session() as session:
            start_time = time.time()
            wait_time = INITIAL_WAIT
            retry_log = []
            
            for attempt in range(MAX_ATTEMPTS):
                try:
                    response = session.get(
                        base_url,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        response_time = round((time.time() - start_time) * 1000)
                        # Nếu là lần đầu thành công
                        if attempt == 0:
                            print(f"200 OK (Phản hồi: {response_time}ms)")
                        else:
                            # In log retry nếu có
                            for log in retry_log:
                                print(log)
                            print(f"200 OK (Khởi động thành công sau {attempt+1} lần thử, phản hồi: {response_time}ms)")
                        return True
                    
                    elif response.status_code == 503:
                        if attempt < MAX_ATTEMPTS - 1:
                            retry_msg = f"Service Unavailable (Render đang khởi động lại) (Thử lại {attempt+1}/{MAX_ATTEMPTS}), đợi {round(wait_time)}s..."
                            retry_log.append(retry_msg)
                            time.sleep(wait_time)
                            wait_time = min(wait_time * 1.5, MAX_WAIT)
                            continue
                        print("Service không khởi động được sau 5 lần thử")
                        return False
                    
                    else:
                        print(f"HTTP {response.status_code}")
                        return False
                        
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    if attempt < MAX_ATTEMPTS - 1:
                        retry_msg = f"Timeout/Connection Error (Thử lại {attempt+1}/{MAX_ATTEMPTS}), đợi {round(wait_time)}s..."
                        retry_log.append(retry_msg)
                        time.sleep(wait_time)
                        wait_time = min(wait_time * 1.5, MAX_WAIT)
                        continue
                    print("Không thể kết nối sau 5 lần thử")
                    return False
                
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return False

if __name__ == "__main__":
    success = ping_endpoint()
    sys.exit(0 if success else 1)
