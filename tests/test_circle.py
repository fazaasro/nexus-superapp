"""
Circle module tests
"""
import pytest
from modules.circle.service import CircleModule


class TestCircleModuleInit:
    """Test CircleModule initialization"""

    def test_module_initialization(self):
        """Test that CircleModule initializes correctly"""
        circle = CircleModule()

        assert circle.db_path is not None
        assert circle.SYMPTOM_TYPES is not None
        assert len(circle.SYMPTOM_TYPES) > 0
        assert 'allergy' in circle.SYMPTOM_TYPES
        assert 'mood' in circle.SYMPTOM_TYPES
        assert circle.RELATIONSHIP_TYPES is not None
        assert 'friend' in circle.RELATIONSHIP_TYPES
        assert 'family' in circle.RELATIONSHIP_TYPES


class TestContactCRUD:
    """Test contact CRUD operations"""

    def test_create_contact(self, test_user, sample_contact):
        """Test creating a contact"""
        circle = CircleModule()

        result = circle.create_contact(sample_contact, test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'
        assert result['id'].startswith('cnt_')

    def test_get_contacts(self, test_user, sample_contact):
        """Test getting contacts"""
        circle = CircleModule()

        # Create test contact
        create_result = circle.create_contact(sample_contact, test_user['user_id'])
        contact_id = create_result['id']

        # Get contacts
        contacts = circle.get_contacts(test_user['user_id'])

        assert len(contacts) > 0
        # Find our created contact
        found = [c for c in contacts if c['id'] == contact_id]
        assert len(found) == 1

    def test_get_contact_by_id(self, test_user, sample_contact):
        """Test getting single contact by ID"""
        circle = CircleModule()

        # Create test contact
        create_result = circle.create_contact(sample_contact, test_user['user_id'])
        contact_id = create_result['id']

        # Get contact
        contact = circle.get_contact(contact_id, test_user['user_id'])

        assert contact is not None
        assert contact['id'] == contact_id
        assert contact['name'] == sample_contact['name']

    def test_update_contact(self, test_user, sample_contact):
        """Test updating a contact"""
        circle = CircleModule()

        # Create test contact
        create_result = circle.create_contact(sample_contact, test_user['user_id'])
        contact_id = create_result['id']

        # Update contact
        update_data = {
            'name': 'Updated Name',
            'notes': 'Updated contact for testing purposes.'
        }
        update_result = circle.update_contact(contact_id, update_data, test_user['user_id'])

        assert update_result['status'] == 'updated'
        assert update_result['id'] == contact_id

        # Verify update
        updated_contact = circle.get_contact(contact_id, test_user['user_id'])
        assert updated_contact['name'] == 'Updated Name'

    def test_record_contact(self, test_user, sample_contact):
        """Test recording that you contacted someone"""
        circle = CircleModule()

        # Create test contact
        create_result = circle.create_contact(sample_contact, test_user['user_id'])
        contact_id = create_result['id']

        # Record contact
        result = circle.record_contact(contact_id, test_user['user_id'])

        assert 'id' in result
        assert 'last_contact_date' in result
        assert 'next_scheduled_ping' in result
        assert result['id'] == contact_id

    def test_calculate_next_ping(self):
        """Test calculating next scheduled ping"""
        circle = CircleModule()

        # Weekly frequency (7 days)
        weekly_date = circle._calculate_next_ping('weekly')
        assert weekly_date is not None
        assert isinstance(weekly_date, str)

        # Monthly frequency (30 days)
        monthly_date = circle._calculate_next_ping('monthly')
        assert monthly_date is not None
        assert isinstance(monthly_date, str)

        # Quarterly frequency (90 days)
        quarterly_date = circle._calculate_next_ping('quarterly')
        assert quarterly_date is not None
        assert isinstance(quarterly_date, str)


class TestHealthLogs:
    """Test health log functionality"""

    def test_create_health_log(self, test_user, sample_health_log):
        """Test creating a health log"""
        circle = CircleModule()

        result = circle.create_health_log(sample_health_log, logged_by=test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'
        assert result['id'].startswith('hlg_')

    def test_get_health_logs(self, test_user, sample_health_log):
        """Test getting health logs"""
        circle = CircleModule()

        # Create test health log
        create_result = circle.create_health_log(sample_health_log, logged_by=test_user['user_id'])
        log_id = create_result['id']

        # Get health logs
        logs = circle.get_health_logs(user_id=test_user['user_id'], owner=sample_health_log['owner'])

        assert len(logs) >= 0
        # Find our created log
        found = [l for l in logs if l['id'] == log_id]
        assert len(found) == 1

    def test_analyze_health(self, test_user, sample_health_log):
        """Test health analysis"""
        circle = CircleModule()

        # Create test health logs
        circle.create_health_log(sample_health_log, logged_by=test_user['user_id'])
        circle.create_health_log(sample_health_log, logged_by=test_user['user_id'])

        # Analyze health
        analysis = circle.analyze_health(sample_health_log['owner'], sample_health_log['symptom_type'], days=30)

        assert 'total_logs' in analysis
        assert 'severity_distribution' in analysis
        assert 'trends' in analysis
        assert analysis['total_logs'] >= 2


class TestCheckIns:
    """Test relationship check-in functionality"""

    def test_create_checkin(self, test_user):
        """Test creating a check-in"""
        circle = CircleModule()

        checkin_data = {
            'for_user': 'gaby',
            'vibe': 5,
            'notes': 'Feeling great today!',
            'activities': ['coding', 'cooking']
        }

        result = circle.create_checkin(checkin_data, user_id=test_user['user_id'])

        assert 'id' in result
        assert result['status'] == 'created'

    def test_get_checkins(self, test_user):
        """Test getting check-ins"""
        circle = CircleModule()

        # Create test check-in
        checkin_data = {
            'for_user': 'gaby',
            'vibe': 4
        }
        circle.create_checkin(checkin_data, user_id=test_user['user_id'])

        # Get check-ins
        checkins = circle.get_checkins(start_date=None, end_date=None, limit=10)

        assert len(checkins) >= 1

    def test_get_checkin_trends(self, test_user):
        """Test getting check-in trends"""
        circle = CircleModule()

        # Create test check-ins
        for i in range(5):
            checkin_data = {
                'for_user': 'gaby',
                'vibe': 3 + (i % 4)  # Varied vibes
            }
            circle.create_checkin(checkin_data, user_id=test_user['user_id'])

        # Get trends
        trends = circle.get_checkin_trends(days=30)

        assert 'average_vibe' in trends
        assert 'vibe_trend' in trends
        assert 'total_checkins' in trends
        assert trends['total_checkins'] >= 5


class TestReminders:
    """Test reminder functionality"""

    def test_get_reminders(self, test_user, sample_contact):
        """Test getting pending reminders"""
        circle = CircleModule()

        # Create test contact with upcoming ping
        create_result = circle.create_contact(sample_contact, test_user['user_id'])
        contact_id = create_result['id']

        # Get reminders
        reminders = circle.get_reminders(test_user['user_id'])

        assert isinstance(reminders, list)
        # Should include our contact if ping is soon
        # (may not if date is far in future)
        assert isinstance(reminders, list)


class TestStatistics:
    """Test statistics functionality"""

    def test_get_stats(self, test_user, sample_contact, sample_health_log):
        """Test getting Circle module statistics"""
        circle = CircleModule()

        # Create test data
        circle.create_contact(sample_contact, test_user['user_id'])
        circle.create_health_log(sample_health_log, logged_by=test_user['user_id'])

        # Get stats
        stats = circle.get_stats(test_user['user_id'])

        assert 'total_contacts' in stats
        assert 'total_health_logs' in stats
        assert 'inner_circle_count' in stats
        assert 'total_checkins' in stats
        assert stats['total_contacts'] >= 1
        assert stats['total_health_logs'] >= 1


@pytest.mark.integration
class TestCircleIntegration:
    """Integration tests for Circle module"""

    @pytest.mark.asyncio
    async def test_complete_contact_workflow(self, test_user, sample_contact):
        """Test complete contact workflow: create -> update -> contact -> delete"""
        circle = CircleModule()

        # Create
        create_result = circle.create_contact(sample_contact, test_user['user_id'])
        contact_id = create_result['id']

        # Update
        update_data = {'notes': 'Updated notes'}
        circle.update_contact(contact_id, update_data, test_user['user_id'])

        # Record contact
        circle.record_contact(contact_id, test_user['user_id'])

        # Verify
        contact = circle.get_contact(contact_id, test_user['user_id'])
        assert contact['notes'] == 'Updated notes'
        assert contact['last_contact_date'] is not None

    @pytest.mark.asyncio
    async def test_health_tracking_workflow(self, test_user, sample_health_log):
        """Test health tracking workflow: log -> analyze -> trends"""
        circle = CircleModule()

        # Create health logs
        for i in range(3):
            log_data = sample_health_log.copy()
            log_data['severity'] = 3 + i  # Varied severity
            circle.create_health_log(log_data, logged_by=test_user['user_id'])

        # Analyze
        analysis = circle.analyze_health(sample_health_log['owner'], sample_health_log['symptom_type'], days=30)

        assert analysis['total_logs'] == 3
        assert 'severity_distribution' in analysis
