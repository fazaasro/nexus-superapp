#!/usr/bin/env python3
"""
Test script for The Circle module (Social CRM).
Tests contact management, health logs, and check-ins.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.circle.service import CircleModule
from core.database import init_db


def test_contacts():
    """Test contact management."""
    print("\n" + "="*70)
    print("NEXUS CIRCLE MODULE - CONTACT MANAGEMENT TESTS")
    print("="*70)

    # Initialize database
    print("\n[1/5] Initializing database...")
    init_db()
    print("✅ Database initialized")

    circle = CircleModule()
    user_id = 'faza'

    # Test 1: Create contact
    print("\n[2/5] Creating contact...")
    contact_data = {
        'name': 'Sarah Johnson',
        'relationship': 'friend',
        'inner_circle': True,
        'phone': '+1-555-1234',
        'email': 'sarah@example.com',
        'telegram_handle': '@sarahj',
        'contact_frequency': 'monthly',
        'birthday': '1990-05-20',
        'important_dates': [
            {'date': '2026-05-20', 'description': 'Birthday - 36 years old'}
        ],
        'notes': 'Met at university, loves hiking'
    }
    
    result = circle.create_contact(contact_data, user_id)
    assert 'id' in result, f"Failed to create contact: {result}"
    contact_id = result['id']
    print(f"✅ Contact created: {contact_id}")

    # Test 2: Get contact
    print("\n[3/5] Retrieving contact...")
    contact = circle.get_contact(contact_id, user_id)
    assert contact is not None, "Contact not found"
    assert contact['name'] == 'Sarah Johnson', f"Name mismatch: {contact['name']}"
    assert contact['inner_circle'] == True, "Inner circle flag incorrect"
    print(f"✅ Contact retrieved: {contact['name']}")

    # Test 3: List contacts
    print("\n[4/5] Listing contacts...")
    contacts = circle.get_contacts(user_id)
    assert len(contacts) > 0, "No contacts found"
    assert contacts[0]['inner_circle'] == True, "Contact order incorrect"
    print(f"✅ Found {len(contacts)} contacts")

    # Test 4: Update contact
    print("\n[5/5] Updating contact...")
    update_data = {
        'notes': 'Met at university, loves hiking and camping'
    }
    result = circle.update_contact(contact_id, update_data, user_id)
    assert result['status'] == 'updated', f"Failed to update: {result}"
    print(f"✅ Contact updated")

    print("\n" + "="*70)
    print("ALL CONTACT TESTS PASSED ✅")
    print("="*70)


def test_health_logs():
    """Test health logging."""
    print("\n" + "="*70)
    print("NEXUS CIRCLE MODULE - HEALTH LOGGING TESTS")
    print("="*70)

    from core.database import init_db
    init_db()
    
    circle = CircleModule()

    # Test 1: Create health log
    print("\n[1/4] Creating health log...")
    health_data = {
        'owner': 'gaby',
        'symptom_type': 'reflux',
        'severity': 7,
        'triggers': ['spicy food', 'late dinner'],
        'location': 'home',
        'meal_before': 'Indian curry',
        'stress_level': 6,
        'sleep_quality': 5,
        'description': 'Burning sensation in chest after dinner',
        'remedy_tried': 'Tums',
        'remedy_effectiveness': 4
    }
    
    result = circle.create_health_log(health_data, logged_by='faza')
    assert 'id' in result, f"Failed to create health log: {result}"
    log_id = result['id']
    print(f"✅ Health log created: {log_id}")

    # Test 2: Get health logs
    print("\n[2/4] Listing health logs...")
    logs = circle.get_health_logs(user_id='faza', owner='gaby', days=30)
    assert len(logs) > 0, "No health logs found"
    assert logs[0]['symptom_type'] == 'reflux', "Symptom type mismatch"
    print(f"✅ Found {len(logs)} health logs")

    # Test 3: Analyze health
    print("\n[3/4] Analyzing health...")
    analysis = circle.analyze_health('gaby', 'reflux', days=30)
    assert 'episode_count' in analysis, "Analysis missing episode_count"
    assert 'avg_severity' in analysis, "Analysis missing avg_severity"
    assert 'common_triggers' in analysis, "Analysis missing common_triggers"
    print(f"✅ Health analysis: {analysis['episode_count']} episodes, "
          f"avg severity {analysis['avg_severity']}")
    print(f"   Common triggers: {[t['trigger'] for t in analysis['common_triggers']]}")

    # Test 4: Get health log
    print("\n[4/4] Retrieving single health log...")
    log = circle.get_health_log(log_id, user_id='faza')
    assert log is not None, "Health log not found"
    assert log['severity'] == 7, "Severity mismatch"
    print(f"✅ Health log retrieved: severity {log['severity']}")

    print("\n" + "="*70)
    print("ALL HEALTH LOG TESTS PASSED ✅")
    print("="*70)


def test_checkins():
    """Test relationship check-ins."""
    print("\n" + "="*70)
    print("NEXUS CIRCLE MODULE - CHECK-IN TESTS")
    print("="*70)

    from core.database import init_db
    init_db()
    
    circle = CircleModule()

    # Test 1: Create check-in
    print("\n[1/4] Creating check-in...")
    checkin_data = {
        'faza_mood': 7,
        'gaby_mood': 8,
        'relationship_vibe': 9,
        'topics_discussed': ['work', 'weekend plans', 'health'],
        'friction_points': None,
        'wins': 'Had a nice dinner together'
    }
    
    result = circle.create_checkin(checkin_data, user_id='faza')
    assert 'id' in result, f"Failed to create check-in: {result}"
    checkin_id = result['id']
    assert 'sentiment_score' in result, "Sentiment score missing"
    print(f"✅ Check-in created: {checkin_id}, sentiment: {result['sentiment_score']:.2f}")

    # Test 2: List check-ins
    print("\n[2/4] Listing check-ins...")
    checkins = circle.get_checkins(limit=50)
    assert len(checkins) > 0, "No check-ins found"
    print(f"✅ Found {len(checkins)} check-ins")

    # Test 3: Get trends
    print("\n[3/4] Getting check-in trends...")
    trends = circle.get_checkin_trends(days=30)
    assert 'faza_avg_mood' in trends, "Trends missing faza_avg_mood"
    assert 'gaby_avg_mood' in trends, "Trends missing gaby_avg_mood"
    assert 'relationship_avg_vibe' in trends, "Trends missing relationship_avg_vibe"
    assert 'trend' in trends, "Trends missing trend"
    print(f"✅ Trends: Faza {trends['faza_avg_mood']}, Gaby {trends['gaby_avg_mood']}, "
          f"Vibe {trends['relationship_avg_vibe']}, Trend: {trends['trend']}")
    if trends['insights']:
        for insight in trends['insights']:
            print(f"   - {insight}")

    # Test 4: Get reminders
    print("\n[4/4] Getting reminders...")
    reminders = circle.get_reminders(user_id='faza')
    assert 'contacts_to_ping' in reminders, "Reminders missing contacts_to_ping"
    assert 'upcoming_birthdays' in reminders, "Reminders missing upcoming_birthdays"
    assert 'health_alerts' in reminders, "Reminders missing health_alerts"
    assert 'relationship_alerts' in reminders, "Reminders missing relationship_alerts"
    print(f"✅ Reminders retrieved")
    print(f"   Contacts to ping: {len(reminders['contacts_to_ping'])}")
    print(f"   Upcoming birthdays: {len(reminders['upcoming_birthdays'])}")
    print(f"   Health alerts: {len(reminders['health_alerts'])}")
    print(f"   Relationship alerts: {len(reminders['relationship_alerts'])}")

    print("\n" + "="*70)
    print("ALL CHECK-IN TESTS PASSED ✅")
    print("="*70)


if __name__ == '__main__':
    try:
        test_contacts()
        test_health_logs()
        test_checkins()
        print("\n✅ All Circle module tests passed successfully!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
