#!/usr/bin/env python3
"""
EasyOCR Flow Test Script

Tests the complete OCR pipeline:
1. Service health check
2. Test image generation
3. OCR processing
4. Result display

Author: Levy (Agent Faza)
Date: 2026-02-17
"""

import base64
import requests
import json
from typing import Dict, Any, Optional
from pathlib import Path
from io import BytesIO
from datetime import datetime

# Try to import PIL for image generation
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL not installed. Image generation will be skipped.")


class EasyOCRTester:
    """Test harness for EasyOCR service."""
    
    def __init__(self, service_url: str = "http://127.0.0.1:5000"):
        self.service_url = service_url.rstrip('/')
        self.timeout = 30
    
    def check_service(self) -> bool:
        """Check if EasyOCR service is running and accessible."""
        print("\n" + "="*70)
        print("🔍 EasyOCR Service Health Check")
        print("="*70)
        
        try:
            # Try root endpoint
            response = requests.get(f"{self.service_url}/", timeout=5)
            print(f"✅ Service is accessible!")
            print(f"   Status Code: {response.status_code}")
            return True
            
        except requests.exceptions.Timeout:
            print(f"❌ Service check timed out (>{5}s)")
            print(f"   Service might still be starting...")
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to service at {self.service_url}")
            print(f"   Service is not running or port is incorrect")
            return False
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def generate_test_receipt(self) -> Optional[str]:
        """Generate a test receipt image with OCR-friendly text."""
        if not PIL_AVAILABLE:
            print("⚠️  Skipping image generation (PIL not available)")
            return None
        
        print("\n" + "="*70)
        print("🖼️  Generating Test Receipt Image")
        print("="*70)
        
        try:
            # Create image (white background, black text)
            img = Image.new('RGB', (600, 800), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a simple font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            # Receipt content
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
            
            # Save to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG', quality=95)
            img_bytes.seek(0)
            
            # Convert to base64
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            
            print(f"✅ Test receipt image generated (600x800)")
            print(f"   Size: {len(img_base64)} characters (base64)")
            
            return img_base64
            
        except Exception as e:
            print(f"❌ Failed to generate test image: {e}")
            return None
    
    def test_ocr(self, image_base64: str) -> Dict[str, Any]:
        """Test OCR processing with image."""
        print("\n" + "="*70)
        print("🔍 Testing OCR Processing")
        print("="*70)
        
        payload = {
            "image": f"data:image/jpeg;base64,{image_base64}"
        }
        
        try:
            print(f"📤 Sending image to {self.service_url}/predict...")
            
            start_time = datetime.now()
            response = requests.post(
                f"{self.service_url}/predict",
                json=payload,
                timeout=self.timeout
            )
            elapsed = (datetime.now() - start_time).total_seconds()
            
            # Check response
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ OCR request completed successfully!")
            print(f"   Time: {elapsed:.2f} seconds")
            print(f"   Status Code: {response.status_code}")
            
            # Display results
            if isinstance(result, dict):
                text = result.get("text", "")
                print(f"\n📄 Extracted Text:")
                print("-" * 70)
                print(text[:500])  # First 500 chars
                if len(text) > 500:
                    print(f"... ({len(text) - 500} more characters)")
                print("-" * 70)
                
                words = result.get("words", [])
                if words:
                    print(f"\n📊 Extracted Words ({len(words)}):")
                    for i, word in enumerate(words[:10]):  # First 10 words
                        text = word.get("text", "?")
                        conf = word.get("confidence", 0)
                        bbox = word.get("bbox", [])
                        print(f"   {i+1}. \"{text}\" (conf: {conf:.2f}, bbox: {bbox})")
                
            return {
                "success": True,
                "elapsed_seconds": elapsed,
                "text_length": len(text),
                "words_count": len(words),
                "result": result
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"Request timed out after {self.timeout}s",
                "elapsed_seconds": self.timeout
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "elapsed_seconds": 0
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse response: {e}",
                "elapsed_seconds": 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "elapsed_seconds": 0
            }
    
    def run_full_test(self) -> None:
        """Run complete test: service check, image generation, OCR processing."""
        print("\n" + "🔷" * 35)
        print("EasyOCR Flow - Full Test")
        print("🔷" * 35)
        
        # Step 1: Check service
        service_healthy = self.check_service()
        
        if not service_healthy:
            print("\n❌ Cannot proceed with OCR test - service not accessible")
            print("   Troubleshooting:")
            print("   1. Check if container is running: docker ps | grep easyocr")
            print("   2. View container logs: docker logs easyocr")
            print("   3. Restart if needed: cd ~/stack && docker compose restart easyocr")
            print("   4. Check if service is listening: curl http://127.0.0.1:5000/")
            return
        
        # Step 2: Generate test receipt
        test_image = self.generate_test_receipt()
        
        if not test_image:
            print("\n⚠️  Skipping OCR test (no test image available)")
            return
        
        # Step 3: Test OCR
        result = self.test_ocr(test_image)
        
        # Summary
        print("\n" + "="*70)
        print("📊 Test Summary")
        print("="*70)
        
        if result["success"]:
            print(f"✅ OCR Test PASSED")
            print(f"   Processing Time: {result['elapsed_seconds']:.2f}s")
            print(f"   Text Extracted: {result['text_length']} characters")
            print(f"   Words Detected: {result['words_count']}")
            print(f"\n   💡 Next Step: Integrate this into Nexus Bag module")
            print(f"      - Use EasyOCR for receipt text extraction")
            print(f"      - Send OCR text to GLM-4 for interpretation")
            print(f"      - Parse structured data (merchant, items, total)")
        else:
            print(f"❌ OCR Test FAILED")
            print(f"   Error: {result.get('error', 'Unknown')}")
            print(f"   Processing Time: {result['elapsed_seconds']:.2f}s")


def main():
    """Run the EasyOCR flow test."""
    print("\n" + "="*70)
    print("🚀 EasyOCR Flow Test")
    print("Author: Levy (Agent Faza)")
    print("Date: 2026-02-17")
    print("="*70)
    
    tester = EasyOCRTester()
    tester.run_full_test()


if __name__ == "__main__":
    main()
