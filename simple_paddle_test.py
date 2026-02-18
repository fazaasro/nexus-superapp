#!/usr/bin/env python3
"""Simple PaddleOCR Test

Quick test to verify PaddleOCR works.
"""
from paddleocr import PaddleOCR

print("="*70)
print("PaddleOCR Quick Test")
print("="*70)

try:
    print("Initializing PaddleOCR...")
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    print("✅ PaddleOCR initialized!")
    
    # Test with sample image (no cls parameter - it's not supported)
    result = ocr.ocr('/home/ai-dev/test_receipt.jpg')
    
    if result:
        print(f"✅ SUCCESS! Found {len(result)} text regions")
        for i, line in enumerate(result[:3]):
            if line[1] and len(line[1]) > 0:
                text = line[1][0]
                print(f"{i}. {text}")
            else:
                print(f"{i}. Empty region")
    else:
        print("❌ No text detected")
    
except ImportError as e:
    print(f"❌ Failed to import PaddleOCR: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
