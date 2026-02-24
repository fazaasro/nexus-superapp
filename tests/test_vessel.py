"""
Vessel module tests
"""
import pytest
from modules.vessel.service import VesselModule


class TestVesselModuleInit:
    """Test VesselModule initialization"""

    def test_module_initialization(self):
        """Test that VesselModule initializes correctly"""
        vessel = VesselModule()

        assert vessel.db_path is not None
        assert vessel.WORKOUT_TYPES is not None
        assert len(vessel.WORKOUT_TYPES) > 0
        assert 'hyperpump' in vessel.WORKOUT_TYPES
        assert 'cardio' in vessel.WORKOUT_TYPES


class TestBlueprintProtocol:
    """Test Blueprint protocol logging"""

    def test_log_blueprint(self, test_user, sample_blueprint_log):
        """Test logging Blueprint protocol"""
        vessel = VesselModule()

        result = vessel.log_blueprint(sample_blueprint_log, test_user['user_id'])

        assert 'id' in result
        assert 'compliance_score' in result
        assert result['status'] == 'created' or result['status'] == 'updated'

    def test_calculate_blueprint_score(self):
        """Test calculating Blueprint compliance score"""
        vessel = VesselModule()

        # Perfect compliance (all fields True)
        perfect_data = {
            'supplements_taken': True,
            'super_veggie_eaten': True,
            'nutty_pudding_eaten': True,
            'exercise_done': True,
            'meals_logged': ['breakfast', 'lunch', 'dinner'],
            'water_intake_ml': 3000
        }
        perfect_score = vessel._calculate_blueprint_score(perfect_data)

        assert 0 <= perfect_score <= 1.0
        assert perfect_score > 0.8  # Should be high for perfect compliance

        # Poor compliance (all fields False)
        poor_data = {
            'supplements_taken': False,
            'super_veggie_eaten': False,
            'nutty_pudding_eaten': False,
            'exercise_done': False,
            'meals_logged': [],
            'water_intake_ml': 500
        }
        poor_score = vessel._calculate_blueprint_score(poor_data)

        assert 0 <= poor_score <= 1.0
        assert poor_score < 0.3  # Should be low for poor compliance

    def test_get_blueprint_logs(self, test_user, sample_blueprint_log):
        """Test getting Blueprint logs"""
        vessel = VesselModule()

        # Create test log
        vessel.log_blueprint(sample_blueprint_log, test_user['user_id'])

        # Get logs
        logs = vessel.get_blueprint_logs(user_id=test_user['user_id'], limit=10)

        assert len(logs) >= 1
        assert all('compliance_score' in log for log in logs)

    def test_get_blueprint_log_by_date(self, test_user, sample_blueprint_log):
        """Test getting Blueprint log for specific date"""
        vessel = VesselModule()

        # Create test log
        vessel.log_blueprint(sample_blueprint_log, test_user['user_id'])

        # Get log for specific date
        log = vessel.get_blueprint_log(sample_blueprint_log['date'], test_user['user_id'], user_id=test_user['user_id'])

        assert log is not None
        assert log['date'] == sample_blueprint_log['date']
        assert 'compliance_score' in log


