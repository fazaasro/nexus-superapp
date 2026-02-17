#!/usr/bin/env python3
"""Test PaddleOCR with a sample image.

This script creates a test receipt image and runs OCR on it.
"""

from PIL import Image, ImageDraw, ImageFont
import base64
from datetime import datetime

def create_test_image():
    """Create a test receipt image."""
    print("Creating test receipt image...")
    
    try:
        img = Image.new('RGB', (600, 800), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        y = 50
        
        # Merchant
        draw.text((50, y), "SUPERMARKET", fill='black', font=font)
        y += 40
        
        # Date
        draw.text((50, y), datetime.now().strftime("%Y-%m-%d %H:%M"), fill='black', font=font)
        y += 40
        
        # Items
        draw.text((50, y), "1. MILK 1L", fill='black', font=font)
        y += 30
        draw.text((450, y), "$2.99", fill='black', font=font)
        y += 40
        
        draw.text((50, y), "2. BREAD", fill='black', font=font)
        y += 30
        draw.text((450, y), "$1.50", fill='black', font=font)
        y += 40
        
        # Separator
        draw.line([(50, y), (550, y)], fill='gray', width=2)
        y += 50
        
        # Total
        draw.text((50, y), "TOTAL", fill='black', font=font)
        y += 30
        draw.text((450, y), "$4.49", fill='black', font=font)
        
        test_path = "/tmp/test_receipt.jpg"
        img.save(test_path, "JPEG", quality=95)
        
        print(f"Test image created: {test_path}")
        return test_path
        
    except ImportError:
        print("PIL not available. Skipping image generation.")
        return None
    except Exception as e:
        print(f"Failed to create test image: {e}")
        return None

def test_ocr(image_path):
    """Test OCR with PaddleOCR."""
    print("Testing OCR with PaddleOCR...")
    
    try:
        from paddleocr import PaddleOCR
        
        # Initialize PaddleOCR (CPU)
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        print("PaddleOCR initialized (use_angle_cls=True, lang='en', use_gpu=False)")
        
        # Read image
        import os
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return
        
        # Run OCR
        result = ocr.ocr(image_path, cls=True)
        
        # Display results
        print("\n" + "="*70)
        print("OCR Results:")
        print("="*70)
        
        if result:
            print(f"Detected {len(result)} regions")
            
            for i, line in enumerate(result):
                if len(line) > 0:
                    text = line[0][1] if len(line[0]) > 1 else ""
                    confidence = line[0][2] if len(line[0]) > 2 else 0
                    print(f"{i+1}. Text: \"{text}\" (Confidence: {confidence:.2f})")
                else:
                    print(f"{i+1}. Empty region")
            
            print("\n" + "="*70)
            print("✅ PaddleOCR Test Complete!")
            print("="*70)
        else:
            print("No text detected")
            
    except ImportError:
        print("Error: PaddleOCR not installed")
        print("Please install with: pip install paddleocr")
    except Exception as e:
        print(f"Error during OCR: {e}")

if __name__ == "__main__":
    print("="*70)
    print("PaddleOCR Test Script")
    print("="*70)
    
    # Create test image
    test_image = create_test_image()
    
    if test_image:
        # Test OCR
        test_ocr(test_image)
    else:
        print("Skipping OCR test (no test image)")
