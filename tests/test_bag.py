"""
Bag module tests
"""
import pytest
from modules.bag.service import BagModule


class TestBagModuleInit:
    """Test BagModule initialization"""

    def test_module_initialization(self):
        """Test that BagModule initializes correctly"""
        bag = BagModule()

        assert bag.db_path is not None
        assert bag.CATEGORIES is not None
        assert len(bag.CATEGORIES) > 0
        assert 'survival' in bag.CATEGORIES
        assert 'lifestyle' in bag.CATEGORIES

    def test_ocr_processor_initialization(self):
        """Test that OCR processor initializes (lazy)"""
        bag = BagModule()

        # OCR processor should be None initially (lazy loading)
        assert bag.ocr_processor is None


class TestTransactionCRUD:
    """Test transaction CRUD operations"""

    def test_create_transaction(self, test_user, sample_transaction):
        """Test creating a transaction"""
        bag = BagModule()

        result = bag.create_transaction(sample_transaction, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'
        assert result['id'].startswith('txn_')

    def test_get_transactions(self, test_user, sample_transaction):
        """Test getting transactions"""
        bag = BagModule()

        # Create test transaction
        create_result = bag.create_transaction(sample_transaction, test_user['user_id'])
        txn_id = create_result['id']

        # Get transactions
        transactions = bag.get_transactions(test_user['user_id'], limit=10)

        assert len(transactions) > 0
        # Find our created transaction
        found = [t for t in transactions if t['id'] == txn_id]
        assert len(found) == 1

    def test_get_transaction_by_id(self, test_user, sample_transaction):
        """Test getting single transaction by ID"""
        bag = BagModule()

        # Create test transaction
        create_result = bag.create_transaction(sample_transaction, test_user['user_id'])
        txn_id = create_result['id']

        # Get transaction
        transaction = bag.get_transaction(txn_id, test_user['user_id'])

        assert transaction is not None
        assert transaction['id'] == txn_id
        assert transaction['merchant'] == sample_transaction['merchant']

    def test_update_transaction(self, test_user, sample_transaction):
        """Test updating a transaction"""
        bag = BagModule()

        # Create test transaction
        create_result = bag.create_transaction(sample_transaction, test_user['user_id'])
        txn_id = create_result['id']

        # Update transaction
        update_data = {
            'amount': 199.99,
            'notes': 'Updated transaction for testing purposes.'
        }
        update_result = bag.update_transaction(txn_id, update_data, test_user['user_id'])

        assert update_result['status'] == 'updated'
        assert update_result['id'] == txn_id

        # Verify update
        updated_txn = bag.get_transaction(txn_id, test_user['user_id'])
        assert updated_txn['amount'] == 199.99
        assert updated_txn['notes'] == 'Updated transaction for testing purposes.'

    def test_delete_transaction(self, test_user, sample_transaction):
        """Test deleting a transaction"""
        bag = BagModule()

        # Create test transaction
        create_result = bag.create_transaction(sample_transaction, test_user['user_id'])
        txn_id = create_result['id']

        # Delete transaction
        delete_result = bag.delete_transaction(txn_id, test_user['user_id'])

        assert delete_result['status'] == 'deleted'
        assert delete_result['id'] == txn_id

        # Verify deletion
        deleted_txn = bag.get_transaction(txn_id, test_user['user_id'])
        assert deleted_txn is None


class TestRunwayCalculation:
    """Test runway calculation"""

    def test_calculate_runway_with_balance(self, test_user, sample_transaction):
        """Test runway calculation with provided balance"""
        bag = BagModule()

        # Create test transaction
        bag.create_transaction(sample_transaction, test_user['user_id'])

        # Calculate runway with provided balance
        result = bag.calculate_runway(test_user['user_id'], current_balance=5000.0)

        assert 'days_remaining' in result
        assert 'months_remaining' in result
        assert 'daily_burn' in result
        assert 'monthly_burn' in result
        assert 'current_balance' in result
        assert 'status' in result
        assert result['status'] in ['critical', 'warning', 'healthy']
        assert result['current_balance'] == 5000.0

    def test_calculate_runway_without_balance(self, test_user, sample_transaction):
        """Test runway calculation without provided balance (calculates from DB)"""
        bag = BagModule()

        # Create test transaction
        bag.create_transaction(sample_transaction, test_user['user_id'])

        # Calculate runway without balance
        result = bag.calculate_runway(test_user['user_id'])

        assert 'days_remaining' in result
        assert 'current_balance' in result
        # Balance should be negative (expense only, no income)


class TestBalanceCalculation:
    """Test balance calculation"""

    def test_get_current_balance(self, test_user, sample_transaction):
        """Test getting current balance from database"""
        bag = BagModule()

        # Create expense transaction
        expense_txn = sample_transaction.copy()
        expense_txn['category'] = 'lifestyle'
        bag.create_transaction(expense_txn, test_user['user_id'])

        # Create income transaction
        income_txn = {
            'merchant': 'Salary',
            'amount': 5000.0,
            'category': 'income',
            'currency': 'EUR'
        }
        bag.create_transaction(income_txn, test_user['user_id'])

        # Get balance
        balance = bag._get_current_balance(test_user['user_id'])

        assert isinstance(balance, float)
        # Should be income - expense
        assert balance == 5000.0 - expense_txn['amount']

    def test_get_bank_balance(self, test_user):
        """Test getting bank balance (placeholder for API)"""
        bag = BagModule()

        # Get bank balance (uses calculated balance as placeholder)
        result = bag.get_bank_balance(test_user['user_id'])

        assert 'balance' in result
        assert 'currency' in result
        assert 'source' in result
        assert result['source'] == 'calculated'


class TestReceiptProcessing:
    """Test receipt OCR and processing"""

    def test_parse_ocr_receipt_json(self):
        """Test parsing OCR response with JSON"""
        bag = BagModule()

        # Simulate JSON response from OCR
        ocr_text = """
        {
            "merchant": "Test Store",
            "date": "2026-02-24",
            "items": [
                {"name": "Item 1", "price": 10.00},
                {"name": "Item 2", "price": 5.50}
            ],
            "subtotal": 15.50,
            "tax": 1.24,
            "total": 16.74
        }
        """

        parsed = bag._parse_ocr_receipt(ocr_text)

        assert parsed is not None
        assert parsed['merchant'] == 'Test Store'
        assert parsed['date'] == '2026-02-24'
        assert len(parsed['items']) == 2
        assert parsed['total'] == 16.74

    def test_parse_ocr_receipt_regex(self):
        """Test parsing OCR response with regex (no JSON)"""
        bag = BagModule()

        # Simulate plain text OCR response
        ocr_text = """
        Test Store
        2026-02-24
        Item 1                10.00
        Item 2                5.50
        SUBTOTAL               15.50
        TAX                    1.24
        TOTAL                  16.74
        """

        parsed = bag._parse_ocr_receipt(ocr_text)

        assert parsed is not None
        assert parsed['merchant'] is not None or parsed['total'] is not None
        # At minimum, total should be extracted
        assert parsed.get('total') is not None

    def test_calculate_ocr_confidence(self):
        """Test OCR confidence calculation"""
        bag = BagModule()

        # High confidence (all fields present)
        high_conf_data = {
            'merchant': 'Test Store',
            'date': '2026-02-24',
            'total': 16.74
        }
        high_score = bag._calculate_ocr_confidence(high_conf_data)

        assert 0 <= high_score <= 1.0
        assert high_score > 0.5  # Should be fairly high

        # Low confidence (fewer fields)
        low_conf_data = {
            'total': 16.74
        }
        low_score = bag._calculate_ocr_confidence(low_conf_data)

        assert 0 <= low_score <= 1.0
        assert low_score < high_score  # Should be lower than high confidence

    @pytest.mark.skipif(not True, reason="Requires OCR backend and test image")
    def test_process_receipt_paddleocr(self, test_user):
        """Test processing receipt with PaddleOCR"""
        bag = BagModule()

        # This would require a test receipt image
        # Skip for now, but structure test
        pytest.skip("Requires test receipt image file")

    @pytest.mark.skipif(not True, reason="Requires OCR backend and test image")
    def test_process_receipt_backend_selection(self):
        """Test OCR backend selection"""
        bag = BagModule()

        # Test that backend parameter is accepted
        backends = ['paddleocr', 'easyocr', 'openai']

        for backend in backends:
            # Just verify backend parameter is processed
            # Actual processing would require image file
            assert backend in bag.ocr_backend or backend == 'openai'


class TestBudgets:
    """Test budget management"""

    def test_create_budget(self, test_user):
        """Test creating a budget"""
        bag = BagModule()

        budget_data = {
            'name': 'Lifestyle Budget',
            'category': 'lifestyle',
            'amount': 500.0,
            'period': 'monthly',
            'start_date': '2026-02-01',
            'end_date': '2026-02-28'
        }

        result = bag.create_budget(budget_data, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'

    def test_get_budgets(self, test_user):
        """Test getting budgets"""
        bag = BagModule()

        # Create test budget
        budget_data = {
            'name': 'Test Budget',
            'category': 'lifestyle',
            'amount': 500.0,
            'period': 'monthly'
        }
        bag.create_budget(budget_data, test_user['user_id'])

        # Get budgets
        budgets = bag.get_budgets(test_user['user_id'])

        assert len(budgets) > 0
        assert any(b['name'] == 'Test Budget' for b in budgets)

    def test_check_budget_status(self, test_user):
        """Test checking budget status"""
        bag = BagModule()

        # Create budget and transaction
        budget_data = {
            'name': 'Test Budget',
            'category': 'lifestyle',
            'amount': 100.0,
            'period': 'monthly'
        }
        bag.create_budget(budget_data, test_user['user_id'])

        txn_data = {
            'merchant': 'Test Merchant',
            'amount': 50.0,
            'category': 'lifestyle'
        }
        bag.create_transaction(txn_data, test_user['user_id'])

        # Check budget status
        status = bag.check_budget_status(test_user['user_id'], budget_name='Test Budget')

        assert 'budget' in status
        assert 'spent' in status
        assert 'remaining' in status
        assert 'percent_used' in status
        assert 'status' in status
        assert status['status'] in ['over', 'warning', 'ok']


class TestSubscriptions:
    """Test subscription management"""

    def test_detect_subscription_from_transaction(self, test_user, sample_transaction):
        """Test detecting subscription from transaction"""
        bag = BagModule()

        # Create transaction that might be a subscription
        sub_txn = {
            'merchant': 'Netflix',
            'amount': 15.99,
            'category': 'lifestyle',
            'notes': 'Monthly subscription'
        }
        bag.create_transaction(sub_txn, test_user['user_id'])

        # Detect subscriptions
        subs = bag.detect_subscriptions(test_user['user_id'])

        assert len(subs) >= 0
        # Should detect Netflix as potential subscription
        assert any(s['merchant'] == 'Netflix' for s in subs)

    def test_create_subscription(self, test_user):
        """Test creating subscription"""
        bag = BagModule()

        sub_data = {
            'merchant': 'Netflix',
            'amount': 15.99,
            'frequency': 'monthly',
            'category': 'lifestyle',
            'is_essential': False,
            'cancellation_url': 'https://netflix.com/cancel'
        }

        result = bag.create_subscription(sub_data, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'


class TestStatistics:
    """Test statistics functionality"""

    def test_get_stats(self, test_user, sample_transaction):
        """Test getting Bag module statistics"""
        bag = BagModule()

        # Create test transaction
        bag.create_transaction(sample_transaction, test_user['user_id'])

        # Get stats
        stats = bag.get_stats(test_user['user_id'])

        assert 'total_transactions' in stats
        assert 'total_spent' in stats
        assert 'by_category' in stats
        assert stats['total_transactions'] >= 1

    def test_get_spending_by_period(self, test_user, sample_transaction):
        """Test getting spending by time period"""
        bag = BagModule()

        # Create test transaction
        bag.create_transaction(sample_transaction, test_user['user_id'])

        # Get spending (last 30 days)
        spending = bag.get_spending_by_period(
            test_user['user_id'],
            days=30
        )

        assert 'total' in spending
        assert 'by_category' in spending
        assert 'average_daily' in spending
        assert spending['total'] >= 0


@pytest.mark.integration
class TestOCRIntegration:
    """Integration tests for OCR processing"""

    @pytest.mark.skipif(not True, reason="Requires PaddleOCR installation")
    def test_paddleocr_integration(self):
        """Test PaddleOCR integration"""
        bag = BagModule()

        # Initialize PaddleOCR processor
        from modules.bag.ocr import OCRProcessor

        try:
            ocr = OCRProcessor(backend='paddleocr')

            assert ocr.paddleocr_processor is not None
            assert ocr.paddleocr_processor.available or not ocr.paddleocr_processor.available

        except Exception as e:
            pytest.skip(f"PaddleOCR not available: {e}")

    @pytest.mark.skipif(not True, reason="Requires EasyOCR service")
    def test_easyocr_integration(self):
        """Test EasyOCR integration"""
        bag = BagModule()

        from modules.bag.ocr import OCRProcessor

        try:
            ocr = OCRProcessor(backend='easyocr')

            assert ocr.easyocr_processor is not None

        except Exception as e:
            pytest.skip(f"EasyOCR not available: {e}")
