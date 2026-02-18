#!/usr/bin/env python3
"""
Test script for The Vessel module (Health Tracking).
Tests Blueprint protocol, workouts, biometrics, and sobriety tracking.
"""
import sys
from pathlib import Path
from datetime import date

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.vessel.service import VesselModule
from core.database import init_db


def test_blueprint():
    """Test Blueprint protocol logging."""
    print("\n" + "="*70)
    print("NEXUS VESSEL MODULE - BLUEPRINT PROTOCOL TESTS")
    print("="*70)

    # Initialize database
    print("\n[1/4] Initializing database...")
    init_db()
    print("✅ Database initialized")

    vessel = VesselModule()
    user_id = 'faza'

    # Test 1: Log Blueprint
    print("\n[2/4] Logging Blueprint protocol...")
    blueprint_data = {
        'owner': 'faza',
        'date': date.today().isoformat(),
        'supplements_taken': True,
        'super_veggie_eaten': True,
        'nutty_pudding_eaten': True,
        'exercise_done': True,
        'supplement_list': [
            {'name': 'Vitamin D3', 'dosage': '5000 IU'},
            {'name': 'Omega-3', 'dosage': '2000 mg'},
            {'name': 'Magnesium', 'dosage': '400 mg'}
        ],
        'meals_logged': [
            {'meal': 'breakfast', 'description': 'Oatmeal with berries'},
            {'meal': 'lunch', 'description': 'Grilled chicken salad'}
        ],
        'water_intake_ml': 2500
    }
    
    result = vessel.log_blueprint(blueprint_data, user_id)
    assert 'id' in result, f"Failed to log Blueprint: {result}"
    assert result['compliance_score'] == 100, f"Expected 100% compliance, got {result['compliance_score']}"
    blueprint_id = result['id']
    print(f"✅ Blueprint logged: {blueprint_id}, compliance: {result['compliance_score']}%")

    # Test 2: Get Blueprint logs
    print("\n[3/4] Listing Blueprint logs...")
    logs = vessel.get_blueprint_logs(user_id, owner='faza', limit=10)
    assert len(logs) > 0, "No Blueprint logs found"
    assert logs[0]['compliance_score'] == 100, "Compliance score mismatch"
    print(f"✅ Found {len(logs)} Blueprint logs")

    # Test 3: Get specific day
    print("\n[4/4] Getting Blueprint log for specific date...")
    today_log = vessel.get_blueprint_log(date.today().isoformat(), 'faza', user_id)
    assert today_log is not None, "Blueprint log not found for today"
    assert today_log['compliance_score'] == 100, "Compliance score mismatch"
    print(f"✅ Blueprint log retrieved: compliance {today_log['compliance_score']}%")

    print("\n" + "="*70)
    print("ALL BLUEPRINT TESTS PASSED ✅")
    print("="*70)


