"""
Module 1: The Bag (Finance)
Receipt OCR, Classification, Split Logic, Runway Calculation
"""
import json
import uuid
import re
import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any
from pathlib import Path

from core.database import get_db, generate_uuid, log_audit
from .ocr import OCRProcessor

# Configure logging
logger = logging.getLogger(__name__)


class BagModule:
    """Finance management module"""

    CATEGORIES = ['survival', 'health', 'lifestyle', 'trash', 'income', 'investment']
    SPLIT_TYPES = ['solo', 'split_equal', 'split_custom']

    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "levy.db"
        # Initialize OCR processor for receipt processing
        self.ocr_processor = None
    
    # ========== TRANSACTION CRUD ==========
    
    def create_transaction(self, data: Dict, user_id: str) -> Dict:
        """Create a new transaction"""
        txn_id = f"txn_{generate_uuid()}"
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO transactions 
                   (id, owner, created_by, raw_text, merchant, amount, currency,
                    category, impact_score, split_type, faza_portion, gaby_portion,
                    is_business, client, tags, location, payment_method, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    txn_id,
                    data.get('owner', user_id),
                    user_id,
                    data.get('raw_text'),
                    data.get('merchant'),
                    data.get('amount'),
                    data.get('currency', 'EUR'),
                    data.get('category', 'lifestyle'),
                    data.get('impact_score', 3),
                    data.get('split_type', 'solo'),
                    data.get('faza_portion', 1.0 if user_id == 'faza' else 0.0),
                    data.get('gaby_portion', 1.0 if user_id == 'gaby' else 0.0),
                    data.get('is_business', False),
                    data.get('client'),
                    json.dumps(data.get('tags', [])),
                    data.get('location'),
                    data.get('payment_method'),
                    data.get('notes')
                )
            )
        
        # Audit log
        log_audit(user_id, 'bag', 'create', 'transaction', txn_id, 
                 {'amount': data.get('amount'), 'merchant': data.get('merchant')})
        
        return {'id': txn_id, 'status': 'created'}
    
    def get_transactions(self, user_id: str, include_shared: bool = True,
                        category: str = None, limit: int = 50) -> List[Dict]:
        """Get transactions for user"""
        owners = [user_id]
        if include_shared:
            owners.append('shared')
        
        query = "SELECT * FROM transactions WHERE owner IN ({})".format(
            ','.join(['?' for _ in owners])
        )
        params = owners.copy()
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        transactions = []
        for row in rows:
            txn = dict(row)
            if txn.get('tags'):
                txn['tags'] = json.loads(txn['tags'])
            transactions.append(txn)
        
        return transactions
    
    def update_split(self, txn_id: str, split_type: str, user_id: str,
                    faza_portion: float = None, gaby_portion: float = None) -> Dict:
        """Update bill split for a transaction"""
        
        if split_type == 'solo':
            # Assign to the user who created it
            faza_portion = 1.0 if user_id == 'faza' else 0.0
            gaby_portion = 1.0 if user_id == 'gaby' else 0.0
        elif split_type == 'split_equal':
            faza_portion = 0.5
            gaby_portion = 0.5
        elif split_type == 'split_custom':
            # Use provided portions
            if faza_portion is None or gaby_portion is None:
                return {'error': 'Custom split requires portions'}
        
        with get_db() as conn:
            conn.execute(
                """UPDATE transactions 
                   SET split_type = ?, faza_portion = ?, gaby_portion = ?
                   WHERE id = ?""",
                (split_type, faza_portion, gaby_portion, txn_id)
            )
        
        log_audit(user_id, 'bag', 'update', 'transaction', txn_id,
                 {'split_type': split_type, 'faza': faza_portion, 'gaby': gaby_portion})
        
        return {'id': txn_id, 'split_type': split_type, 
                'faza_portion': faza_portion, 'gaby_portion': gaby_portion}
    
    # ========== RUNWAY CALCULATION ==========

    def calculate_runway(self, user_id: str, current_balance: float = None) -> Dict:
        """Calculate days of survival remaining"""

        # Get average monthly spend (last 3 months)
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT AVG(monthly_spend) as avg_spend
                   FROM (
                       SELECT
                           strftime('%Y-%m', timestamp) as month,
                           SUM(amount) as monthly_spend
                       FROM transactions
                       WHERE owner IN (?, 'shared')
                         AND category != 'income'
                         AND timestamp > datetime('now', '-3 months')
                       GROUP BY strftime('%Y-%m', timestamp)
                   )""",
                (user_id,)
            )
            row = cursor.fetchone()
            avg_monthly = row['avg_spend'] or 0

        if avg_monthly == 0:
            return {'error': 'No spending data available'}

        # Calculate current balance if not provided
        if current_balance is None:
            current_balance = self._get_current_balance(user_id)

        daily_burn = avg_monthly / 30
        days_remaining = int(current_balance / daily_burn)

        depletion_date = datetime.now() + timedelta(days=days_remaining)

        return {
            'days_remaining': days_remaining,
            'months_remaining': round(days_remaining / 30, 1),
            'daily_burn': round(daily_burn, 2),
            'monthly_burn': round(avg_monthly, 2),
            'current_balance': current_balance,
            'projected_depletion': depletion_date.isoformat(),
            'status': 'critical' if days_remaining < 30 else
                     'warning' if days_remaining < 90 else 'healthy'
        }

    def _get_current_balance(self, user_id: str) -> float:
        """
        Get current balance from database or bank API.

        Calculates balance from:
        1. Sum of income transactions
        2. Sum of expense transactions

        Future: Integrate with bank API for real-time balance.
        """
        with get_db() as conn:
            # Calculate total income
            income = conn.execute(
                """SELECT COALESCE(SUM(amount), 0) as total
                   FROM transactions
                   WHERE owner IN (?, 'shared')
                   AND category = 'income'""",
                (user_id,)
            ).fetchone()['total']

            # Calculate total expenses
            expenses = conn.execute(
                """SELECT COALESCE(SUM(amount), 0) as total
                   FROM transactions
                   WHERE owner IN (?, 'shared')
                   AND category != 'income'""",
                (user_id,)
            ).fetchone()['total']

            current_balance = income - expenses

            logger.info(f"Balance for {user_id}: income={income}, expenses={expenses}, current={current_balance}")

            return current_balance

    def get_bank_balance(self, user_id: str, bank_account_id: str = None) -> Dict:
        """
        Get real-time balance from bank API.

        This is a placeholder for future bank API integration.
        Supported APIs (to be implemented):
        - Plaid (US banks)
        - Yodlee (global)
        - Open Banking (EU PSD2)
        - GoCardless (UK)

        Args:
            user_id: User ID
            bank_account_id: Specific bank account ID (optional)

        Returns:
            Dict with balance information

        Note: This requires OAuth flow with bank and API credentials.
        """
        # TODO: Integrate with bank API (Plaid, Yodlee, etc.)
        # For now, return calculated balance
        try:
            balance = self._get_current_balance(user_id)
            return {
                'balance': balance,
                'currency': 'EUR',
                'source': 'calculated',
                'account_id': bank_account_id or 'all_accounts',
                'timestamp': datetime.now().isoformat(),
                'message': 'Bank API integration pending - using calculated balance'
            }
        except Exception as e:
            logger.error(f"Error getting bank balance: {e}")
            return {
                'error': str(e),
                'balance': 0,
                'source': 'error'
            }

    # ========== SUBSCRIPTION DETECTION ==========
    
    def detect_subscriptions(self, user_id: str) -> List[Dict]:
        """ML-based pattern detection for recurring charges"""
        
        with get_db() as conn:
            # Find merchants with multiple charges
            cursor = conn.execute(
                """SELECT 
                    merchant,
                    amount,
                    COUNT(*) as charge_count,
                    MIN(timestamp) as first_seen,
                    MAX(timestamp) as last_seen,
                    GROUP_CONCAT(DISTINCT strftime('%Y-%m', timestamp)) as months
                   FROM transactions
                   WHERE owner IN (?, 'shared')
                     AND timestamp > datetime('now', '-6 months')
                   GROUP BY merchant, amount
                   HAVING charge_count >= 2
                   ORDER BY charge_count DESC""",
                (user_id,)
            )
            
            patterns = []
            for row in cursor:
                months = row['months'].split(',') if row['months'] else []
                
                # Determine frequency
                if len(months) >= 6:
                    frequency = 'monthly'
                elif len(months) >= 2:
                    frequency = 'quarterly'
                else:
                    frequency = 'unknown'
                
                # Check if already tracked
                sub_check = conn.execute(
                    "SELECT id FROM subscriptions WHERE merchant = ? AND amount = ?",
                    (row['merchant'], row['amount'])
                ).fetchone()
                
                if not sub_check:
                    patterns.append({
                        'merchant': row['merchant'],
                        'amount': row['amount'],
                        'frequency': frequency,
                        'charge_count': row['charge_count'],
                        'confidence': min(row['charge_count'] / 6, 1.0),
                        'suggested': True
                    })
        
        return patterns
    
    def add_subscription(self, data: Dict, user_id: str) -> Dict:
        """Add a subscription to tracking"""
        sub_id = f"sub_{generate_uuid()}"
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO subscriptions
                   (id, owner, merchant, amount, frequency, next_payment, 
                    category, is_essential, cancellation_url, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    sub_id,
                    data.get('owner', user_id),
                    data['merchant'],
                    data['amount'],
                    data.get('frequency', 'monthly'),
                    data.get('next_payment'),
                    data.get('category', 'lifestyle'),
                    data.get('is_essential', False),
                    data.get('cancellation_url'),
                    'active'
                )
            )
        
        log_audit(user_id, 'bag', 'create', 'subscription', sub_id, data)
        
        return {'id': sub_id, 'status': 'created'}
    
    # ========== BUDGET ==========
    
    def create_budget(self, data: Dict, user_id: str) -> Dict:
        """Create a budget"""
        budget_id = f"bud_{generate_uuid()}"
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO budgets
                   (id, owner, name, category, amount, period, start_date, end_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    budget_id,
                    data.get('owner', user_id),
                    data['name'],
                    data.get('category', 'all'),
                    data['amount'],
                    data.get('period', 'monthly'),
                    data.get('start_date', datetime.now().isoformat()),
                    data.get('end_date')
                )
            )
        
        return {'id': budget_id, 'status': 'created'}
    
    def get_budget_status(self, budget_id: str) -> Dict:
        """Get current spend vs budget"""
        with get_db() as conn:
            budget = conn.execute(
                "SELECT * FROM budgets WHERE id = ?", (budget_id,)
            ).fetchone()
            
            if not budget:
                return {'error': 'Budget not found'}
            
            # Calculate spent this period
            spent = conn.execute(
                """SELECT COALESCE(SUM(amount), 0) as spent
                   FROM transactions
                   WHERE owner = ?
                     AND (category = ? OR ? = 'all')
                     AND timestamp >= datetime('now', 'start of month')""",
                (budget['owner'], budget['category'], budget['category'])
            ).fetchone()['spent']
            
            remaining = budget['amount'] - spent
            
            return {
                'budget_id': budget_id,
                'name': budget['name'],
                'amount': budget['amount'],
                'spent': spent,
                'remaining': remaining,
                'percent_used': round((spent / budget['amount']) * 100, 1),
                'status': 'over' if remaining < 0 else 
                         'warning' if remaining < budget['amount'] * 0.2 else 'ok'
            }
    
    # ========== RECEIPT OCR ==========

    def process_receipt(self, image_path: str, user_id: str, backend: str = 'paddleocr') -> Dict:
        """
        Process receipt image through OCR.

        Supports multiple backends:
        - paddleocr: Self-hosted, free, fast (default)
        - easyocr: Self-hosted service, free
        - openai: Cloud API, accurate, costs money

        Args:
            image_path: Path to receipt image file
            user_id: User ID creating the transaction
            backend: OCR backend to use ('paddleocr', 'easyocr', 'openai')

        Returns:
            Dict with OCR results and parsed transaction data
        """
        try:
            # Initialize OCR processor if not already done
            if self.ocr_processor is None or self.ocr_processor.backend != backend:
                self.ocr_processor = OCRProcessor(backend=backend)

            # Extract structured data from receipt
            result = self.ocr_processor.extract_structured_data(image_path)

            if not result.get("success"):
                return {
                    'status': 'error',
                    'error': result.get("error", "OCR extraction failed"),
                    'image_path': image_path
                }

            # Parse the structured response
            raw_text = result.get("text", "")

            # Parse transaction data from OCR text
            transaction_data = self._parse_ocr_receipt(raw_text)

            # Add metadata
            transaction_data["image_path"] = image_path
            transaction_data["ocr_timestamp"] = datetime.now().isoformat()
            transaction_data["backend"] = backend

            # Calculate confidence
            confidence = self._calculate_ocr_confidence(transaction_data)

            logger.info(f"Receipt processed: {transaction_data.get('merchant', 'unknown')}, amount={transaction_data.get('total', 0)}, confidence={confidence}")

            return {
                'status': 'success',
                'transaction_data': transaction_data,
                'raw_text': raw_text,
                'confidence': confidence,
                'backend': backend,
                'usage': result.get("usage", {})
            }

        except FileNotFoundError as e:
            return {
                'status': 'error',
                'error': f"Image file not found: {str(e)}",
                'image_path': image_path
            }
        except Exception as e:
            logger.error(f"Error processing receipt: {e}")
            return {
                'status': 'error',
                'error': f"Unexpected error: {str(e)}",
                'image_path': image_path
            }

    def _parse_ocr_receipt(self, raw_text: str) -> Dict:
        """
        Parse OCR text to extract receipt information.

        Args:
            raw_text: Raw OCR text from receipt

        Returns:
            Dict with parsed transaction data
        """
        # Initialize result
        transaction_data = {
            'merchant': None,
            'date': None,
            'items': [],
            'subtotal': None,
            'tax': None,
            'total': None,
            'payment_method': None
        }

        # Try to parse JSON from text (if AI-structured)
        try:
            import json
            # Look for JSON object in text
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                # Update transaction_data with parsed values
                transaction_data.update(parsed)
                return transaction_data
        except Exception:
            pass  # Continue with regex parsing

        # Regex-based parsing (fallback)
        lines = raw_text.split('\n')

        for line in lines:
            # Extract merchant (first few lines, usually store name)
            if not transaction_data['merchant'] and len(line) > 3 and len(line) < 50:
                # Check if it's not a price or date
                if not re.search(r'\d+\.\d{2}', line) and not re.search(r'\d{4}-\d{2}-\d{2}', line):
                    transaction_data['merchant'] = line.strip()
                    continue

            # Extract date
            date_match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})', line)
            if date_match and not transaction_data['date']:
                transaction_data['date'] = date_match.group(1)
                continue

            # Extract total (look for "TOTAL", "TOTAL:", "JUMLAH", etc.)
            if re.search(r'(TOTAL|Total|JUMLAH|SUM)', line, re.IGNORECASE):
                total_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})', line)
                if total_match:
                    # Clean up number format
                    total_str = total_match.group(1).replace(',', '').replace('.', '')
                    if len(total_str) > 2:
                        total_str = total_str[:-2] + '.' + total_str[-2:]
                    transaction_data['total'] = float(total_str)
                    continue

            # Extract subtotal
            if re.search(r'(SUBTOTAL|Subtotal)', line, re.IGNORECASE):
                subtotal_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})', line)
                if subtotal_match:
                    subtotal_str = subtotal_match.group(1).replace(',', '').replace('.', '')
                    if len(subtotal_str) > 2:
                        subtotal_str = subtotal_str[:-2] + '.' + subtotal_str[-2:]
                    transaction_data['subtotal'] = float(subtotal_str)
                    continue

            # Extract tax
            if re.search(r'(TAX|Tax|VAT|PPN)', line, re.IGNORECASE):
                tax_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})', line)
                if tax_match:
                    tax_str = tax_match.group(1).replace(',', '').replace('.', '')
                    if len(tax_str) > 2:
                        tax_str = tax_str[:-2] + '.' + tax_str[-2:]
                    transaction_data['tax'] = float(tax_str)
                    continue

            # Extract line items (pattern: name + price)
            item_match = re.match(r'(.+?)\s+(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})', line)
            if item_match:
                item_name = item_match.group(1).strip()
                price_str = item_match.group(2).replace(',', '').replace('.', '')
                if len(price_str) > 2:
                    price_str = price_str[:-2] + '.' + price_str[-2:]
                price = float(price_str)

                if item_name and price > 0:
                    transaction_data['items'].append({
                        'name': item_name,
                        'price': price,
                        'quantity': 1  # Default to 1
                    })

        return transaction_data

    def _calculate_ocr_confidence(self, transaction_data: Dict) -> float:
        """
        Calculate confidence score for OCR extraction.

        Args:
            transaction_data: Parsed transaction data

        Returns:
            Confidence score (0.0 - 1.0)
        """
        score = 0.0
        max_score = 4.0  # Total possible score

        # Merchant found
        if transaction_data.get('merchant'):
            score += 1.0

        # Date found
        if transaction_data.get('date'):
            score += 1.0

        # Total found
        if transaction_data.get('total'):
            score += 1.0

        # Items found
        if transaction_data.get('items') and len(transaction_data['items']) > 0:
            score += 1.0

        # Bonus: subtotal and tax match
        subtotal = transaction_data.get('subtotal')
        tax = transaction_data.get('tax')
        total = transaction_data.get('total')
        if subtotal and tax and total:
            expected_total = subtotal + tax
            if abs(total - expected_total) < 0.01:  # Within 1 cent
                score += 0.5
                max_score = 4.5

        return round(score / max_score, 2)

    # ========== REAL OCR IMPLEMENTATION ==========

    async def ingest_receipt(self, image_path: str, ocr_api_key: Optional[str] = None, user_id: str = 'faza') -> Dict[str, Any]:
        """
        Ingest a receipt image using OCR to extract transaction data.
        
        Args:
            image_path: Path to receipt image file (JPEG, PNG, etc.)
            ocr_api_key: Optional OpenAI API key for OCR. If None, uses OPENAI_API_KEY env var.
            user_id: User ID creating the transaction.
            
        Returns:
            Dict with:
            - success: bool
            - transaction_data: dict with merchant, date, items, amounts
            - raw_text: str (full OCR text)
            - confidence: float (0-1)
            - error: str (if failed)
            
        Example:
            result = await ingest_receipt("/path/to/receipt.jpg")
            if result["success"]:
                merchant = result["transaction_data"]["merchant"]
                total = result["transaction_data"]["total"]
        """
        try:
            # Initialize OCR processor
            ocr = OCRProcessor(api_key=ocr_api_key)
            
            # Extract structured data from receipt
            result = ocr.extract_structured_data(image_path)
            
            if not result.get("success"):
                return {
                    "success": False,
                    "error": result.get("error", "OCR extraction failed"),
                    "image_path": image_path
                }
            
            # Parse the structured response
            raw_text = result["text"]
            
            # Try to extract JSON from response
            transaction_data = _parse_ocr_response(raw_text)
            
            # Add metadata
            transaction_data["image_path"] = image_path
            transaction_data["ocr_timestamp"] = datetime.utcnow().isoformat()
            
            return {
                "success": True,
                "transaction_data": transaction_data,
                "raw_text": raw_text,
                "confidence": _calculate_confidence(transaction_data),
                "usage": result.get("usage", {})
            }
            
        except FileNotFoundError as e:
            return {
                "success": False,
                "error": f"Image file not found: {str(e)}",
                "image_path": image_path
            }
        except ValueError as e:
            return {
                "success": False,
                "error": f"OCR configuration error: {str(e)}",
                "image_path": image_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "image_path": image_path
            }


def _extract_price(text: str) -> Optional[float]:
    """
    Extract price from text, supporting multiple currency formats.

    Supports:
    - $14.99, $1,234.56
    - Rp 14.500, Rp 1.234.567 (Indonesian format with dots as thousands)
    - 14.99, 14,99 (European format)

    Args:
        text: Text containing a price.

    Returns:
        Price as float, or None if not found.
    """
    if not text:
        return None

    # Try Indonesian format first: Rp XX.XXX or Rp X.XXX.XXX
    # Note: Indonesian uses dot as thousands separator (e.g., "Rp 88.000" = 88000)
    rp_match = re.search(r'Rp\s*([\d\.,]+)', text)
    if rp_match:
        amount_str = rp_match.group(1)
        # Remove all dots (thousands separators) to get the raw number
        amount_str = amount_str.replace('.', '')
        # Replace comma with dot (for decimal separator)
        amount_str = amount_str.replace(',', '.')
        try:
            return float(amount_str)
        except ValueError:
            pass

    # Try standard USD/EUR format: $XX.XX or XX.XX
    # Match: $14.99, 14.99, 1,234.56, etc.
    # Use word boundary and ensure we don't match Indonesian thousands
    if 'Rp' not in text:  # Only apply if not Indonesian format
        # Check if this looks like a decimal (has cents)
        decimal_match = re.search(r'[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        if decimal_match:
            amount_str = decimal_match.group(1).replace(',', '')
            try:
                return float(amount_str)
            except ValueError:
                pass

    # Try plain number
    plain_match = re.search(r'\b(\d+(?:\.\d+)?)\b', text)
    if plain_match:
        try:
            return float(plain_match.group(1))
        except ValueError:
            pass

    return None


def _parse_ocr_response(raw_text: str) -> Dict[str, Any]:
    """
    Parse OCR text response into structured transaction data.
    
    Args:
        raw_text: Raw text from OCR API.
        
    Returns:
        Dict with transaction fields.
    """
    # Try to extract JSON from response
    try:
        # Look for JSON block in markdown code fences
        if "```json" in raw_text:
            json_start = raw_text.find("```json") + 7
            json_end = raw_text.find("```", json_start)
            json_str = raw_text[json_start:json_end].strip()
            return json.loads(json_str)
        elif "```" in raw_text:
            json_start = raw_text.find("```") + 3
            json_end = raw_text.find("```", json_start)
            json_str = raw_text[json_start:json_end].strip()
            return json.loads(json_str)
        else:
            # Try parsing entire response as JSON
            return json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: extract key-value pairs using regex
        return _extract_fallback_data(raw_text)


def _extract_fallback_data(text: str) -> Dict[str, Any]:
    """
    Fallback extraction when JSON parsing fails.

    Enhanced to handle PaddleOCR output format.

    Args:
        text: Raw OCR text (newline-separated lines).

    Returns:
        Dict with basic extracted fields.
    """
    data = {
        "merchant": None,
        "date": None,
        "items": [],
        "subtotal": None,
        "tax": None,
        "total": None,
        "payment_method": None
    }

    # Split text into lines
    lines = text.strip().split('\n') if text else []
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return data

    # Extract merchant (usually the first line that's not a date)
    for line in lines:
        # Skip date-like lines
        if re.match(r'^\d{4}-\d{2}-\d{2}', line) or re.match(r'^\d{2}/\d{2}/\d{2,4}', line):
            continue
        # Skip "TOTAL" or similar keywords
        if line.upper() in ['TOTAL', 'SUBTOTAL', 'TAX', 'GRAND TOTAL']:
            continue
        # First meaningful line is likely the merchant
        data["merchant"] = line
        break

    # Extract items, subtotal, tax, and total
    # Pattern: "1. ITEM NAME" followed by price
    # Supports: $14.99, Rp 14.500, 14.99, etc.
    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this line looks like an item (starts with number + dot)
        item_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if item_match:
            item_name = item_match.group(2)
            # Look ahead for price on next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # Check if next line is a price (supports $XX.XX, Rp XX.XXX, XX.XXX)
                price = _extract_price(next_line)
                if price is not None:
                    # Skip if it's a total line
                    if next_line.upper() not in ['SUBTOTAL', 'TOTAL', 'TAX', 'JUMLAH']:
                        data["items"].append({
                            "name": item_name,
                            "quantity": int(item_match.group(1)),
                            "price": price
                        })
                        i += 2
                        continue

        # Check for totals (keywords followed by amount)
        if line.upper() in ['SUBTOTAL', 'SUM', 'JUMLAH']:
            if i + 1 < len(lines):
                price = _extract_price(lines[i + 1])
                if price is not None:
                    data["subtotal"] = price

        elif line.upper() in ['TAX', 'VAT', 'TAX (10%)', 'TAX (10%)', 'PPN', 'PPN 11%']:
            if i + 1 < len(lines):
                price = _extract_price(lines[i + 1])
                if price is not None:
                    data["tax"] = price

        elif line.upper() in ['TOTAL', 'GRAND TOTAL', 'AMOUNT']:
            if i + 1 < len(lines):
                price = _extract_price(lines[i + 1])
                if price is not None:
                    data["total"] = price

        # Extract date (common formats)
        if not data.get("date"):
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})',  # 2026-02-18 10:30
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
            ]
            for pattern in date_patterns:
                match = re.search(pattern, line)
                if match:
                    data["date"] = match.group(1)
                    break

        i += 1

    # If we still don't have a total, look for the largest amount
    if not data.get("total"):
        # Try to extract all prices and get the largest
        all_prices = []
        for line in lines:
            price = _extract_price(line)
            if price is not None and price > 0:
                all_prices.append(price)

        if all_prices:
            # The largest price is usually the total
            data["total"] = max(all_prices)

    return data


def _calculate_confidence(transaction_data: Dict[str, Any]) -> float:
    """
    Calculate confidence score based on completeness of extracted data.

    Args:
        transaction_data: Extracted transaction data.

    Returns:
        Confidence score 0.0 to 1.0.
    """
    required_fields = ["merchant", "date", "total"]
    optional_fields = ["items", "subtotal", "tax", "payment_method"]

    required_score = sum(1 for field in required_fields if transaction_data.get(field))
    optional_score = sum(1 for field in optional_fields if transaction_data.get(field))

    # Additional points for having items
    items_bonus = 0.2 if transaction_data.get("items") and len(transaction_data["items"]) > 0 else 0

    # Calculate base confidence from required fields (max 0.6)
    required_confidence = (required_score / len(required_fields)) * 0.6

    # Add optional fields bonus (max 0.2)
    optional_confidence = (optional_score / len(optional_fields)) * 0.2

    # Total confidence
    confidence = required_confidence + optional_confidence + items_bonus

    return min(confidence, 1.0)


# Transaction classifier
def classify_transaction(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify a transaction into spending categories and subcategories.
    
    Uses merchant name, items, and amount patterns to predict:
    - Category (e.g., Food, Transportation, Shopping)
    - Subcategory (e.g., Groceries, Restaurant, Gas)
    - Is_discretionary (bool)
    - Recurrence_type (one_time, weekly, monthly, etc.)
    
    Args:
        transaction_data: Dict with merchant, items, total, etc.
        
    Returns:
        Dict with classification results.
        
    Example:
        classification = classify_transaction({
            "merchant": "Whole Foods",
            "items": [{"name": "Milk"}, {"name": "Bread"}],
            "total": 45.67
        })
        # Returns: {"category": "Food", "subcategory": "Groceries", ...}
    """
    merchant = transaction_data.get("merchant", "").lower()
    items = transaction_data.get("items", [])
    total = transaction_data.get("total", 0)
    
    # Define merchant patterns and rules
    category_rules = _get_category_rules()
    
    # Check merchant name first
    for rule in category_rules:
        if any(pattern in merchant for pattern in rule["merchant_patterns"]):
            return {
                "category": rule["category"],
                "subcategory": rule["subcategory"],
                "is_discretionary": rule["is_discretionary"],
                "recurrence_type": rule["recurrence_type"],
                "confidence": "high"
            }
    
    # Fallback: analyze items
    if items:
        return _classify_by_items(items, total)
    
    # Final fallback: amount-based heuristics
    return _classify_by_amount(merchant, total)


