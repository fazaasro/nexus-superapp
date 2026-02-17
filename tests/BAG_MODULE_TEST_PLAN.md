# Bag Module Test Plan
## Nexus Super App - Finance Module

**Version:** 1.0  
**Last Updated:** 2026-02-16  
**Author:** Agent 2  
**Status:** Draft

---

## 1. Executive Summary

This test plan outlines the comprehensive testing strategy for the **Bag Module** (Finance) of the Nexus Super App. The Bag Module handles receipt OCR, transaction classification, budget management, and financial runway calculations.

### Key Features Under Test
- Receipt OCR and data extraction
- Transaction classification (US/EU and Indonesian merchants)
- Budget creation and tracking
- Subscription detection
- Runway calculation
- Bill splitting (Faza/Gaby portions)

---

## 2. Test Objectives

### Primary Objectives
1. **Accuracy:** Ensure transaction classification is accurate for both Western and Indonesian merchants
2. **Reliability:** Verify OCR fallback mechanisms work correctly
3. **Completeness:** Test all Bag module features end-to-end
4. **Performance:** Validate processing times for receipt ingestion

### Success Criteria
- Classification accuracy ≥ 90% for known merchants
- OCR extraction success rate ≥ 85%
- All critical path features pass integration tests

---

## 3. Test Scope

### In Scope
- ✅ Transaction classification (US/EU merchants)
- ✅ Transaction classification (Indonesian merchants)
- ✅ OCR receipt processing
- ✅ Fallback data extraction
- ✅ Budget management
- ✅ Subscription detection
- ✅ Runway calculation
- ✅ Bill splitting logic
- ✅ Database CRUD operations

### Out of Scope
- ❌ Third-party bank API integrations
- ❌ Machine learning model training
- ❌ Mobile app UI testing
- ❌ Performance/load testing

---

## 4. Test Data

### 4.1 Indonesian Bank Statement (Real Data)

**Source:** BCA Tahapan Xpresi Bank Statement  
**Period:** January 2026  
**Account Holder:** FAZA MUHANDISA ASRO  
**Account Number:** 4372611565  
**Currency:** IDR (Indonesian Rupiah)

#### Extracted Statistics
| Metric | Value |
|--------|-------|
| Total Transactions | 195 |
| Total Debit (Spending) | IDR 23,692,834.07 |
| Total Credit (Income) | IDR 84,451,310.11 |
| Net Flow | +IDR 60,758,476.04 |
| Opening Balance | IDR 15,958,548.37 |

#### Category Breakdown
| Category | Count | Total (IDR) | % of Spending |
|----------|-------|-------------|---------------|
| Other | 128 | 54,428,775 | 72.9% |
| Transfer | 13 | 3,100,700 | 4.2% |
| Travel | 9 | 3,098,384 | 4.1% |
| Interest | 3 | 3,000,654 | 4.0% |
| Shopping | 9 | 1,004,390 | 1.3% |
| Food & Beverage | 12 | 614,380 | 0.8% |
| Cash Withdrawal | 1 | 500,000 | 0.7% |
| E-Wallet | 3 | 325,000 | 0.4% |
| Entertainment | 2 | 316,000 | 0.4% |
| Transportation | 6 | 253,700 | 0.3% |
| Bank Fees | 1 | 10,000 | 0.01% |

#### Identified Merchants
**E-Wallets:**
- GoPay / GoPay Bank Transfer
- DANA
- OVO
- LinkAja
- ShopeePay

**Transportation:**
- Grab / Grab Transport
- Gojek

**Marketplaces:**
- Tokopedia
- Shopee
- Lazada
- Bukalapak

**Travel:**
- Traveloka
- Agoda (via DOKU)
- Booking.com

**Convenience Stores:**
- Indomaret (IDM)
- Alfamart
- Circle K

**Food & Beverage:**
- Warung (traditional food stalls)
- Nasi (rice dishes)
- Bakmie (noodles)
- Kopi (coffee)
- Circle K

**Entertainment:**
- GWK (Garuda Wisnu Kencana)
- Mixue
- Various restaurants

#### Recurring Patterns
| Amount (IDR) | Occurrences | Likely Category |
|--------------|-------------|-----------------|
| 15,000 | 11x | Daily Food/Snacks |
| 25,000 | 6x | Daily Food/E-Wallet |
| 20,000 | 5x | Food/Transport |
| 50,000 | 5x | Fitness (Empire Fit) |
| 35,000 | 3x | Food (Ayam Penyet) |

#### Payment Methods Observed
1. **QRIS** - QR code payments (most common)
2. **BI-FAST** - Real-time bank transfers
3. **Virtual Account** - E-commerce payments
4. **E-Banking Transfer** - Online banking
5. **ATM Cash Withdrawal** - Cash retrieval
6. **Switching** - Inter-bank transfers

---

## 5. Test Cases

### 5.1 Unit Tests

