#!/usr/bin/env python3
"""PaddleOCR Test Script

Tests PaddleOCR with a sample receipt image.
Run this from within the paddle_env virtual environment.

Author: Levy (Agent Faza)
Date: 2026-02-17
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_test_receipt():
    """Create a test receipt image."""
    print("Creating test receipt image...")
    
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
    
    print(f"✅ Test image created: {test_path}")
    return test_path

def test_paddleocr(image_path):
    """Test PaddleOCR functionality."""
    print(f"\nTesting PaddleOCR with: {image_path}")
    print("="*70)
    
    try:
        from paddleocr import PaddleOCR
        
        # Initialize PaddleOCR (CPU mode)
        print("Initializing PaddleOCR...")
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        print("✅ PaddleOCR initialized (use_angle_cls=True, lang='en', use_gpu=False)")
        
        # Read image
        print(f"Reading image: {image_path}...")
        result = ocr.ocr(image_path, cls=True)
        
        # Display results
        print("\n" + "="*70)
        print("OCR Results:")
        print("="*70)
        
        if result and len(result) > 0:
            print(f"Detected {len(result)} text regions:\n")
            
            for i, line in enumerate(result, 1):
                if line[1]:  # Check if line is not empty
                    text = line[1][0]  # First text in the line
                    confidence = line[1][1][1] if line[1][1] and len(line[1][1]) > 0 else 0
                    
                    bbox = line[0] if line[0] else None
                    
                    print(f"{i}. Text: \"{text}\" (Confidence: {confidence:.2f}, BBox: {bbox})")
                else:
                    print(f"{i}. Empty region")
            
            print("\n" + "="*70)
            print("✅ PaddleOCR Test Complete!")
            print("="*70)
        else:
            print("No text detected")
            
    except ImportError as e:
        print(f"❌ Failed to import PaddleOCR: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're running this from paddle_env virtual environment")
        print("   Command: source paddle_env/bin/activate")
        print("2. Check if PaddleOCR is installed:")
        print("   Command: paddleocr --help")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        sys.exit(1)

def main():
    """Run complete PaddleOCR test."""
    print("="*70)
    print("PaddleOCR Test Script")
    print("Author: Levy (Agent Faza)")
    print("Date: 2026-02-17")
    print("="*70)
    
    # Create test image
    test_image = create_test_receipt()
    
    # Test PaddleOCR
    test_paddleocr(test_image)

if __name__ == "__main__":
    main()
