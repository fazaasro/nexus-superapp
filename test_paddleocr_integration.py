#!/usr/bin/env python3
"""
Test PaddleOCR integration with Nexus Bag Module.

This script tests the OCRProcessor with PaddleOCR backend.
"""
import os
import sys
import asyncio

# IMPORTANT: Set these BEFORE importing anything from the bag module
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

# Add workspace to path
sys.path.insert(0, '/home/ai-dev/.openclaw/workspace')

from modules.bag.ocr import OCRProcessor


def create_test_receipt():
    """Create a test receipt image."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        test_path = os.path.expanduser("~/test_nexus_receipt.jpg")

        img = Image.new('RGB', (600, 800), color='white')
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        except:
            font = ImageFont.load_default()
            font_large = ImageFont.load_default()

        y = 50

        # Merchant
        draw.text((50, y), "SUPERMARKET XYZ", fill='black', font=font_large)
        y += 50

        # Date
        draw.text((50, y), "2026-02-18 10:30", fill='black', font=font)
        y += 50

        # Items
        draw.text((50, y), "1. MILK 1L", fill='black', font=font)
        y += 35
        draw.text((450, y), "$2.99", fill='black', font=font)
        y += 50

        draw.text((50, y), "2. BREAD", fill='black', font=font)
        y += 35
        draw.text((450, y), "$1.50", fill='black', font=font)
        y += 50

        draw.text((50, y), "3. EGGS (12)", fill='black', font=font)
        y += 35
        draw.text((450, y), "$3.99", fill='black', font=font)
        y += 50

        draw.text((50, y), "4. COFFEE", fill='black', font=font)
        y += 35
        draw.text((450, y), "$5.99", fill='black', font=font)
        y += 50

        # Separator
        draw.line([(50, y), (550, y)], fill='gray', width=2)
        y += 60

        # Subtotal
        draw.text((50, y), "Subtotal", fill='black', font=font)
        y += 35
        draw.text((450, y), "$14.47", fill='black', font=font)
        y += 50

        # Tax
        draw.text((50, y), "Tax (10%)", fill='black', font=font)
        y += 35
        draw.text((450, y), "$1.45", fill='black', font=font)
        y += 50

        # Total
        draw.text((50, y), "TOTAL", fill='black', font=font_large)
        y += 40
        draw.text((450, y), "$15.92", fill='black', font=font_large)

        img.save(test_path, "JPEG", quality=95)

        print(f"✅ Test receipt created: {test_path}")
        return test_path

    except ImportError:
        print("❌ PIL not available")
        return None
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return None


def test_paddleocr():
    """Test PaddleOCR processor."""
    print("="*70)
    print("PaddleOCR Integration Test")
    print("="*70)

    # Create test receipt
    test_image = create_test_receipt()
    if not test_image:
        print("❌ Cannot create test image - aborting test")
        return False

    # Initialize OCR processor with PaddleOCR backend
    print("\nInitializing OCRProcessor with PaddleOCR backend...")
    try:
        ocr = OCRProcessor(backend='paddleocr')
    except Exception as e:
        print(f"❌ Failed to initialize OCRProcessor: {e}")
        return False

    # Extract text
    print(f"\nExtracting text from: {test_image}")
    result = ocr.extract_text(test_image)

    print("\n" + "="*70)
    print("Results:")
    print("="*70)

    if result.get("success"):
        print(f"✅ OCR Success!")
        print(f"\nBackend: {result.get('backend')}")
        print(f"Text lines extracted: {len(result.get('texts', []))}")
        print(f"\nExtracted text:")
        print("-" * 70)
        print(result.get("text"))
        print("-" * 70)

        # Check if expected text was extracted
        expected_keywords = ["SUPERMARKET", "MILK", "BREAD", "EGGS", "COFFEE", "TOTAL"]
        text = result.get("text", "")
        found = [kw for kw in expected_keywords if kw in text]

        print(f"\nExpected keywords found: {len(found)}/{len(expected_keywords)}")
        print(f"Found: {found}")

        if len(found) >= 4:
            print("\n✅ PaddleOCR integration working correctly!")
            return True
        else:
            print("\n⚠️  Some expected text missing")
            return False
    else:
        print(f"❌ OCR Failed!")
        print(f"Error: {result.get('error')}")
        return False


async def test_bag_module_integration():
    """Test BagModule with PaddleOCR."""
    print("\n" + "="*70)
    print("BagModule Integration Test")
    print("="*70)

    try:
        from modules.bag.service import BagModule

        # Create test receipt
        test_image = create_test_receipt()
        if not test_image:
            print("❌ Cannot create test image")
            return False

        # Initialize BagModule
        print("\nInitializing BagModule...")
        bag = BagModule()

        # Ingest receipt
        print(f"\nIngesting receipt: {test_image}")
        result = await bag.ingest_receipt(test_image, user_id='faza')

        print("\n" + "="*70)
        print("BagModule Results:")
        print("="*70)

        if result.get("success"):
            print("✅ Receipt ingestion successful!")
            print(f"\nTransaction data:")
            print(f"  Merchant: {result.get('transaction_data', {}).get('merchant')}")
            print(f"  Date: {result.get('transaction_data', {}).get('date')}")
            print(f"  Total: {result.get('transaction_data', {}).get('total')}")
            print(f"  Items: {len(result.get('transaction_data', {}).get('items', []))}")
            print(f"  Confidence: {result.get('confidence', 0):.2f}")
            return True
        else:
            print(f"❌ Receipt ingestion failed!")
            print(f"Error: {result.get('error')}")
            return False

    except Exception as e:
        print(f"❌ BagModule test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "PaddleOCR Integration Test" + " "*22 + "║")
    print("╚" + "="*68 + "╝")

    # Test 1: PaddleOCR processor
    success1 = test_paddleocr()

    # Test 2: BagModule integration
    success2 = asyncio.run(test_bag_module_integration())

    # Summary
    print("\n" + "="*70)
    print("Test Summary:")
    print("="*70)
    print(f"PaddleOCR Processor: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"BagModule Integration: {'✅ PASS' if success2 else '❌ FAIL'}")

    if success1 and success2:
        print("\n✅ All tests passed! PaddleOCR integration is working.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
