import os
import sys
from listing_generator import AIListingGenerator


def test_deepseek():
    print("Step 1: 创建生成器实例...")
    generator = AIListingGenerator()
    
    print("Step 2: 设置API Key...")
    generator.set_api_key("sk-b0b98722667f49d887a42c920d8f997c")
    
    print("\n=== Temu AI Listing 生成器 (DeepSeek) ===")
    print("测试数据：")
    print("商品名称：无线蓝牙耳机")
    print("核心卖点：降噪、续航30小时、防水")
    print("目标市场：美国\n")
    
    print("Step 3: 开始调用API...")
    sys.stdout.flush()
    
    try:
        listing = generator.generate_listing(
            product_name="无线蓝牙耳机",
            selling_points="降噪、续航30小时、防水",
            target_market="美国"
        )
        
        print("Step 4: API调用成功！")
        print("\n=== 生成结果 ===")
        print("\n【商品标题】")
        print(listing['title'])
        print("\n【商品描述】")
        print(listing['description'])
        
        return listing
    except Exception as e:
        print(f"\n生成失败: {str(e)}")
        return None


if __name__ == '__main__':
    test_deepseek()