import requests

print("测试网络连接...")
try:
    response = requests.get("https://api.deepseek.com", timeout=10)
    print(f"连接成功！状态码: {response.status_code}")
except Exception as e:
    print(f"连接失败: {str(e)}")