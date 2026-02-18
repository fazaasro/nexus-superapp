#!/usr/bin/env python3
"""
Test PaddleOCR with Indonesian receipt.

Creates a test receipt in Indonesian format.
"""
import os
import sys

os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

sys.path.insert(0, '/home/ai-dev/.openclaw/workspace')

from modules.bag.ocr import OCRProcessor
from PIL import Image, ImageDraw, ImageFont

def create_indonesian_receipt():
    """Create an Indonesian-style receipt."""
    test_path = os.path.expanduser("~/receipt_indonesia.jpg")

    img = Image.new('RGB', (500, 700), color='white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()
        font_large = ImageFont.load_default()

    y = 40

    # Merchant header
    draw.text((30, y), "INDOMARET POINT", fill='red', font=font_large)
    y += 35
    draw.text((30, y), "Jakarta Selatan", fill='black', font=font)
    y += 50

    # Date (Indonesian format)
    draw.text((30, y), "18/02/2026 14:30", fill='black', font=font)
    y += 50

    # Items
    draw.text((30, y), "1. AQUA 600ML", fill='black', font=font)
    y += 30
    draw.text((380, y), "Rp 4.500", fill='black', font=font)
    y += 40

    draw.text((30, y), "2. ROTI TAWAR", fill='black', font=font)
    y += 30
    draw.text((380, y), "Rp 15.000", fill='black', font=font)
    y += 40

    draw.text((30, y), "3. TELUR AYAM", fill='black', font=font)
    y += 30
    draw.text((380, y), "Rp 32.000", fill='black', font=font)
    y += 40

    draw.text((30, y), "4. GULA PASIR", fill='black', font=font)
    y += 30
    draw.text((380, y), "Rp 18.000", fill='black', font=font)
    y += 50

    # Separator
    draw.line([(30, y), (470, y)], fill='gray', width=2)
    y += 50

    # Subtotal
    draw.text((30, y), "JUMLAH", fill='black', font=font)
    y += 30
    draw.text((380, y), "Rp 69.500", fill='black', font=font)
    y += 40

    # Tax (PPN)
    draw.text((30, y), "PPN 11%", fill='black', font=font)
    y += 30
    draw.text((380, y), "Rp 7.645", fill='black', font=font)
    y += 40

    # Total
    draw.text((30, y), "TOTAL", fill='black', font=font_large)
    y += 35
    draw.text((380, y), "Rp 77.145", fill='black', font=font_large)

    img.save(test_path, "JPEG", quality=95)
    print(f"✅ Indonesian receipt created: {test_path}")
    return test_path


def test_indonesian_ocr():
    """Test OCR with Indonesian language."""
    print("="*70)
    print("Indonesian Receipt OCR Test")
    print("="*70)

    # Create Indonesian receipt
    test_image = create_indonesian_receipt()

    # Test with English model (default)
    print("\n📝 Testing with English language model...")
    ocr_en = OCRProcessor(backend='paddleocr')
    result_en = ocr_en.extract_text(test_image)

    print("\n--- English Model Results ---")
    print(f"Success: {result_en.get('success')}")
    print(f"Text lines: {len(result_en.get('texts', []))}")
    print("\nExtracted text:")
    print(result_en.get('text', '')[:500])

    # Test with Indonesian language model
    print("\n\n📝 Testing with Indonesian language model...")
    ocr_id = OCRProcessor(backend='paddleocr', paddleocr_path='/home/ai-dev/.openclaw/workspace/paddle_env2/bin/paddleocr')
    ocr_id.paddleocr_processor.lang = 'id'
    result_id = ocr_id.extract_text(test_image)

    print("\n--- Indonesian Model Results ---")
    print(f"Success: {result_id.get('success')}")
    print(f"Text lines: {len(result_id.get('texts', []))}")
    print("\nExtracted text:")
    print(result_id.get('text', '')[:500])

    # Compare results
    print("\n\n" + "="*70)
    print("Comparison:")
    print("="*70)
    en_text = result_en.get('text', '')
    id_text = result_id.get('text', '')

    keywords = ['INDOMARET', 'AQUA', 'ROTI', 'TELUR', 'GULA', 'JUMLAH', 'TOTAL', 'Rp']

    print(f"\nEnglish model found {sum(1 for kw in keywords if kw in en_text)}/{len(keywords)} keywords")
    print(f"Indonesian model found {sum(1 for kw in keywords if kw in id_text)}/{len(keywords)} keywords")


if __name__ == "__main__":
    test_indonesian_ocr()