def _get_category_rules() -> List[Dict[str, Any]]:
    """
    Get merchant pattern classification rules.
    
    Supports:
    - US/EU merchants (Whole Foods, Amazon, Netflix, etc.)
    - Indonesian merchants (GoPay, Grab, Tokopedia, etc.)
    
    Returns:
        List of classification rule dicts.
    """
    return [
        # ========== US/EU MERCHANTS ==========
        {
            "merchant_patterns": ["whole foods", "trader joe", "safeway", "kroger", "aldi", "costco"],
            "category": "Food",
            "subcategory": "Groceries",
            "is_discretionary": False,
            "recurrence_type": "weekly"
        },
        {
            "merchant_patterns": ["mcdonald", "burger king", "wendy", "taco bell", "chipotle", "subway"],
            "category": "Food",
            "subcategory": "Restaurant",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        {
            "merchant_patterns": ["shell", "chevron", "exxon", "bp", "gas station"],
            "category": "Transportation",
            "subcategory": "Fuel",
            "is_discretionary": False,
            "recurrence_type": "weekly"
        },
        {
            "merchant_patterns": ["amazon", "walmart", "target", "best buy"],
            "category": "Shopping",
            "subcategory": "General",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        {
            "merchant_patterns": ["netflix", "spotify", "hulu", "disney", "apple music"],
            "category": "Entertainment",
            "subcategory": "Streaming",
            "is_discretionary": True,
            "recurrence_type": "monthly"
        },
        {
            "merchant_patterns": ["gym", "fitness", "la fitness", "equinox"],
            "category": "Health",
            "subcategory": "Fitness",
            "is_discretionary": True,
            "recurrence_type": "monthly"
        },
        {
            "merchant_patterns": ["pharmacy", "walgreens", "cvs", "rite aid"],
            "category": "Health",
            "subcategory": "Pharmacy",
            "is_discretionary": False,
            "recurrence_type": "one_time"
        },
        # ========== INDONESIAN MERCHANTS ==========
        # E-Wallets
        {
            "merchant_patterns": ["gopay", "go-pay", "dompet anak bangsa"],
            "category": "Finance",
            "subcategory": "E-Wallet",
            "is_discretionary": True,
            "recurrence_type": "weekly"
        },
        {
            "merchant_patterns": ["dana", "dana id", "ovo", "ovoid", "linkaja", "shopeepay"],
            "category": "Finance",
            "subcategory": "E-Wallet",
            "is_discretionary": True,
            "recurrence_type": "weekly"
        },
        # Transportation
        {
            "merchant_patterns": ["grab", "grab trans", "grabfood", "grab bike"],
            "category": "Transportation",
            "subcategory": "Ride Sharing",
            "is_discretionary": True,
            "recurrence_type": "daily"
        },
        {
            "merchant_patterns": ["gojek", "go-jek", "go ride", "go food", "go-send"],
            "category": "Transportation",
            "subcategory": "Ride Sharing",
            "is_discretionary": True,
            "recurrence_type": "daily"
        },
        # Marketplaces
        {
            "merchant_patterns": ["tokopedia", "tokped", "toko"],
            "category": "Shopping",
            "subcategory": "Online Marketplace",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        {
            "merchant_patterns": ["shopee", "shopee indonesia", "shopee pay"],
            "category": "Shopping",
            "subcategory": "Online Marketplace",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        {
            "merchant_patterns": ["lazada", "bukalapak", "blibli", "jd.id"],
            "category": "Shopping",
            "subcategory": "Online Marketplace",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        # Travel
        {
            "merchant_patterns": ["traveloka", "tiket.com", "agoda", "booking.com", "doku agoda"],
            "category": "Travel",
            "subcategory": "Booking",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        # Convenience Stores / Groceries
        {
            "merchant_patterns": ["indomaret", "idm indomaret", "alfamart", "alfamidi", "circle k"],
            "category": "Food",
            "subcategory": "Groceries",
            "is_discretionary": False,
            "recurrence_type": "weekly"
        },
        # Food & Beverage
        {
            "merchant_patterns": ["warung", "restoran", "resto", "nasi ", "bakmie", "bakso", "sate", "ayam", "kopi", "es teh"],
            "category": "Food",
            "subcategory": "Restaurant",
            "is_discretionary": True,
            "recurrence_type": "daily"
        },
        # Banking
        {
            "merchant_patterns": ["bca", "mandiri", "bni", "bri", "biaya adm", "admin fee"],
            "category": "Finance",
            "subcategory": "Bank Fees",
            "is_discretionary": False,
            "recurrence_type": "monthly"
        },
        {
            "merchant_patterns": ["bi-fast", "bifast", "switching", "kliring"],
            "category": "Finance",
            "subcategory": "Transfer",
            "is_discretionary": False,
            "recurrence_type": "one_time"
        },
        # QRIS Payments
        {
            "merchant_patterns": ["qris", "qr payment", "qr 0", "transaksi qr"],
            "category": "Payment",
            "subcategory": "QRIS",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        # ATM/Cash
        {
            "merchant_patterns": ["tarikan atm", "tarik tunai", "atm withdrawal"],
            "category": "Finance",
            "subcategory": "Cash Withdrawal",
            "is_discretionary": True,
            "recurrence_type": "weekly"
        },
        # Entertainment
        {
            "merchant_patterns": ["gwk", "garuda wisnu", "museum", "waterbom", "ancol"],
            "category": "Entertainment",
            "subcategory": "Attractions",
            "is_discretionary": True,
            "recurrence_type": "one_time"
        },
        {
            "merchant_patterns": ["netflix indonesia", "spotify indonesia", "youtube premium", "disney+ hotstar"],
            "category": "Entertainment",
            "subcategory": "Streaming",
            "is_discretionary": True,
            "recurrence_type": "monthly"
        },
        # Utilities
        {
            "merchant_patterns": ["pln", "listrik", "pdam", "telkom", "indihome", "xl axiata", "telkomsel", "three", "tri"],
            "category": "Utilities",
            "subcategory": "Bills",
            "is_discretionary": False,
            "recurrence_type": "monthly"
        }
    ]


def _classify_by_items(items: List[Dict[str, Any]], total: float) -> Dict[str, Any]:
    """
    Classify transaction based on purchased items.
    
    Args:
        items: List of item dicts with 'name' field.
        total: Total transaction amount.
        
    Returns:
        Classification dict.
    """
    item_names = " ".join([item.get("name", "").lower() for item in items])
    
    # Food items
    food_keywords = ["milk", "bread", "eggs", "cheese", "fruit", "vegetable", "meat", "chicken"]
    if any(keyword in item_names for keyword in food_keywords):
        return {
            "category": "Food",
            "subcategory": "Groceries",
            "is_discretionary": False,
            "recurrence_type": "weekly",
            "confidence": "medium"
        }
    
    # Default
    return {
        "category": "Uncategorized",
        "subcategory": "Other",
        "is_discretionary": True,
        "recurrence_type": "one_time",
        "confidence": "low"
    }


def _classify_by_amount(merchant: str, total: float) -> Dict[str, Any]:
    """
    Classify transaction based on amount patterns.
    
    Args:
        merchant: Merchant name.
        total: Transaction amount.
        
    Returns:
        Classification dict.
    """
    # Small frequent transactions: likely daily spending
    if total < 10:
        return {
            "category": "Uncategorized",
            "subcategory": "Small Purchase",
            "is_discretionary": True,
            "recurrence_type": "one_time",
            "confidence": "low"
        }
    
    # Monthly subscription range
    if 9.99 <= total <= 29.99:
        return {
            "category": "Uncategorized",
            "subcategory": "Possible Subscription",
            "is_discretionary": True,
            "recurrence_type": "monthly",
            "confidence": "low"
        }
    
    # Default
    return {
        "category": "Uncategorized",
        "subcategory": "Other",
        "is_discretionary": True,
        "recurrence_type": "one_time",
        "confidence": "low"
    }
