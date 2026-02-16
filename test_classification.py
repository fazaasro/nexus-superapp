#!/usr/bin/env python3
"""
Test script for transaction classification (does not require OpenAI API).
Run with: python3 test_classification.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def test_transaction_classification():
    """Test transaction classification with sample data."""
    print("\n" + "="*60)
    print("NEXUS BAG MODULE - TRANSACTION CLASSIFICATION TESTS")
    print("="*60)

    # Import here to avoid dependency issues
    from modules.bag.service import (
        classify_transaction,
        _get_category_rules,
        _classify_by_items,
        _classify_by_amount,
        _extract_fallback_data,
        _calculate_confidence
    )

    test_cases = [
        {
            "name": "Grocery store",
            "data": {
                "merchant": "Whole Foods Market",
                "date": "2025-02-15",
                "items": [
                    {"name": "Organic Milk", "quantity": 1, "price": 5.99},
                    {"name": "Sourdough Bread", "quantity": 1, "price": 4.50}
                ],
                "total": 45.67
            },
            "expected": {"category": "Food", "subcategory": "Groceries"}
        },
        {
            "name": "Restaurant",
            "data": {
                "merchant": "Chipotle Mexican Grill",
                "date": "2025-02-15",
                "items": [
                    {"name": "Burrito Bowl", "quantity": 1, "price": 9.85}
                ],
                "total": 12.45
            },
            "expected": {"category": "Food", "subcategory": "Restaurant"}
        },
        {
            "name": "Gas station",
            "data": {
                "merchant": "Shell Gas Station",
                "date": "2025-02-15",
                "items": [],
                "total": 52.30
            },
            "expected": {"category": "Transportation", "subcategory": "Fuel"}
        },
        {
            "name": "Streaming service",
            "data": {
                "merchant": "Netflix",
                "date": "2025-02-15",
                "items": [],
                "total": 15.99
            },
            "expected": {"category": "Entertainment", "subcategory": "Streaming"}
        },
        {
            "name": "Gym membership",
            "data": {
                "merchant": "LA Fitness",
                "date": "2025-02-15",
                "items": [],
                "total": 49.99
            },
            "expected": {"category": "Health", "subcategory": "Fitness"}
        },
        {
            "name": "Amazon shopping",
            "data": {
                "merchant": "Amazon",
                "date": "2025-02-15",
                "items": [],
                "total": 79.99
            },
            "expected": {"category": "Shopping", "subcategory": "General"}
        }
    ]

    print("\nTEST 1: Transaction Classification")
    print("="*60)

    results = []
    passed = 0
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print(f"   Merchant: {test_case['data']['merchant']}")
        print(f"   Total: ${test_case['data']['total']}")

        classification = classify_transaction(test_case['data'])

        print(f"   → Category: {classification['category']}")
        print(f"   → Subcategory: {classification['subcategory']}")
        print(f"   → Discretionary: {classification['is_discretionary']}")
        print(f"   → Recurrence: {classification['recurrence_type']}")
        print(f"   → Confidence: {classification['confidence']}")

        # Validate
        expected = test_case.get('expected', {})
        if expected:
            actual_cat = classification['category']
            actual_sub = classification['subcategory']
            exp_cat = expected.get('category')
            exp_sub = expected.get('subcategory')

            if actual_cat == exp_cat and actual_sub == exp_sub:
                print(f"   ✅ PASSED")
                passed += 1
            else:
                print(f"   ❌ FAILED (expected {exp_cat}/{exp_sub}, got {actual_cat}/{actual_sub})")

        results.append({
            "name": test_case['name'],
            "classification": classification
        })

    print("\n" + "="*60)
    print("TEST 2: Fallback Data Extraction")
    print("="*60)

    # Test fallback extraction
    test_text = """
    WHOLE FOODS MARKET
    Date: 02/15/2025
    Items:
    Milk $4.99
    Bread $3.50
    Subtotal: $8.49
    Tax: $0.68
    Total: $9.17
    """

    extracted = _extract_fallback_data(test_text)
    print(f"\nExtracted from text:")
    print(f"  Total: ${extracted.get('total', 'N/A')}")
    print(f"  Subtotal: ${extracted.get('subtotal', 'N/A')}")
    print(f"  Tax: ${extracted.get('tax', 'N/A')}")
    print(f"  Date: {extracted.get('date', 'N/A')}")

    if extracted.get('total') == 9.17:
        print("  ✅ Fallback extraction PASSED")
        passed += 1
    else:
        print(f"  ❌ Fallback extraction FAILED")

    print("\n" + "="*60)
    print("TEST 3: Confidence Calculation")
    print("="*60)

    # Test confidence calculation
    complete_data = {
        "merchant": "Test Store",
        "date": "2025-02-15",
        "items": [{"name": "Item 1"}],
        "total": 10.00,
        "subtotal": 9.00,
        "tax": 1.00,
        "payment_method": "Credit Card"
    }

    incomplete_data = {
        "merchant": "Test Store",
        "total": 10.00
    }

    conf_complete = _calculate_confidence(complete_data)
    conf_incomplete = _calculate_confidence(incomplete_data)

    print(f"\nComplete data confidence: {conf_complete:.2f}")
    print(f"Incomplete data confidence: {conf_incomplete:.2f}")

    if conf_complete > conf_incomplete:
        print("  ✅ Confidence calculation PASSED")
        passed += 1
    else:
        print("  ❌ Confidence calculation FAILED")

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    total_tests = len(test_cases) + 2  # classification + fallback + confidence
    print(f"Score: {passed}/{total_tests} tests passed")

    if passed == total_tests:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(test_transaction_classification())