def test_workouts():
    """Test workout logging."""
    print("\n" + "="*70)
    print("NEXUS VESSEL MODULE - WORKOUT TESTS")
    print("="*70)

    from core.database import init_db
    init_db()
    
    vessel = VesselModule()

    # Test 1: Log workout
    print("\n[1/3] Logging workout...")
    workout_data = {
        'owner': 'faza',
        'workout_type': 'hyperpump',
        'location': 'gym',
        'duration_minutes': 75,
        'total_volume_kg': 12500,
        'avg_rpe': 7.5,
        'prs_achieved': [
            {'exercise': 'Bench Press', 'weight': '100 kg', 'reps': 5}
        ],
        'exercises': [
            {'name': 'Bench Press', 'sets': 4, 'reps': '8-10', 'weight': '90 kg'},
            {'name': 'Squat', 'sets': 4, 'reps': '8-10', 'weight': '120 kg'}
        ]
    }
    
    result = vessel.log_workout(workout_data, user_id='faza')
    assert 'id' in result, f"Failed to log workout: {result}"
    workout_id = result['id']
    print(f"✅ Workout logged: {workout_id}")

    # Test 2: Get workouts
    print("\n[2/3] Listing workouts...")
    workouts = vessel.get_workouts(user_id='faza', owner='faza', days=30)
    assert len(workouts) > 0, "No workouts found"
    assert workouts[0]['workout_type'] == 'hyperpump', "Workout type mismatch"
    print(f"✅ Found {len(workouts)} workouts")

    # Test 3: Get workout stats
    print("\n[3/3] Getting workout statistics...")
    stats = vessel.get_workout_stats('faza', days=30)
    assert 'total_workouts' in stats, "Stats missing total_workouts"
    assert 'total_minutes' in stats, "Stats missing total_minutes"
    assert 'avg_rpe' in stats, "Stats missing avg_rpe"
    assert 'by_type' in stats, "Stats missing by_type"
    print(f"✅ Workout stats: {stats['total_workouts']} workouts, "
          f"{stats['total_minutes']} minutes, avg RPE {stats['avg_rpe']}")
    print(f"   By type: {stats['by_type']}")

    print("\n" + "="*70)
    print("ALL WORKOUT TESTS PASSED ✅")
    print("="*70)


def test_biometrics():
    """Test biometric logging."""
    print("\n" + "="*70)
    print("NEXUS VESSEL MODULE - BIOMETRICS TESTS")
    print("="*70)

    from core.database import init_db
    init_db()
    
    vessel = VesselModule()

    # Test 1: Log biometrics
    print("\n[1/3] Logging biometrics...")
    biometric_data = {
        'owner': 'faza',
        'date': date.today().isoformat(),
        'sleep_score': 85,
        'sleep_hours': 7.5,
        'deep_sleep_pct': 22.5,
        'hrv': 55,
        'resting_hr': 62,
        'recovery_score': 78,
        'weight_kg': 82.5,
        'body_fat_pct': 18.2,
        'device_source': 'Whoop'
    }
    
    result = vessel.log_biometrics(biometric_data, user_id='faza')
    assert 'id' in result, f"Failed to log biometrics: {result}"
    bio_id = result['id']
    print(f"✅ Biometrics logged: {bio_id}")

    # Test 2: Get biometrics
    print("\n[2/3] Listing biometrics...")
    biometrics = vessel.get_biometrics(user_id='faza', owner='faza', days=30)
    assert len(biometrics) > 0, "No biometrics found"
    assert biometrics[0]['sleep_score'] == 85, "Sleep score mismatch"
    print(f"✅ Found {len(biometrics)} biometric entries")

    # Test 3: Get trends
    print("\n[3/3] Getting biometric trends...")
    trends = vessel.get_biometric_trends('faza', days=30)
    assert 'avg_sleep_score' in trends, "Trends missing avg_sleep_score"
    assert 'avg_sleep_hours' in trends, "Trends missing avg_sleep_hours"
    assert 'avg_hrv' in trends, "Trends missing avg_hrv"
    assert 'trend' in trends, "Trends missing trend"
    print(f"✅ Biometric trends:")
    print(f"   Avg sleep: {trends['avg_sleep_hours']}h (score: {trends['avg_sleep_score']})")
    print(f"   HRV: {trends['avg_hrv']}, Resting HR: {trends['avg_resting_hr']}")
    print(f"   Weight: {trends['avg_weight']}kg (change: {trends['weight_change_kg']}kg)")
    print(f"   Trend: {trends['trend']}")

    print("\n" + "="*70)
    print("ALL BIOMETRICS TESTS PASSED ✅")
    print("="*70)


