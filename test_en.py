from listing_generator import AIListingGenerator


def test_deepseek():
    generator = AIListingGenerator()
    generator.set_api_key("sk-b0b98722667f49d887a42c920d8f997c")
    
    print("\n=== Temu AI Listing Generator (English) ===")
    print("测试数据：")
    print("Product Name: Wireless Bluetooth Earbuds")
    print("Key Selling Points: Noise Cancelling, 30H Battery, Waterproof")
    print("Target Market: USA\n")
    
    print("Generating listing...")
    
    try:
        listing = generator.generate_listing(
            product_name="Wireless Bluetooth Earbuds",
            selling_points="Noise Cancelling, 30H Battery, Waterproof",
            target_market="USA"
        )
        
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
    test_deepseek()