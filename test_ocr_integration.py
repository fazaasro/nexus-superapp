# /test_ocr_integration.py
"""
Test script for OCR receipt ingestion and transaction classification.
Run with: python test_ocr_integration.py
"""
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.bag.service import BagModule, classify_transaction


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("NEXUS BAG MODULE - OCR & CLASSIFICATION TESTS")
    print("="*60)
    
    # Test 1: Transaction Classification
    print("\n🔍 Running transaction classification tests...")
    await test_transaction_classification_async()
    
    # Test 2: OCR Ingestion (requires real receipt image)
    await test_ocr_ingestion()


async def test_ocr_ingestion():
    """Test OCR receipt ingestion."""
    print("\n" + "="*60)
    print("TEST 1: OCR Receipt Ingestion")
    print("="*60)
    
    # Initialize BagModule
    bag = BagModule()
    
    # Update this path to your actual receipt image
    receipt_path = "/tmp/test_receipt.jpg"
    
    # Check if test image exists
    if not Path(receipt_path).exists():
        print(f"❌ Test image not found: {receipt_path}")
        print("   Skipping OCR test (requires real receipt image)")
        print("   To test, place a receipt image at specified path")
        return None
    
    # Test with env var API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        return None
    
    try:
        result = await bag.ingest_receipt(receipt_path, user_id='faza')
        
        if result["success"]:
            print("✅ OCR ingestion successful")
            print(f"   Merchant: {result['transaction_data'].get('merchant', 'N/A')}")
            print(f"   Date: {result['transaction_data'].get('date', 'N/A')}")
            print(f"   Total: ${result['transaction_data'].get('total', 'N/A')}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"\n   Raw text preview:")
            print(f"   {result['raw_text'][:200]}...")
            return result
        else:
            print(f"❌ OCR ingestion failed: {result['error']}")
            return None
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


async def test_transaction_classification_async():
    """Test transaction classification with sample data."""
    print("\n" + "="*60)
    print("TEST 2: Transaction Classification")
    print("="*60)
    
    test_cases = [
        {
            "name": "Grocery store",
            "data": {
                "merchant": "Whole Foods Market",
                "date": "2025-02-15",
                "items": [
                    {"name": "Organic Milk", "quantity": 1, "price": 5.99},
                    {"name": "Sourdough Bread", "quantity": 1, "price": 4.50}
                ],
                "total": 45.67
            }
        },
        {
            "name": "Restaurant",
            "data": {
                "merchant": "Chipotle Mexican Grill",
                "date": "2025-02-15",
                "items": [
                    {"name": "Burrito Bowl", "quantity": 1, "price": 9.85}
                ],
                "total": 12.45
            }
        },
        {
            "name": "Gas station",
            "data": {
                "merchant": "Shell Gas Station",
                "date": "2025-02-15",
                "items": [],
                "total": 52.30
            }
        },
        {
            "name": "Streaming service",
            "data": {
                "merchant": "Netflix",
                "date": "2025-02-15",
                "items": [],
                "total": 15.99
            }
        },
        {
            "name": "Unknown merchant",
            "data": {
                "merchant": "Unknown Store",
                "date": "2025-02-15",
                "items": [],
                "total": 25.00
            }
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print(f"   Merchant: {test_case['data']['merchant']}")
        print(f"   Total: ${test_case['data']['total']}")
        
        classification = classify_transaction(test_case['data'])
        
        print(f"   → Category: {classification['category']}")
        print(f"   → Subcategory: {classification['subcategory']}")
        print(f"   → Discretionary: {classification['is_discretionary']}")
        print(f"   → Recurrence: {classification['recurrence_type']}")
        print(f"   → Confidence: {classification['confidence']}")
        
        results.append({
            "name": test_case['name'],
            "classification": classification
        })
    
    # Validate results
    print("\n" + "-"*60)
    print("VALIDATION:")
    
    expected_results = {
        "Grocery store": {"category": "Food", "subcategory": "Groceries"},
        "Restaurant": {"category": "Food", "subcategory": "Restaurant"},
        "Gas station": {"category": "Transportation", "subcategory": "Fuel"},
        "Streaming service": {"category": "Entertainment", "subcategory": "Streaming"},
    }
    
    passed = 0
    for result in results:
        name = result['name']
        if name in expected_results:
            expected = expected_results[name]
            actual = result['classification']
            if actual['category'] == expected['category'] and actual['subcategory'] == expected['subcategory']:
                print(f"   ✅ {name}: Passed")
                passed += 1
            else:
                print(f"   ❌ {name}: Failed (expected {expected}, got {actual['category']}/{actual['subcategory']})")
    
    print(f"\n   Score: {passed}/{len(expected_results)} tests passed")
    return results


if __name__ == "__main__":
    asyncio.run(main())
