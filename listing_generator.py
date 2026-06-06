import os
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
            raise ValueError("API key not set. Please set DEEPSEEK_API_KEY environment variable or call set_api_key()")
        
        prompt = f"""
You are a professional Temu/Amazon SEO listing expert. Generate a high-quality English listing based on the following information:

Product Name: {product_name}
Key Selling Points: {selling_points}
Target Market: {target_market}

Please output in the following JSON format:
{{
  "title": "Optimized product title (60-80 characters, SEO optimized with keywords)",
  "bullets": [
    "Bullet point 1: Key feature with benefit",
    "Bullet point 2: Key feature with benefit",
    "Bullet point 3: Key feature with benefit",
    "Bullet point 4: Key feature with benefit",
    "Bullet point 5: Key feature with benefit"
  ],
  "description": "Detailed product description (150-200 words) with all key selling points"
}}

Requirements:
1. Title: Include main keywords, follow Temu/Amazon SEO best practices
2. Bullet points: 5 points, each starting with capital letter, highlight key benefits
3. Description: Detailed narrative explaining product features and benefits
4. All output must be in English
5. Use attractive and persuasive language
6. Include relevant search keywords naturally
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
            "max_tokens": 1500,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.status_code} - {response.text}")
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        try:
            import json
            listing = json.loads(content)
            return listing
        except:
            return {
                'title': content[:100],
                'bullets': ["Error parsing response"],
                'description': content
            }


def main():
    generator = AIListingGenerator()
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        api_key = input("请输入你的DeepSeek API Key: ").strip()
        generator.set_api_key(api_key)
    
    print("\n=== Temu AI Listing Generator (English) ===")
    print("请输入商品信息，我将为您生成英文listing\n")
    
    product_name = input("Product Name: ").strip()
    selling_points = input("Key Selling Points (comma separated): ").strip()
    target_market = input("Target Market: ").strip()
    
    print("\nGenerating listing...")
    
    try:
        listing = generator.generate_listing(product_name, selling_points, target_market)
        
        print("\n=== Generated Result ===")
        print("\n【Title】")
        print(listing['title'])
        print("\n【Bullet Points】")
        for i, bullet in enumerate(listing['bullets'], 1):
            print(f"{i}. {bullet}")
        print("\n【Description】")
        print(listing['description'])
        
        with open("listing_result_en.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {listing['title']}\n\n")
            f.write("Bullet Points:\n")
            for i, bullet in enumerate(listing['bullets'], 1):
                f.write(f"{i}. {bullet}\n")
            f.write(f"\nDescription:\n{listing['description']}")
        print("\nResult saved to listing_result_en.txt")
        
        return listing
    except Exception as e:
        print(f"Generation failed: {str(e)}")
        return None


if __name__ == '__main__':
    main()