def test_sobriety():
    """Test sobriety tracking."""
    print("\n" + "="*70)
    print("NEXUS VESSEL MODULE - SOBRIETY TRACKING TESTS")
    print("="*70)

    from core.database import init_db
    init_db()

    vessel = VesselModule()

    # Get existing tracker or create new one
    tracker_data = {
        'owner': 'faza',
        'habit_type': 'alcohol',
        'start_date': '2025-01-01',
        'why_i_started': 'Wanted to improve health and save money'
    }

    # Check if tracker already exists
    existing_tracker = None
    from core.database import get_db
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM sobriety_tracker WHERE owner = ? AND habit_type = ?",
            (tracker_data['owner'], tracker_data['habit_type'])
        ).fetchone()
        if existing:
            existing_tracker = existing['id']

    if existing_tracker:
        tracker_id = existing_tracker
        print(f"\n[1/4] Using existing tracker: {tracker_id}")
    else:
        # Test 1: Start sobriety tracker
        print("\n[1/4] Starting sobriety tracker...")
        result = vessel.start_sobriety_tracker(tracker_data, user_id='faza')
        assert 'id' in result, f"Failed to start tracker: {result}"
        tracker_id = result['id']
        print(f"✅ Sobriety tracker started: {tracker_id}")

    # Test 2: Get tracker
    print("\n[2/4] Getting tracker status...")
    tracker = vessel.get_sobriety_tracker(tracker_id, user_id='faza')
    assert tracker is not None, "Tracker not found"
    assert tracker['habit_type'] == 'alcohol', "Habit type mismatch"
    assert tracker['current_streak_days'] > 0, "Streak should be > 0"
    print(f"✅ Tracker retrieved: habit={tracker['habit_type']}, "
          f"streak={tracker['current_streak_days']} days")

    # Test 3: Log relapse (for testing purposes, use a future date)
    print("\n[3/4] Logging relapse...")
    relapse_data = {
        'relapse_date': '2026-03-01',  # Future date for testing
        'reason': 'Birthday celebration',
        'triggers': ['social pressure', 'celebration'],
        'cost': 50.0
    }
    
    result = vessel.log_relapse(tracker_id, relapse_data, user_id='faza')
    assert 'id' in result, f"Failed to log relapse: {result}"
    print(f"✅ Relapse logged")

    # Test 4: Verify tracker updated
    print("\n[4/4] Verifying tracker updated...")
    updated_tracker = vessel.get_sobriety_tracker(tracker_id, user_id='faza')
    assert updated_tracker['last_relapse'] == '2026-03-01', "Last relapse date not updated"
    assert len(updated_tracker['relapse_log']) > 0, "Relapse log empty"
    print(f"✅ Tracker updated: last relapse={updated_tracker['last_relapse']}, "
          f"relapses logged={len(updated_tracker['relapse_log'])}")

    print("\n" + "="*70)
    print("ALL SOBRIETY TRACKER TESTS PASSED ✅")
    print("="*70)


def test_analytics():
    """Test analytics."""
    print("\n" + "="*70)
    print("NEXUS VESSEL MODULE - ANALYTICS TESTS")
    print("="*70)

    from core.database import init_db
    init_db()
    
    vessel = VesselModule()

    # Test 1: Get analytics
    print("\n[1/1] Getting analytics...")
    analytics = vessel.get_analytics('faza', days=30)
    assert 'blueprint' in analytics, "Analytics missing blueprint"
    assert 'workouts' in analytics, "Analytics missing workouts"
    assert 'biometrics' in analytics, "Analytics missing biometrics"
    assert 'insights' in analytics, "Analytics missing insights"
    print(f"✅ Analytics retrieved")
    print(f"   Blueprint: {analytics['blueprint']['avg_compliance']}% compliance")
    print(f"   Workouts: {analytics['workouts']['total_workouts']} workouts")
    print(f"   Insights: {len(analytics['insights'])}")
    for insight in analytics['insights']:
        print(f"   - {insight}")

    print("\n" + "="*70)
    print("ALL ANALYTICS TESTS PASSED ✅")
    print("="*70)


if __name__ == '__main__':
    try:
        test_blueprint()
        test_workouts()
        test_biometrics()
        test_sobriety()
        test_analytics()
        print("\n✅ All Vessel module tests passed successfully!")
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
