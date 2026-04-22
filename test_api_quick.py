"""
快速测试API脚本
"""
import requests
import json

url = "http://localhost:8000/api/v1/generate"

payload = {
    "product_info": {
        "name": "白色衣架",
        "description": "简约设计的白色塑料衣架，适合家庭使用",
        "category": "家居用品",
        "key_features": ["简约设计", "耐用", "防滑"]
    },
    "mode": "text2img",
    "platform": "temu",
    "quality_threshold": 0.75,
    "max_retries": 2
}

print("发送请求到:", url)
print("请求内容:")
print(json.dumps(payload, indent=2, ensure_ascii=False))
print("\n" + "="*60 + "\n")

try:
    response = requests.post(url, json=payload, timeout=300)  # 5分钟超时
    print(f"状态码: {response.status_code}")
    print("\n响应内容:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except requests.exceptions.Timeout:
    print("❌ 请求超时！可能是LLM API响应太慢或卡住了")
except Exception as e:
    print(f"❌ 错误: {str(e)}")
