"""
Module 1: The Bag (Finance)
Receipt OCR, Classification, Split Logic, Runway Calculation
"""
import json
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
from pathlib import Path

from core.database import get_db, generate_uuid, log_audit


class BagModule:
    """Finance management module"""
    
    CATEGORIES = ['survival', 'health', 'lifestyle', 'trash', 'income', 'investment']
    SPLIT_TYPES = ['solo', 'split_equal', 'split_custom']
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "levy.db"
    
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
        
        # Calculate runway
        if current_balance is None:
            # For demo, use a placeholder
            current_balance = 5000  # TODO: integrate with bank API
        
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
    
    # ========== RECEIPT OCR (Placeholder) ==========
    
    def process_receipt(self, image_path: str, user_id: str) -> Dict:
        """
        Process receipt image through OCR
        TODO: Integrate Tesseract or OpenAI Vision
        """
        # Placeholder implementation
        # Will be implemented with actual OCR
        
        return {
            'status': 'placeholder',
            'message': 'OCR integration pending',
            'image_path': image_path,
            'raw_text': None,
            'merchant': None,
            'amount': None
        }
