import time
import requests
import json
from datetime import datetime
import sys

URL = "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc5NjczNTAxIiwibmJmIjoiMTc3OTY3MzUwMSIsImV4cCI6IjE3Nzk2NzUzMDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzI1LzIwMjYgODo0NTowMSBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZЕНИRmdpY2Uvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjQ4NzIwMyIsIlVzZXJOYW1lIjoiOTU5Nzc3NTQ1NTg5IiwiVXNlclBob3RvIjoiMjAiLCJOaWNrTmFtZSI6Ik1HVEhBTlQgIiwiQW1vdW50IjoiMi42MSIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiNS8yNS8yMDI2IDg6MTU6MDEgQU0iLCJMb2dpbklQQWRkcmVzcyI6IjExNi4y00Ni4xOTMuNDAiLCJEYk51bWJlciI6IjAiLCJJc3ZhbGlkYXRvciI6IjAiLCiS2V5Q29kZSI6IjYwNSIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjEiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.x3qj70HmHJKnSsYTI08LqurJ-KB4W7e0syYMwPWfbvE",
    "Ar-Origin": "https://www.cklottery.top",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

PAYLOAD = {
    "pageSize": 10,
    "pageNo": 1,
    "typeId": 30,
    "language": 0,
    "random": "be8d0ae92c154507a735d86a2d792cd3",
    "signature": "DBDC04A4BEB3AAAB575F34FD0B4C6872",
    "timestamp": 1779674033
}

def fetch_bot_data():
    print(f"\n[+] Fetching Data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...", flush=True)
    try:
        response = requests.post(URL, json=PAYLOAD, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0 and "data" in result:
                game_list = result["data"].get("list", [])
                print(f"Server Time: {result.get('serviceNowTime')}", flush=True)
                print("-" * 50, flush=True)
                
                for item in game_list:
                    issue = item.get("issueNumber")
                    num = item.get("number")
                    colour = item.get("colour")
                    print(f"Issue: {issue} | Number: {num} | Colour: {colour}", flush=True)
            else:
                print(f"[-] API Error Message: {result.get('msg')}", flush=True)
        else:
            print(f"[-] HTTP Error: Status Code {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"[-] Error occurred: {e}", flush=True)

if __name__ == "__main__":
    print("[*] Starting 30S API Bot on Railway...", flush=True)
    while True:
        fetch_bot_data()
        time.sleep(30)
