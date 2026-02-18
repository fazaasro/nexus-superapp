#!/usr/bin/env python3
"""PaddleOCR Test Script (Fixed for Permission Issues)

Tests PaddleOCR with a sample receipt image.
Saves test image to home directory (avoid /tmp/ permission issues).
Author: Levy (Agent Faza)
Date: 2026-02-18

FIX: Use ~/test_receipt.jpg instead of /tmp/test_receipt.jpg to avoid permission denied errors.
"""

import os
import sys
from datetime import datetime

def create_test_image():
    """Create a test receipt image."""
    print("Creating test receipt image...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Use home directory for test image (avoid /tmp/ permission issues)
        test_path = os.path.expanduser("~/test_receipt.jpg")
        
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
        draw.text((50, y), "SUPERMARKET", fill='black', font=font_large)
        y += 50
        
        # Date
        draw.text((50, y), datetime.now().strftime("%Y-%m-%d %H:%M"), fill='black', font=font)
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
        
        # Separator
        draw.line([(50, y), (550, y)], fill='gray', width=2)
        y += 60
        
        # Subtotal
        draw.text((50, y), "Subtotal", fill='black', font=font)
        y += 35
        draw.text((450, y), "$8.48", fill='black', font=font)
        y += 50
        
        # Tax
        draw.text((50, y), "Tax (10%)", fill='black', font=font)
        y += 35
        draw.text((450, y), "$0.85", fill='black', font=font)
        y += 50
        
        # Total
        draw.text((50, y), "TOTAL", fill='black', font=font_large)
        y += 40
        draw.text((450, y), "$9.33", fill='black', font=font_large)
        
        # Save to home directory (FIXED: Use ~ instead of /tmp/)
        img.save(test_path, "JPEG", quality=95)
        
        print(f"✅ Test receipt image created: {test_path}")
        print(f"📁 Location: {os.path.dirname(test_path)}")
        return test_path
        
    except ImportError:
        print("⚠️  PIL not available. Cannot create test image.")
        return None
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return None

def test_paddleocr_receipt(image_path):
    """Test PaddleOCR with receipt image."""
    print(f"\nTesting PaddleOCR with: {image_path}")
    print("="*70)
    
    try:
        from paddleocr import PaddleOCR
        
        # Initialize PaddleOCR (NO deprecated params)
        print("Initializing PaddleOCR...")
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        print("✅ PaddleOCR initialized")
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return False
        
        # Run OCR (no cls parameter)
        print(f"\nProcessing image: {image_path}...")
        result = ocr.ocr(image_path)
        
        # Display results
        print("\n" + "="*70)
        print("PaddleOCR Results:")
        print("="*70)
        
        if result and len(result) > 0:
            print(f"✅ Detected {len(result)} text regions:\n")
            
            for i, line in enumerate(result, 1):
                if line and len(line) > 0:
                    # PaddleOCR 2.7.0+ returns: [bbox, [text, confidence]]
                    bbox = line[0]
                    if line[1] and len(line[1]) > 0:
                        text_result = line[1][0]
                        confidence = line[1][1][1] if line[1][1] and len(line[1][1]) > 1 else 0
                        
                        print(f"{i}. Text: \"{text_result}\"")
                        print(f"   BBox: {bbox}")
                        print(f"   Confidence: {confidence:.2f}")
                    else:
                        print(f"{i}. Empty region with bbox: {bbox}")
                else:
                    print(f"{i}. Empty line")
            
            print("\n" + "="*70)
            print("✅ PaddleOCR Test Complete!")
            print("="*70)
            
            return True
        else:
            print("❌ No text detected in image")
            return False
            
    except ImportError:
        print("❌ Failed to import PaddleOCR")
        print("\nTroubleshooting:")
        print("1. Make sure paddle_env virtual environment is activated:")
        print("   source paddle_env/bin/activate")
        print("2. Check if PaddleOCR is installed:")
        print("   pip show paddleocr")
        print("3. Check if MKLDNN is disabled:")
        print("   echo $FLAGS_use_mkldnn")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        
        # Print help for specific errors
        if "ConvertPirAttribute" in str(e):
            print("\n💡 TIP: This is the MKLDNN bug. Ensure FLAGS_use_mkldnn=0 is set at script top.")
        elif "unexpected keyword" in str(e):
            print("\n💡 TIP: PaddleOCR parameter has changed. Try removing deprecated parameters.")
        
        sys.exit(1)

def main():
    """Run complete PaddleOCR test."""
    print("="*70)
    print("PaddleOCR Test Script (Fixed - Uses Home Directory)")
    print("="*70)
    print("FIX: Saved test image to ~/test_receipt.jpg instead of /tmp/")
    print("="*70)
    
    # Create test receipt
    test_image = create_test_image()
    
    if test_image:
        # Test PaddleOCR
        success = test_paddleocr_receipt(test_image)
        
        if success:
            print("\n" + "="*70)
            print("✅ PaddleOCR is working correctly!")
            print("="*70)
            print("\n🚀 Ready to integrate into Nexus Bag Module!")
            print("\nNext Steps:")
            print("1. Create PaddleOCR wrapper module")
            print("2. Integrate with GLM-4 for text interpretation")
            print("3. Update Nexus Bag service to use PaddleOCR")
        else:
            print("\n" + "="*70)
            print("❌ PaddleOCR test failed")
            print("="*70)
    else:
        print("\n" + "="*70)
        print("⚠️  Skipping OCR test (no test image)")
        print("="*70)

if __name__ == "__main__":
    main()
