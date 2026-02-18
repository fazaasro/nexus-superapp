#!/usr/bin/env python3
"""Simple PaddleOCR Test Script

Tests PaddleOCR with proper environment setup to avoid MKLDNN bug.
"""
import os
import sys

# IMPORTANT: Must be set BEFORE importing paddleocr
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

def main():
    """Run PaddleOCR test."""
    print("="*70)
    print("PaddleOCR Simple Test")
    print("="*70)

    try:
        from paddleocr import PaddleOCR
        print("✅ PaddleOCR imported successfully!")
    except ImportError as e:
        print(f"❌ Failed to import PaddleOCR: {e}")
        sys.exit(1)

    # Initialize PaddleOCR (use new API without deprecated params)
    print("\nInitializing PaddleOCR...")
    print("Using parameters: use_textline_orientation=True, lang='en'")

    try:
        ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        print("✅ PaddleOCR initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize PaddleOCR: {e}")
        sys.exit(1)

    # Test image path
    test_image = os.path.expanduser("~/test_receipt.jpg")

    if not os.path.exists(test_image):
        print(f"\n❌ Test image not found: {test_image}")
        print("Creating a simple test image...")

        try:
            from PIL import Image, ImageDraw, ImageFont

            img = Image.new('RGB', (400, 300), color='white')
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font = ImageFont.load_default()

            # Draw some text
            draw.text((20, 50), "TEST RECEIPT", fill='black', font=font)
            draw.text((20, 100), "MILK - $2.99", fill='black', font=font)
            draw.text((20, 140), "BREAD - $1.50", fill='black', font=font)
            draw.text((20, 180), "TOTAL - $4.49", fill='black', font=font)

            img.save(test_image, "JPEG")
            print(f"✅ Test image created: {test_image}")
        except Exception as e:
            print(f"❌ Failed to create test image: {e}")
            sys.exit(1)

    # Run OCR using predict method (new API)
    print(f"\nProcessing image: {test_image}...")
    print("Using predict() method (new API)...")

    try:
        result = ocr.predict(test_image)

        print("\n" + "="*70)
        print("OCR Results:")
        print("="*70)

        if result and len(result) > 0:
            print(f"✅ Detection successful!")
            print(f"Result type: {type(result)}")
            print(f"Result length: {len(result)}")

            # Extract text from result
            all_text = []
            for item in result:
                if hasattr(item, 'rec_texts'):
                    all_text.extend(item.rec_texts)
                    print(f"Texts: {item.rec_texts}")
                elif isinstance(item, dict) and 'rec_texts' in item:
                    all_text.extend(item['rec_texts'])
                    print(f"Texts: {item['rec_texts']}")

            print("\n" + "="*70)
            print("✅ PaddleOCR Test Complete!")
            print("="*70)
            print(f"All extracted text: {all_text}")
        else:
            print("❌ No results returned")
    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