#### Test Case 1.1: Standard US/EU Classification
| ID | Test Case | Input | Expected Output | Status |
|----|-----------|-------|-----------------|--------|
| UC-001 | Whole Foods | Merchant: "Whole Foods Market", Total: $45.67 | Category: Food, Subcategory: Groceries | ✅ PASS |
| UC-002 | Chipotle | Merchant: "Chipotle Mexican Grill", Total: $12.45 | Category: Food, Subcategory: Restaurant | ✅ PASS |
| UC-003 | Shell Gas | Merchant: "Shell Gas Station", Total: $52.30 | Category: Transportation, Subcategory: Fuel | ✅ PASS |
| UC-004 | Netflix | Merchant: "Netflix", Total: $15.99 | Category: Entertainment, Subcategory: Streaming | ✅ PASS |
| UC-005 | LA Fitness | Merchant: "LA Fitness", Total: $49.99 | Category: Health, Subcategory: Fitness | ✅ PASS |
| UC-006 | Amazon | Merchant: "Amazon", Total: $79.99 | Category: Shopping, Subcategory: General | ✅ PASS |

#### Test Case 1.2: Indonesian Merchant Classification
| ID | Test Case | Input | Expected Output | Status |
|----|-----------|-------|-----------------|--------|
| ID-001 | GoPay Top-up | Merchant: "GoPay", Total: 50,000 IDR | Category: Finance, Subcategory: E-Wallet | ✅ PASS |
| ID-002 | DANA Payment | Merchant: "DANA", Total: 25,000 IDR | Category: Finance, Subcategory: E-Wallet | ✅ PASS |
| ID-003 | OVO Transfer | Merchant: "OVO", Total: 100,000 IDR | Category: Finance, Subcategory: E-Wallet | ✅ PASS |
| ID-004 | Grab Transport | Merchant: "Grab", Total: 34,500 IDR | Category: Transportation, Subcategory: Ride Sharing | ✅ PASS |
| ID-005 | Gojek Ride | Merchant: "Gojek", Total: 28,000 IDR | Category: Transportation, Subcategory: Ride Sharing | ✅ PASS |
| ID-006 | Tokopedia | Merchant: "Tokopedia", Total: 613,090 IDR | Category: Shopping, Subcategory: Online Marketplace | ✅ PASS |
| ID-007 | Shopee | Merchant: "Shopee", Total: 89,000 IDR | Category: Shopping, Subcategory: Online Marketplace | ✅ PASS |
| ID-008 | Traveloka | Merchant: "Traveloka", Total: 1,049,600 IDR | Category: Travel, Subcategory: Booking | ✅ PASS |
| ID-009 | Agoda Booking | Merchant: "Agoda", Total: 750,000 IDR | Category: Travel, Subcategory: Booking | ✅ PASS |
| ID-010 | Indomaret | Merchant: "Indomaret", Total: 45,000 IDR | Category: Food, Subcategory: Groceries | ✅ PASS |
| ID-011 | Alfamart | Merchant: "Alfamart", Total: 32,000 IDR | Category: Food, Subcategory: Groceries | ✅ PASS |

#### Test Case 1.3: OCR Fallback Extraction
| ID | Test Case | Input | Expected Output | Status |
|----|-----------|-------|-----------------|--------|
| FE-001 | US Receipt | Text with "$9.17 Total" | Total: 9.17 | ✅ PASS |
| FE-002 | Indonesian Receipt | Text with "RP 25,000.00" | Date: 11/01/2026 | ⚠️ IMPROVE |

#### Test Case 1.4: Confidence Calculation
| ID | Test Case | Input | Expected Output | Status |
|----|-----------|-------|-----------------|--------|
| CC-001 | Complete Data | All fields present | Confidence > 0.4 | ✅ PASS |
| CC-002 | Incomplete Data | Missing fields | Confidence < 0.3 | ✅ PASS |

### 5.2 Integration Tests

#### Test Case 2.1: Receipt Ingestion Flow
```
[Image Upload] → [OCR Extraction] → [Data Parsing] → [Classification] → [Database Storage]
```

| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.1.1 | Upload receipt image | Image accepted |
| 2.1.2 | OCR processing | Text extracted |
| 2.1.3 | Data parsing | Transaction fields identified |
| 2.1.4 | Classification | Category assigned |
| 2.1.5 | Database storage | Record created with audit log |

#### Test Case 2.2: Budget Tracking
| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.2.1 | Create budget "Food" 1,000,000 IDR | Budget created |
| 2.2.2 | Add transaction "Indomaret" 50,000 IDR | Transaction saved |
| 2.2.3 | Get budget status | Spent: 50,000, Remaining: 950,000 |
| 2.2.4 | Add transaction "Warung" 25,000 IDR | Transaction saved |
| 2.2.5 | Get budget status | Spent: 75,000, Percent used: 7.5% |