class TestWorkouts:
    """Test workout logging"""

    def test_log_workout(self, test_user):
        """Test logging a workout"""
        vessel = VesselModule()

        workout_data = {
            'owner': test_user['user_id'],
            'workout_type': 'hyperpump',
            'duration_minutes': 45,
            'exercises': ['squat', 'bench', 'deadlift'],
            'notes': 'Test workout for unit tests'
        }

        result = vessel.log_workout(workout_data, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'

    def test_get_workouts(self, test_user):
        """Test getting workouts"""
        vessel = VesselModule()

        # Create test workout
        workout_data = {
            'owner': test_user['user_id'],
            'workout_type': 'cardio',
            'duration_minutes': 30,
            'exercises': ['running']
        }
        vessel.log_workout(workout_data, test_user['user_id'])

        # Get workouts
        workouts = vessel.get_workouts(user_id=test_user['user_id'], days=30)

        assert len(workouts) >= 1
        assert all('workout_type' in w for w in workouts)

    def test_get_workout_stats(self, test_user):
        """Test getting workout statistics"""
        vessel = VesselModule()

        # Create test workouts
        for i in range(5):
            workout_data = {
                'owner': test_user['user_id'],
                'workout_type': vessel.WORKOUT_TYPES[i % len(vessel.WORKOUT_TYPES)],
                'duration_minutes': 30 + i * 5,
                'exercises': ['exercise']
            }
            vessel.log_workout(workout_data, test_user['user_id'])

        # Get stats
        stats = vessel.get_workout_stats(test_user['user_id'], days=30)

        assert 'total_workouts' in stats
        assert 'by_type' in stats
        assert 'total_duration' in stats
        assert stats['total_workouts'] == 5


class TestBiometrics:
    """Test biometric tracking"""

    def test_log_biometrics(self, test_user):
        """Test logging biometrics"""
        vessel = VesselModule()

        biometric_data = {
            'owner': test_user['user_id'],
            'weight_kg': 75.5,
            'body_fat_percent': 15.0,
            'notes': 'Test biometric entry for unit tests'
        }

        result = vessel.log_biometrics(biometric_data, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'

    def test_get_biometrics(self, test_user):
        """Test getting biometric history"""
        vessel = VesselModule()

        # Create test entry
        biometric_data = {
            'owner': test_user['user_id'],
            'weight_kg': 75.5
        }
        vessel.log_biometrics(biometric_data, test_user['user_id'])

        # Get biometrics
        biometrics = vessel.get_biometrics(user_id=test_user['user_id'], days=30)

        assert len(biometrics) >= 1
        assert all('weight_kg' in b for b in biometrics)

    def test_get_biometric_trends(self, test_user):
        """Test getting biometric trends"""
        vessel = VesselModule()

        # Create test entries over multiple days
        for i in range(7):
            biometric_data = {
                'owner': test_user['user_id'],
                'weight_kg': 75.0 + i * 0.1,  # Slight variation
            }
            vessel.log_biometrics(biometric_data, test_user['user_id'])

        # Get trends
        trends = vessel.get_biometric_trends(test_user['user_id'], days=30)

        assert 'average_weight' in trends
        assert 'weight_change' in trends
        assert 'trend' in trends
        assert trends['trend'] in ['increasing', 'decreasing', 'stable']


class TestSobrietyTracker:
    """Test sobriety tracking"""

    def test_start_sobriety_tracker(self, test_user):
        """Test starting a sobriety tracker"""
        vessel = VesselModule()

        tracker_data = {
            'owner': test_user['user_id'],
            'habit_type': 'alcohol',
            'start_date': '2026-02-24',
            'reason': 'Starting sobriety journey',
            'milestone_days': [30, 60, 90, 180, 365]
        }

        result = vessel.start_sobriety_tracker(tracker_data, test_user['user_id'])

        assert 'id' in result
        assert 'status' == 'created'
        assert result['id'].startswith('sob_')

    def test_get_sobriety_tracker(self, test_user):
        """Test getting sobriety tracker status"""
        vessel = VesselModule()

        # Create tracker
        tracker_data = {
            'owner': test_user['user_id'],
            'habit_type': 'nicotine',
            'start_date': '2026-02-24'
        }
        create_result = vessel.start_sobriety_tracker(tracker_data, test_user['user_id'])
        tracker_id = create_result['id']

        # Get tracker
        tracker = vessel.get_sobriety_tracker(tracker_id, test_user['user_id'])

        assert tracker is not None
        assert tracker['id'] == tracker_id
        assert 'days_sober' in tracker
        assert 'relapse_count' in tracker
        assert 'status' in tracker

    def test_log_relapse(self, test_user):
        """Test logging a relapse"""
        vessel = VesselModule()

        # Create tracker
        tracker_data = {
            'owner': test_user['user_id'],
            'habit_type': 'alcohol',
            'start_date': '2026-02-24'
        }
        create_result = vessel.start_sobriety_tracker(tracker_data, test_user['user_id'])
        tracker_id = create_result['id']

        # Log relapse
        relapse_data = {
            'trigger': 'Social gathering',
            'severity': 3,
            'notes': 'Relapse at party'
        }
        result = vessel.log_relapse(tracker_id, relapse_data, test_user['user_id'])

        assert 'status' == 'logged'
        assert result['tracker_id'] == tracker_id

        # Verify relapse count increased
        tracker = vessel.get_sobriety_tracker(tracker_id, test_user['user_id'])
        assert tracker['relapse_count'] >= 1


class TestAnalytics:
    """Test analytics functionality"""

    def test_get_analytics(self, test_user, sample_blueprint_log):
        """Test getting overall health analytics"""
        vessel = VesselModule()

        # Create test data
        vessel.log_blueprint(sample_blueprint_log, test_user['user_id'])

        # Get analytics
        analytics = vessel.get_analytics(test_user['user_id'], days=30)

        assert 'blueprint_compliance' in analytics
        assert 'workout_stats' in analytics
        assert 'biometric_trends' in analytics
        assert 'overall_health_score' in analytics
        assert 0 <= analytics['overall_health_score'] <= 100


class TestStatistics:
    """Test statistics functionality"""

    def test_get_stats(self, test_user):
        """Test getting Vessel module statistics"""
        vessel = VesselModule()

        # Create test data
        workout_data = {
            'owner': test_user['user_id'],
            'workout_type': 'cardio',
            'duration_minutes': 30
        }
        vessel.log_workout(workout_data, test_user['user_id'])

        # Get stats
        stats = vessel.get_stats(user_id=test_user['user_id'], owner=test_user['user_id'])

        assert 'total_blueprint_logs' in stats
        assert 'total_workouts' in stats
        assert 'total_biometric_logs' in stats
        assert 'active_trackers' in stats
        assert 'days_tracked' in stats


@pytest.mark.integration
class TestVesselIntegration:
    """Integration tests for Vessel module"""

    @pytest.mark.asyncio
    async def test_complete_blueprint_workflow(self, test_user, sample_blueprint_log):
        """Test complete Blueprint workflow: log -> check -> update"""
        vessel = VesselModule()

        # Create Blueprint log
        create_result = vessel.log_blueprint(sample_blueprint_log, test_user['user_id'])
        log_id = create_result['id']

        # Get log
        log = vessel.get_blueprint_log(sample_blueprint_log['date'], test_user['user_id'], user_id=test_user['user_id'])

        assert log is not None
        assert log['id'] == log_id

    @pytest.mark.asyncio
    async def test_sobriety_journey_workflow(self, test_user):
        """Test complete sobriety journey: start -> relapse -> continue"""
        vessel = VesselModule()

        # Start tracker
        tracker_data = {
            'owner': test_user['user_id'],
            'habit_type': 'alcohol',
            'start_date': '2026-02-24'
        }
        create_result = vessel.start_sobriety_tracker(tracker_data, test_user['user_id'])
        tracker_id = create_result['id']

        # Get tracker (should be active)
        tracker = vessel.get_sobriety_tracker(tracker_id, test_user['user_id'])
        assert tracker['status'] == 'active'
        assert tracker['relapse_count'] == 0

        # Log relapse
        relapse_data = {
            'trigger': 'Test relapse',
            'severity': 2,
            'notes': 'Unit test relapse'
        }
        vessel.log_relapse(tracker_id, relapse_data, test_user['user_id'])

        # Get tracker (should show relapse)
        updated_tracker = vessel.get_sobriety_tracker(tracker_id, test_user['user_id'])
        assert updated_tracker['relapse_count'] == 1
