#!/usr/bin/env python3
"""
Test Kimi Native Vision for Nexus (The Bag) OCR
Uses Kimi's native image_in capabilities instead of OpenAI Vision API.
"""
import sys
import subprocess
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_kimi_ocr():
    """Test Kimi native vision with receipt image"""
    print("\n" + "="*60)
    print("KIMI NATIVE VISION OCR TEST")
    print("="*60)
    
    # Check if receipt image exists
    receipt_path = "/tmp/test_receipt.jpg"
    if not Path(receipt_path).exists():
        print(f"❌ Receipt image not found: {receipt_path}")
        print("   Place a receipt image at the specified path")
        return None
    
    # Create Kimi prompt for OCR
    prompt = """Analyze this receipt image and extract ALL information:

Return a JSON object with these fields:
{
  "merchant": "store name",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "total": "XX.XX",
  "currency": "IDR or USD or EUR",
  "tax": "XX.XX if visible",
  "items": [
    {
      "name": "item name",
      "quantity": 1,
      "price": "XX.XX",
      "category": "Food/Groceries/Transport/etc"
    }
  ],
  "payment_method": "Cash/Card/E-Wallet",
  "qr_codes": ["QR123", "QR456" if visible],
  "confidence": 0.0 to 1.0,
  "raw_text": "full text extraction from receipt"
}

IMPORTANT: 
- Be as accurate as possible
- Extract ALL items with quantities and prices
- Identify merchant name prominently
- Note any special offers or discounts
- Extract QR codes if present
- Return ONLY valid JSON (no markdown formatting)

Focus on accuracy - this is real financial data!"""
    
    # Create Kimi command
    kimi_cmd = [
        "kimi",
        "-m", "models.gemini-3-pro-preview",
        "-p", prompt,
        "--quiet"  # Minimize output noise
    ]
    
    print(f"\n📸 Running Kimi OCR on: {receipt_path}")
    print(f"   Model: models.gemini-3-pro-preview")
    print(f"   Prompt: Extract structured JSON from receipt")
    
    try:
        # Run Kimi with the image path
        # Kimi will prompt for image input
        result = subprocess.run(
            kimi_cmd,
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes max
        )
        
        # Check if Kimi succeeded
        if result.returncode == 0:
            print("\n✅ Kimi OCR completed successfully")
            print(f"\n📄 Output from Kimi:")
            print("-" * 60)
            print(result.stdout)
            print("-" * 60)
            
            # Try to parse JSON from output
            try:
                # Extract JSON from Kimi response
                if "```json" in result.stdout:
                    json_start = result.stdout.find("```json") + 7
                    json_end = result.stdout.find("```", json_start)
                    json_str = result.stdout[json_start:json_end].strip()
                    ocr_data = json.loads(json_str)
                    
                    print("\n📊 Parsed OCR Results:")
                    print(f"   Merchant: {ocr_data.get('merchant', 'Unknown')}")
                    print(f"   Date: {ocr_data.get('date', 'Unknown')}")
                    print(f"   Time: {ocr_data.get('time', 'Unknown')}")
                    print(f"   Total: {ocr_data.get('currency', '')} {ocr_data.get('total', 'Unknown')}")
                    print(f"   Payment: {ocr_data.get('payment_method', 'Unknown')}")
                    print(f"   Items: {len(ocr_data.get('items', []))}")
                    print(f"   QR Codes: {len(ocr_data.get('qr_codes', []))}")
                    print(f"   Confidence: {ocr_data.get('confidence', 0.0):.2f}")
                    
                    return ocr_data
                else:
                    # Try to find JSON directly
                    lines = result.stdout.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('{') and line.endswith('}'):
                            ocr_data = json.loads(line)
                            
                            print("\n📊 Parsed OCR Results:")
                            print(f"   Merchant: {ocr_data.get('merchant', 'Unknown')}")
                            print(f"   Date: {ocr_data.get('date', 'Unknown')}")
                            print(f"   Time: {ocr_data.get('time', 'Unknown')}")
                            print(f"   Total: {ocr_data.get('currency', '')} {ocr_data.get('total', 'Unknown')}")
                            print(f"   Payment: {ocr_data.get('payment_method', 'Unknown')}")
                            print(f"   Items: {len(ocr_data.get('items', []))}")
                            print(f"   QR Codes: {len(ocr_data.get('qr_codes', []))}")
                            print(f"   Confidence: {ocr_data.get('confidence', 0.0):.2f}")
                            
                            return ocr_data
                    
                    print("\n⚠️  Could not parse JSON from Kimi output")
                    print("   Raw output above - manual review needed")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ Failed to parse JSON from Kimi output: {e}")
                print("   Raw output:")
                print(result.stdout[:500])
                return None
                
        else:
            print(f"\n❌ Kimi returned error code: {result.returncode}")
            print(f"\n📄 Error Output:")
            print(result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print("\n❌ Kimi OCR timed out (2 minutes)")
        print("   Try with a simpler receipt image")
        return None
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None


if __name__ == "__main__":
    result = test_kimi_ocr()
    
    if result:
        print("\n✅ Test PASSED: Kimi Native Vision working!")
        print("\n📋 Next Steps:")
        print("   1. Integrate Kimi OCR into Nexus Bag module")
        print("   2. Replace OpenAI Vision API calls")
        print("   3. Test with Indonesian bank statement data")
        print("   4. Update test cases with real receipts")
        
        # Save results to file
        output_file = Path("/tmp/kimi_ocr_result.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    else:
        print("\n❌ Test FAILED: Check output above")