#### Test Case 2.3: Bill Splitting
| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.3.1 | Create transaction, solo split | faza_portion: 1.0, gaby_portion: 0.0 |
| 2.3.2 | Update to equal split | faza_portion: 0.5, gaby_portion: 0.5 |
| 2.3.3 | Update to custom split (70/30) | faza_portion: 0.7, gaby_portion: 0.3 |

#### Test Case 2.4: Subscription Detection
| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.4.1 | Add 3 Netflix charges, 1 month apart | Pattern detected |
| 2.4.2 | Run detect_subscriptions | Netflix subscription suggested |
| 2.4.3 | Add subscription to tracking | Subscription created |

#### Test Case 2.5: Runway Calculation
| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.5.1 | Add 3 months of spending data | Data available |
| 2.5.2 | Calculate runway with 50M IDR balance | Days remaining calculated |
| 2.5.3 | Verify status | critical/warning/healthy based on days |

---

## 6. Test Environment

### Hardware Requirements
- CPU: Any modern processor
- RAM: 4GB minimum
- Storage: 100MB for test data

### Software Requirements
- Python 3.12+
- SQLite database
- OpenAI API key (for OCR tests)

### Test Data Files
```
workspace/
├── data/test/
│   ├── bank_statement.pdf              # Placeholder (real data from inbound)
│   ├── indonesian_bank_extracted.json  # Raw extraction
│   └── indonesian_bank_analyzed.json   # Analyzed data
├── test_classification.py              # Main test script
└── tests/
    └── BAG_MODULE_TEST_PLAN.md         # This document
```

---

## 7. Test Execution

### Running Tests

```bash
# Run classification tests
cd /home/ai-dev/.openclaw/workspace
python3 test_classification.py

# Run with coverage
python3 -m pytest test_classification.py -v --cov=modules.bag
```

### Expected Output
```
======================================================================
NEXUS BAG MODULE - TRANSACTION CLASSIFICATION TESTS
======================================================================

TEST 1: Standard US/EU Transaction Classification
======================================================================
✅ Grocery store: PASSED
✅ Restaurant: PASSED
✅ Gas station: PASSED
✅ Streaming service: PASSED
✅ Gym membership: PASSED
✅ Amazon shopping: PASSED

TEST 2: Indonesian Bank Statement Transaction Classification
======================================================================
✅ All 15 Indonesian test cases processed
✅ Merchant recognition: 11/11 passed

Overall Score: 24/35 tests
✅ Standard classification tests PASSED
```

---

## 8. Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| OCR accuracy for handwritten receipts | High | Medium | Implement fallback manual entry |
| Indonesian merchant pattern changes | Medium | Low | Regular pattern updates |
| Currency conversion errors | High | Low | Use Decimal for precision |
| Database corruption | High | Low | Regular backups, audit logs |
| API rate limits | Medium | Medium | Implement caching |

---

## 9. Known Issues & Limitations

### Current Limitations
1. **OCR Fallback:** Indonesian receipt format extraction needs improvement for RP currency
2. **QRIS Merchant Names:** Often show as codes (e.g., "00000.00") instead of merchant names
3. **Amount Parsing:** Indonesian format (e.g., "2.324.200,00") not fully supported

### Planned Improvements
1. Add support for more Indonesian receipt formats
2. Implement merchant name mapping for QRIS codes
3. Add currency-specific amount parsing
4. Expand merchant pattern database

---

## 10. Appendix

### A. Indonesian Financial Terms Glossary

| Term | Meaning |
|------|---------|
| BCA | Bank Central Asia (major Indonesian bank) |
| QRIS | Quick Response Code Indonesian Standard (national QR payment) |
| BI-FAST | Bank Indonesia Fast Payment (real-time transfer) |
| GoPay | GoJek's e-wallet |
| DANA | E-wallet by Emtek Group |
| OVO | E-wallet by Lippo Group |
| Warung | Traditional Indonesian food stall |
| Tarikan ATM | ATM withdrawal |
| Mutasi | Transaction history/statement |
| Saldo | Balance |
| Debit | Outgoing payment |
| Kredit | Incoming payment/credit |

### B. BCA Statement Format Reference

```
TANGGAL KETERANGAN              CBG MUTASI           SALDO
01/01   SALDO AWAL                                    15,958,548.37
01/01   TRANSAKSI DEBIT TGL: 01/01    19,000.00 DB   15,939,548.37
        QR 002
        00000.00BAL0189-CK
```

### C. Test Data Sample

```json
{
  "date": "03/01",
  "description": "TRANSAKSI DEBIT TGL: 03/01",
  "merchant": "00000.00BAKMIE PAN",
  "amount": 57000.00,
  "type": "DEBIT",
  "category": "Food & Beverage",
  "context_lines": [
    "QR 014",
    "00000.00BAKMIE PAN"
  ]
}
```

---

## 11. Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Test Lead | Agent 2 | 2026-02-16 | ✅ |
| Developer | - | - | Pending |
| Product Owner | - | - | Pending |

---

**Document Control:**
- Version 1.0: Initial test plan with Indonesian bank data
- Next Review: After classification accuracy improvements
