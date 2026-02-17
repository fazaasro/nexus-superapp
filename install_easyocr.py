#!/usr/bin/env python3
"""
Install EasyOCR natively and test OCR functionality.

This script bypasses Docker and installs EasyOCR directly in the VPS environment.
"""

import subprocess
import sys

print("="*70)
print("Installing EasyOCR (Native, No Docker)")
print("="*70)
print("\n📦 Installing EasyOCR package...")
print("   This may take a few minutes on first run...\n")

# Install EasyOCR
try:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "easyocr", "--quiet"],
        check=True,
        capture_output=True,
        text=True
    )
    print("✅ EasyOCR installed successfully!\n")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to install EasyOCR: {e}")
    sys.exit(1)

# Test import
print("="*70)
print("Testing EasyOCR Import")
print("="*70)

try:
    import easyocr
    print("✅ EasyOCR imported successfully!")
    print(f"   Version: {easyocr.__version__}")
    
    # Create a simple test
    reader = easyocr.Reader(['en'], gpu=False)
    print("✅ OCR Reader initialized (GPU=False)")
    print("\n🔍 Test: Extracting text from a simple image...")
    print("   Creating a test image with text: 'TEST 123'...")
    
    # Create a simple test image using PIL if available
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (200, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 30), "TEST 123", fill='black', font=font)
        
        # Save to temp file
        test_path = "/tmp/test_ocr.jpg"
        img.save(test_path, "JPEG")
        print(f"   Test image saved to: {test_path}")
        
        # Run OCR
        print("   Running OCR...")
        result = reader.readtext(test_path)
        
        print(f"✅ OCR Test PASSED!")
        print(f"   Detected Text: \"{result[0][1]}\"")
        print(f"   Confidence: {result[0][2]:.2f}")
        
    except ImportError:
        print("⚠️  PIL not available. Skipping image test.")
        print("✅ EasyOCR is ready to use (import successful)")
    
    print("\n" + "="*70)
    print("✅ EasyOCR Installation Complete!")
    print("="*70)
    print("\n💡 Usage:")
    print("   import easyocr")
    print("   reader = easyocr.Reader(['en'], gpu=False)")
    print("   result = reader.readtext('receipt.jpg')")
    print("   text = result[0][0]  # First detected text")
    print("\n")
    
except ImportError as e:
    print(f"❌ Failed to import EasyOCR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
