# /modules/bag/ocr.py
"""
OCR processor using OpenAI Vision API or self-hosted EasyOCR for receipt text extraction.

Architecture:
- Default: EasyOCR (self-hosted, free, fast)
- Fallback: OpenAI Vision API (requires API key, slower, costs money)

Author: Levy (Agent Faza)
Date: 2026-02-17
"""
import os
import base64
from typing import Optional, Dict, Any
from pathlib import Path

# Lazy import of openai to allow module usage without API key
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

# Lazy import of requests for EasyOCR
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None


class EasyOCRProcessor:
    """
    OCR processor using self-hosted EasyOCR service.
    
    Runs entirely on local infrastructure - no external API calls.
    Fast CPU-optimized processing (0.5-2s per image).
    
    Requires EasyOCR service running at http://127.0.0.1:5000
    """
    
    def __init__(self, service_url: str = "http://127.0.0.1:5000"):
        """
        Initialize EasyOCR processor.
        
        Args:
            service_url: URL of the EasyOCR service (default: localhost:5000)
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests package is not installed. "
                "Install it with: pip install requests"
            )
        
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
        Process a single image and extract text using EasyOCR.
        
        Args:
            image_path: Path to image file (JPG, PNG, etc.)
            
        Returns:
            Dictionary with OCR results
        """
        print(f"🔍 [EasyOCR] Processing: {image_path}")
        
        # Read and encode image
        img_base64 = self._read_image_as_base64(image_path)
        if img_base64 is None:
            return None

        # Prepare request
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
            
            text = result.get("text", "")
            print(f"✅ [EasyOCR] Completed: {len(text)} characters extracted")
            
            return {
                "success": True,
                "text": text,
                "image_path": image_path,
                "backend": "easyocr",
                "words": result.get("words", [])
            }

        except requests.exceptions.Timeout:
            print(f"❌ [EasyOCR] Request timed out (>{self.timeout}s)")
            return {
                "success": False,
                "error": f"Timeout after {self.timeout}s",
                "image_path": image_path,
                "backend": "easyocr"
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ [EasyOCR] Request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path,
                "backend": "easyocr"
            }
        except Exception as e:
            print(f"❌ [EasyOCR] Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path,
                "backend": "easyocr"
            }


class OCRProcessor:
    """
    Process images using OCR (EasyOCR or OpenAI Vision).
    
    Backends:
    - easyocr: Self-hosted, free, fast (default)
    - openai: Cloud API, accurate, costs money
    """
    
    def __init__(self, api_key: Optional[str] = None, backend: str = "easyocr", easyocr_url: str = "http://127.0.0.1:5000"):
        """
        Initialize OCR processor.

        Args:
            api_key: OpenAI API key (required if backend='openai').
            backend: OCR backend to use ('easyocr' or 'openai'). Default: 'easyocr'.
            easyocr_url: URL of EasyOCR service (default: localhost:5000).

        Raises:
            ImportError: If required package is not installed.
            ValueError: If API key is required but not provided.
        """
        self.backend = backend
        self.easyocr_processor = None
        self.openai_processor = None
        
        if backend == "easyocr":
            # Use EasyOCR (default - self-hosted, free)
            self.easyocr_processor = EasyOCRProcessor(service_url=easyocr_url)
            print(f"✅ OCR backend: EasyOCR (self-hosted at {easyocr_url})")
            
        elif backend == "openai":
            # Use OpenAI Vision API (requires API key)
            if not OPENAI_AVAILABLE:
                raise ImportError(
                    "OpenAI package is not installed. "
                    "Install it with: pip install openai"
                )
            
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key required for backend='openai'. Set OPENAI_API_KEY env var or pass api_key param.")
            
            import openai
            openai.api_key = api_key
            self.openai_processor = openai.OpenAI(api_key=api_key)
            print("✅ OCR backend: OpenAI Vision API (requires API key)")
            
        else:
            raise ValueError(f"Invalid backend: {backend}. Must be 'easyocr' or 'openai'")
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64.
        
        Args:
            image_path: Path to image file.
            
        Returns:
            Base64 encoded string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_text(self, image_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract text from image using selected OCR backend.
        
        Args:
            image_path: Path to image file.
            prompt: Custom prompt for extraction (only for OpenAI Vision).
            
        Returns:
            Dict with extracted text and metadata.
            
        Raises:
            FileNotFoundError: If image doesn't exist.
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Route to appropriate backend
        if self.backend == "easyocr" and self.easyocr_processor:
            # Use EasyOCR (self-hosted, fast)
            result = self.easyocr_processor.process_image(image_path)
            # Add prompt to result for consistency
            result["prompt_used"] = None  # EasyOCR doesn't use prompts
            return result
            
        elif self.backend == "openai" and self.openai_processor:
            # Use OpenAI Vision API (accurate, costs money)
            # Default prompt optimized for receipts
            if prompt is None:
                prompt = """Extract all text from this receipt image. 
                Include merchant name, date, items, prices, totals, and any other visible text.
                Format the output in a structured way that preserves the receipt layout."""
            
            try:
                # Encode image
                base64_image = self._encode_image(image_path)
                
                # Call OpenAI Vision API
                response = self.openai_processor.chat.completions.create(
                    model="gpt-4o",  # GPT-4 with vision capabilities
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=2000,
                )
                
                extracted_text = response.choices[0].message.content
                
                return {
                    "success": True,
                    "text": extracted_text,
                    "image_path": image_path,
                    "model": "gpt-4o",
                    "backend": "openai",
                    "prompt_used": prompt,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                        "total_tokens": response.usage.total_tokens if response.usage else 0,
                    }
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": f"OpenAI API error: {str(e)}",
                    "image_path": image_path,
                    "backend": "openai"
                }
        
        else:
            return {
                "success": False,
                "error": f"No OCR processor available for backend: {self.backend}",
                "image_path": image_path,
                "backend": self.backend
            }
    
    def extract_structured_data(self, image_path: str) -> Dict[str, Any]:
        """
        Extract structured receipt data (merchant, date, total, items).
        
        Args:
            image_path: Path to receipt image.
            
        Returns:
            Dict with structured receipt data.
        """
        prompt = """Extract structured information from this receipt:
        - Merchant/store name
        - Date and time
        - Line items (name, quantity, price)
        - Subtotal, tax, and total amounts
        - Payment method
        
        Return as JSON format with keys: merchant, date, items[], subtotal, tax, total, payment_method."""
        
        return self.extract_text(image_path, prompt)
