# /modules/bag/ocr.py
"""
OCR processor using PaddleOCR, OpenAI Vision API, or self-hosted EasyOCR for receipt text extraction.

Architecture:
- Default: PaddleOCR (self-hosted, free, fast)
- Fallback: EasyOCR (self-hosted service)
- OpenAI Vision API (requires API key, slower, costs money)

Author: Levy (Agent Faza)
Date: 2026-02-17
Updated: 2026-02-18 - Added PaddleOCR support
"""
import os
import sys
import json
import base64
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

# IMPORTANT: Set these BEFORE importing paddleocr to avoid MKLDNN bug
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

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

# Lazy import of paddleocr
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    PaddleOCR = None


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


class PaddleOCRProcessor:
    """
    OCR processor using PaddleOCR (Baidu's open-source OCR engine).

    Runs entirely on local infrastructure - no external API calls.
    Fast CPU-optimized processing (1-5s per image).
    Supports 80+ languages including English, Indonesian, Chinese.

    Requirements:
    - PaddleOCR installed: pip install paddleocr
    - System dependencies: libgl1, libglib2.0-0, etc.
    - MKLDNN disabled (bug workaround)
    """

    def __init__(self, paddleocr_path: Optional[str] = None, lang: str = 'en'):
        """
        Initialize PaddleOCR processor.

        Args:
            paddleocr_path: Path to PaddleOCR executable (auto-detected if None).
            lang: Language model ('en', 'id', 'ch', etc.)
        """
        self.lang = lang
        self.timeout = 60  # 60 second timeout for OCR processing

        # Try to find PaddleOCR in virtual environments
        if paddleocr_path is None:
            possible_paths = [
                Path("/home/ai-dev/.openclaw/workspace/paddle_env2/bin/paddleocr"),
                Path("/home/ai-dev/.openclaw/workspace/paddle_env/bin/paddleocr"),
                Path("paddle_env2/bin/paddleocr"),
                Path("paddle_env/bin/paddleocr"),
            ]
            for path in possible_paths:
                if path.exists():
                    self.paddleocr_path = str(path)
                    break
            else:
                # Try system path
                self.paddleocr_path = "paddleocr"
        else:
            self.paddleocr_path = paddleocr_path

        # Verify PaddleOCR is available
        try:
            result = subprocess.run(
                [self.paddleocr_path, "--help"],
                capture_output=True,
                timeout=5
            )
            self.available = True
            print(f"✅ PaddleOCR found at: {self.paddleocr_path}")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.available = False
            print(f"⚠️ PaddleOCR not found at: {self.paddleocr_path}")

    def process_image(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a single image and extract text using PaddleOCR.

        Args:
            image_path: Path to image file (JPG, PNG, etc.)

        Returns:
            Dictionary with OCR results
        """
        print(f"🔍 [PaddleOCR] Processing: {image_path}")

        if not self.available:
            print(f"❌ [PaddleOCR] Not available - cannot process image")
            return {
                "success": False,
                "error": "PaddleOCR executable not found",
                "image_path": image_path,
                "backend": "paddleocr"
            }

        # Check if image exists
        if not Path(image_path).exists():
            print(f"❌ [PaddleOCR] Image not found: {image_path}")
            return {
                "success": False,
                "error": f"Image file not found: {image_path}",
                "image_path": image_path,
                "backend": "paddleocr"
            }

        # Prepare environment variables to disable MKLDNN
        env = os.environ.copy()
        env['FLAGS_use_mkldnn'] = '0'
        env['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

        try:
            # Run PaddleOCR CLI
            cmd = [
                self.paddleocr_path,
                "ocr",
                "-i", image_path,
                "--lang", self.lang,
                "--use_textline_orientation", "false",
                "--enable_mkldnn", "false",
                "--ocr_version", "PP-OCRv5"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=env
            )

            if result.returncode != 0:
                print(f"❌ [PaddleOCR] CLI error (exit code {result.returncode})")
                print(f"stderr: {result.stderr}")
                return {
                    "success": False,
                    "error": f"PaddleOCR CLI failed: {result.stderr}",
                    "image_path": image_path,
                    "backend": "paddleocr"
                }

            # Parse output to extract text
            # PaddleOCR outputs Python dict to stderr (not stdout!)
            output_text = result.stderr

            # Extract rec_texts from the output
            extracted_texts = self._parse_paddleocr_output(output_text)

            if not extracted_texts:
                print(f"⚠️ [PaddleOCR] No text extracted")
                return {
                    "success": True,
                    "text": "",
                    "texts": [],
                    "image_path": image_path,
                    "backend": "paddleocr"
                }

            # Combine all texts into full text
            full_text = "\n".join(extracted_texts)

            print(f"✅ [PaddleOCR] Completed: {len(extracted_texts)} text lines extracted")
            print(f"📄 Text preview: {full_text[:100]}...")

            return {
                "success": True,
                "text": full_text,
                "texts": extracted_texts,
                "image_path": image_path,
                "backend": "paddleocr"
            }

        except subprocess.TimeoutExpired:
            print(f"❌ [PaddleOCR] Request timed out (>{self.timeout}s)")
            return {
                "success": False,
                "error": f"Timeout after {self.timeout}s",
                "image_path": image_path,
                "backend": "paddleocr"
            }
        except Exception as e:
            print(f"❌ [PaddleOCR] Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path,
                "backend": "paddleocr"
            }

    def _parse_paddleocr_output(self, output: str) -> List[str]:
        """
        Parse PaddleOCR CLI output to extract text.

        Args:
            output: Raw output from PaddleOCR CLI

        Returns:
            List of extracted text strings
        """
        texts = []

        try:
            import re

            # PaddleOCR outputs Python dict representation
            # Look for 'rec_texts' array in the output
            # Pattern: 'rec_texts': ['text1', 'text2', ...]
            pattern = r"'rec_texts'\s*:\s*\[(.*?)\](?=\s*,\s*'rec_scores')"
            match = re.search(pattern, output, re.DOTALL)

            if match:
                # Extract the array content
                array_content = match.group(1)

                # Parse quoted strings from the array
                # Handle both single and double quotes
                str_pattern = r"['\"]([^'\"]+)['\"]"
                str_matches = re.findall(str_pattern, array_content)

                if str_matches:
                    texts = str_matches
                    print(f"📋 [PaddleOCR] Extracted {len(texts)} text lines via rec_texts")
                    return texts

            # Fallback: look for the rec_texts line specifically
            for line in output.split('\n'):
                if "'rec_texts':" in line or '"rec_texts":' in line:
                    # Find the array start
                    start_idx = line.find('[')
                    if start_idx == -1:
                        continue

                    # Collect lines until we find the closing bracket
                    array_text = line[start_idx:]
                    bracket_count = array_text.count('[') - array_text.count(']')

                    if bracket_count > 0:
                        # Need to read more lines to close the array
                        line_idx = output.split('\n').index(line)
                        for subsequent_line in output.split('\n')[line_idx + 1:]:
                            array_text += subsequent_line
                            bracket_count += subsequent_line.count('[') - subsequent_line.count(']')
                            if bracket_count <= 0:
                                break

                    # Extract quoted strings from the array
                    str_matches = re.findall(r"['\"]([^'\"]+)['\"]", array_text)
                    if str_matches:
                        # Filter out non-text content
                        keywords_to_filter = {'input_path', 'page_index', 'model_settings',
                                           'use_doc_preprocessor', 'use_textline_orientation',
                                           'text_det_params', 'text_type', 'rec_texts', 'rec_scores',
                                           'rec_polys', 'rec_boxes', 'dt_polys', 'doc_preprocessor_res',
                                           'angle', 'limit_side_len', 'limit_type', 'thresh', 'max_side_limit',
                                           'box_thresh', 'unclip_ratio', 'text_rec_score_thresh',
                                           'return_word_box', 'lang', 'ocr_version'}
                        texts = [m for m in str_matches if m not in keywords_to_filter and len(m) > 0]
                        print(f"📋 [PaddleOCR] Extracted {len(texts)} text lines via fallback")
                        return texts

            print(f"⚠️ [PaddleOCR] Could not find rec_texts in output")
            print(f"📄 Output preview: {output[:500]}...")

        except Exception as e:
            print(f"⚠️ [PaddleOCR] Error parsing output: {e}")
            import traceback
            traceback.print_exc()

        return texts


class OCRProcessor:
    """
    Process images using OCR (PaddleOCR, EasyOCR or OpenAI Vision).

    Backends:
    - paddleocr: Self-hosted, free, fast (default)
    - easyocr: Self-hosted service, free, fast
    - openai: Cloud API, accurate, costs money
    """

    def __init__(self, api_key: Optional[str] = None, backend: str = "paddleocr",
                 easyocr_url: str = "http://127.0.0.1:5000", paddleocr_path: Optional[str] = None):
        """
        Initialize OCR processor.

        Args:
            api_key: OpenAI API key (required if backend='openai').
            backend: OCR backend to use ('paddleocr', 'easyocr' or 'openai'). Default: 'paddleocr'.
            easyocr_url: URL of EasyOCR service (default: localhost:5000).
            paddleocr_path: Path to PaddleOCR executable (auto-detected if None).

        Raises:
            ImportError: If required package is not installed.
            ValueError: If API key is required but not provided.
        """
        self.backend = backend
        self.paddleocr_processor = None
        self.easyocr_processor = None
        self.openai_processor = None

        if backend == "paddleocr":
            # Use PaddleOCR (default - self-hosted, free)
            self.paddleocr_processor = PaddleOCRProcessor(paddleocr_path=paddleocr_path)
            print(f"✅ OCR backend: PaddleOCR (self-hosted)")

        elif backend == "easyocr":
            # Use EasyOCR (self-hosted service)
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
            raise ValueError(f"Invalid backend: {backend}. Must be 'paddleocr', 'easyocr' or 'openai'")
    
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
        if self.backend == "paddleocr" and self.paddleocr_processor:
            # Use PaddleOCR (self-hosted, fast, free)
            result = self.paddleocr_processor.process_image(image_path)
            # Add prompt to result for consistency
            result["prompt_used"] = None  # PaddleOCR doesn't use prompts
            return result

        elif self.backend == "easyocr" and self.easyocr_processor:
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
