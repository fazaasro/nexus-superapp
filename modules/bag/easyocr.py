"""
EasyOCR Integration Module for Nexus Bag Module

This module provides OCR functionality using a self-hosted EasyOCR service.
No API keys required - runs entirely on local infrastructure.

Author: Levy (Agent Faza)
Date: 2026-02-17
"""

import base64
import json
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path


class EasyOCRProcessor:
    """
    OCR processor using self-hosted EasyOCR service.
    
    Runs entirely on local infrastructure - no external API calls.
    Fast CPU-optimized processing (0.5-2s per image).
    """

    def __init__(self, service_url: str = "http://127.0.0.1:5000"):
        """
        Initialize EasyOCR processor.
        
        Args:
            service_url: URL of the EasyOCR service (default: localhost:5000)
        """
        self.service_url = service_url.rstrip('/')
        self.timeout = 30  # 30 second timeout for OCR processing

    def _read_image_as_base64(self, image_path: str) -> Optional[str]:
        """
        Read image file and convert to base64.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64-encoded image string, or None if file doesn't exist
        """
        try:
            with open(image_path, 'rb') as f:
                img_bytes = f.read()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                return img_base64
        except FileNotFoundError:
            print(f"❌ Image file not found: {image_path}")
            return None
        except Exception as e:
            print(f"❌ Error reading image: {e}")
            return None

    def process_image(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a single image and extract text.
        
        Args:
            image_path: Path to image file (JPG, PNG, etc.)
            
        Returns:
            Dictionary with OCR results:
            {
                "text": "Extracted text",
                "words": [
                    {"text": "word", "bbox": [x1, y1, x2, y2], "confidence": 0.95}
                ],
                "success": True,
                "error": None
            }
            Returns None if processing fails.
        """
        print(f"🔍 Processing: {image_path}")
        
        # Read and encode image
        img_base64 = self._read_image_as_base64(image_path)
        if img_base64 is None:
            return None

        # Prepare request
        # EasyOCR API expects base64 image in JSON format
        payload = {
            "image": f"data:image/jpeg;base64,{img_base64}"
        }

        try:
            # Send to EasyOCR service
            response = requests.post(
                f"{self.service_url}/predict",
                json=payload,
                timeout=self.timeout
            )
            
            # Check response
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ OCR completed: {len(result.get('text', ''))} characters extracted")
            
            return {
                "text": result.get("text", ""),
                "words": result.get("words", []),
                "success": True,
                "error": None
            }

        except requests.exceptions.Timeout:
            print(f"❌ OCR request timed out (>{self.timeout}s)")
            return {
                "text": "",
                "words": [],
                "success": False,
                "error": f"Timeout after {self.timeout}s"
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ OCR request failed: {e}")
            return {
                "text": "",
                "words": [],
                "success": False,
                "error": str(e)
            }
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse OCR response: {e}")
            return {
                "text": "",
                "words": [],
                "success": False,
                "error": f"JSON decode error: {e}"
            }

    def process_receipt(self, image_path: str) -> Dict[str, Any]:
        """
        Process receipt image and extract structured data.
        
        Focuses on receipt-specific content:
        - Merchant name (usually at top)
        - Date/time
        - Line items
        - Total amount (usually near "TOTAL" or "TOTAL")
        
        Args:
            image_path: Path to receipt image
            
        Returns:
            Structured receipt data:
            {
                "merchant": "Store name",
                "date": "2026-02-17",
                "items": [
                    {"name": "Item 1", "price": 10.50},
                    {"name": "Item 2", "price": 5.00}
                ],
                "total": 15.50,
                "raw_text": "Full extracted text",
                "success": True
            }
        """
        print(f"🧾 Processing receipt: {image_path}")
        
        # Get OCR text
        ocr_result = self.process_image(image_path)
        
        if not ocr_result or not ocr_result["success"]:
            return {
                "merchant": "",
                "date": "",
                "items": [],
                "total": 0.0,
                "raw_text": "",
                "success": False,
                "error": ocr_result.get("error", "Unknown error") if ocr_result else "No OCR result"
            }
        
        # Extract text
        text = ocr_result["text"]
        lines = text.strip().split('\n')
        
        # Simple heuristics to extract receipt data
        # This is basic - for complex receipts, would use LLM reasoning
        
        merchant = ""
        date_str = ""
        total = 0.0
        items = []
        
        # Look for merchant (first non-empty line)
        for line in lines:
            if line.strip():
                merchant = line.strip()
                break
        
        # Look for date patterns (DD/MM/YYYY, YYYY-MM-DD, etc.)
        import re
        date_pattern = r'\d{2}[-/]\d{2}[-/]\d{2,4}|\d{4}[-/]\d{2}[-/]\d{2}'
        for line in lines:
            match = re.search(date_pattern, line)
            if match:
                date_str = match.group()
                break
        
        # Look for total amount (lines with "TOTAL" or "TOTAL" and currency)
        for line in lines:
            if "TOTAL" in line.upper():
                # Extract amount (look for currency pattern: $10.50, IDR 50,000, etc.)
                amount_match = re.search(r'[\$RpIDR\s]*\s*[\d,]+\.?\d*', line)
                if amount_match:
                    try:
                        # Remove non-numeric characters
                        amount_str = re.sub(r'[^\d.,]', '', amount_match.group())
                        total = float(amount_str.replace(',', ''))
                    except:
                        pass
                break
        
        print(f"📊 Extracted: Merchant={merchant}, Total={total}")
        
        return {
            "merchant": merchant,
            "date": date_str,
            "items": items,  # Would need LLM to parse line items
            "total": total,
            "raw_text": text,
            "success": True,
            "error": None
        }


def test_easyocr_service(service_url: str = "http://127.0.0.1:5000") -> bool:
    """
    Test if EasyOCR service is running and accessible.
    
    Args:
        service_url: URL of the EasyOCR service
        
    Returns:
        True if service is healthy, False otherwise
    """
    try:
        response = requests.get(f"{service_url}/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main():
    """Example usage of EasyOCR processor."""
    print("="*70)
    print("EASYOCR PROCESSOR - Nexus Bag Module")
    print("="*70)
    
    # Test service
    print("\n🔍 Testing EasyOCR service...")
    if test_easyocr_service():
        print("✅ EasyOCR service is running at http://127.0.0.1:5000")
    else:
        print("❌ EasyOCR service is not accessible")
        print("   Start service: cd ~/stack && docker compose up -d easyocr")
        return
    
    # Create processor
    ocr = EasyOCRProcessor()
    
    # Example usage (uncomment to test)
    # result = ocr.process_receipt("/path/to/receipt.jpg")
    # print(f"\nResult: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
