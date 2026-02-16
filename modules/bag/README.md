# AAC System - Module 1: The Bag (Finance)

## Overview
Receipt OCR → Classification → Split Logic → Runway Calculation

## Components

### 1. Ingestion Pipeline
- **Input:** WhatsApp/Telegram photo upload
- **OCR:** Tesseract or OpenAI Vision
- **Output:** Raw JSON with merchant, items, total

### 2. AI Classifier
**Prompt Template:**
```
Analyze this receipt:
{raw_text}

Return JSON:
{
  "merchant": "store name",
  "category": "survival|health|lifestyle|trash",
  "impact_score": 1-5,
  "items": [...],
  "confidence": 0.0-1.0
}

Category definitions:
- survival: groceries, rent, utilities, transport
- health: gym, supplements, medical
- lifestyle: entertainment, dining out, hobbies
- trash: impulse buys, regret purchases

Impact Score:
1 = Essential, no regret
2 = Useful, good value
3 = Neutral, neither good nor bad
4 = Questionable, mild regret
5 = Regret, unnecessary
```

### 3. Split Bill Logic
```python
class SplitLogic:
    def calculate_split(self, transaction, split_type):
        if split_type == 'solo':
            return {'faza': 1.0, 'gaby': 0.0}
        elif split_type == 'split_equal':
            return {'faza': 0.5, 'gaby': 0.5}
        elif split_type == 'bali_fund':
            # Custom: Faza pays 60%, Gaby 40% for Bali trip
            return {'faza': 0.6, 'gaby': 0.4}
```

### 4. Runway Calculator
```python
def calculate_runway(user):
    """Days of survival remaining"""
    # Get monthly average spend
    avg_monthly = get_avg_spend(user, months=3)
    
    # Get current balance (manual input or bank API)
    balance = get_current_balance(user)
    
    # Calculate
    days = (balance / avg_monthly) * 30
    
    return {
        'days': round(days),
        'months': round(days / 30, 1),
        'burn_rate': avg_monthly,
        'projected_depletion': today + days
    }
```

## API Endpoints

```
POST /api/v1/bag/transactions
  - Upload receipt image
  - Returns classified transaction

GET /api/v1/bag/transactions
  - List transactions (with filters)

POST /api/v1/bag/transactions/{id}/split
  - Set split type

GET /api/v1/bag/runway
  - Get days of survival

GET /api/v1/bag/subscriptions
  - List detected subscriptions

POST /api/v1/bag/subscriptions/audit
  - Trigger subscription scan
```

## Data Model

See `database/schema.sql` - `transactions`, `budgets`, `subscriptions` tables.

## Implementation Plan

### Week 1: Foundation
- [ ] Create BagModule class
- [ ] OCR integration (Tesseract)
- [ ] Basic transaction storage

### Week 2: AI Classification
- [ ] OpenAI prompt engineering
- [ ] Category classifier
- [ ] Impact score calculator

### Week 3: Split & Runway
- [ ] Split bill logic
- [ ] Runway calculator
- [ ] Budget alerts

### Week 4: Subscriptions
- [ ] Recurring pattern detection
- [ ] Cancellation reminders
- [ ] Audit reports

## File Structure

```
modules/bag/
├── __init__.py
├── models.py          # Pydantic models
├── service.py         # Business logic
├── api.py            # FastAPI routes
├── classifier.py     # AI classification
├── ocr.py            # Receipt OCR
├── split_logic.py    # Bill splitting
└── runway.py         # Runway calculation
```
