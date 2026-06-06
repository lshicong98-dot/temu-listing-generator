import os
import sys
import time
import requests
from typing import Dict


class AIListingGenerator:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1"
    
    def set_api_key(self, api_key: str):
        self.api_key = api_key
    
    def generate_listing(self, product_name: str, selling_points: str, target_market: str) -> Dict:
        if not self.api_key:
            raise ValueError("API key not set")
        
        prompt = f"""
你是一个专业的Temu电商listing优化专家。请根据以下信息生成高质量的商品标题和描述：

商品名称：{product_name}
核心卖点：{selling_points}
目标市场：{target_market}

请按照以下格式输出：

【商品标题】
生成一个优化的Temu商品标题，包含主要关键词

【商品描述】
生成一个详细的商品描述
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7
        }
        
        print(f"[{time.time()}] 准备发送请求...")
        print(f"[{time.time()}] URL: {self.base_url}/chat/completions")
        
        try:
            print(f"[{time.time()}] 正在发送POST请求...")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            print(f"[{time.time()}] 请求完成，状态码: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[{time.time()}] 错误响应: {response.text[:500]}")
                raise ValueError(f"API请求失败: {response.status_code}")
            
            print(f"[{time.time()}] 解析响应...")
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"[{time.time()}] 响应内容长度: {len(content)}")
            
            title_start = content.find("【商品标题】")
            desc_start = content.find("【商品描述】")
            
            title = content[title_start+6:desc_start].strip() if title_start != -1 and desc_start != -1 else ""
            description = content[desc_start+6:].strip() if desc_start != -1 else ""
            
            return {
                'title': title if title else content[:50],
                'description': description if description else content
            }
            
        except requests.exceptions.Timeout:
            print(f"[{time.time()}] 超时错误")
            raise ValueError("请求超时")
        except requests.exceptions.ConnectionError:
            print(f"[{time.time()}] 连接错误")
            raise ValueError("连接失败")
        except Exception as e:
            print(f"[{time.time()}] 未知错误: {str(e)}")
            raise


def test_deepseek():
    print("Step 1: 创建生成器实例...")
    generator = AIListingGenerator()
    
    print("Step 2: 设置API Key...")
    generator.set_api_key("sk-b0b98722667f49d887a42c920d8f997c")
    
    print("\n=== Temu AI Listing 生成器 (DeepSeek) ===")
    
    print("\nStep 3: 开始调用API...")
    sys.stdout.flush()
    
    try:
        listing = generator.generate_listing(
            product_name="无线蓝牙耳机",
            selling_points="降噪、续航30小时、防水",
            target_market="美国"
        )
        
        print("\n=== 生成结果 ===")
        print("\n【商品标题】")
        print(listing['title'])
        print("\n【商品描述】")
        print(listing['description'][:500] if len(listing['description']) > 500 else listing['description'])
        
        return listing
    except Exception as e:
        print(f"\n生成失败: {str(e)}")
        return None


if __name__ == '__main__':
    test_deepseek()