# /modules/bag/ocr.py
"""
OCR processor using OpenAI Vision API for receipt text extraction.
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

class OCRProcessor:
    """Process images using OpenAI Vision API to extract text."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OCR processor.

        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var.

        Raises:
            ImportError: If openai package is not installed.
            ValueError: If API key is not provided.
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package is not installed. "
                "Install it with: pip install openai"
            )

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key param.")

        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
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
        Extract text from image using GPT-4 Vision.
        
        Args:
            image_path: Path to image file.
            prompt: Custom prompt for extraction. Default optimized for receipts.
            
        Returns:
            Dict with extracted text and metadata.
            
        Raises:
            FileNotFoundError: If image doesn't exist.
            ValueError: If API call fails.
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Default prompt optimized for receipts
        if prompt is None:
            prompt = """Extract all text from this receipt image. 
            Include merchant name, date, items, prices, totals, and any other visible text.
            Format the output in a structured way that preserves receipt layout."""
        
        try:
            # Encode image
            base64_image = self._encode_image(image_path)
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
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
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                }
            }
            
        except openai.APIError as e:
            return {
                "success": False,
                "error": f"OpenAI API error: {str(e)}",
                "image_path": image_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "image_path": image_path
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
