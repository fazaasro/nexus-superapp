"""
Pytest configuration and fixtures for Nexus Superapp tests
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import get_db, init_db
from core.auth import create_access_token, hash_password


@pytest.fixture(scope="session")
def test_database():
    """
    Create temporary database for testing
    """
    # Create temporary database directory
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test_levy.db')

    # Set database path in environment
    os.environ['TEST_DB_PATH'] = db_path

    # Initialize database by reading and executing schema directly
    schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    # Create connection and execute schema
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    # Run authentication migration to add password_hash column
    migration_path = Path(__file__).parent.parent / "database" / "migrations" / "add_auth_fields.sql"
    if migration_path.exists():
        with open(migration_path, 'r') as f:
            migration_sql = f.read()

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.executescript(migration_sql)
        conn.commit()
        conn.close()

    print(f"✅ Test database initialized at {db_path}")

    yield {'db_path': db_path, 'temp_dir': temp_dir}

    # Cleanup after tests
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_user(test_database):
    """
    Create test user
    """
    user_id = 'test_user'

    # Connect to test database
    import sqlite3
    conn = sqlite3.connect(test_database['db_path'])
    conn.row_factory = sqlite3.Row

    # Create test user
    conn.execute(
        """INSERT OR REPLACE INTO users
           (id, email, name, password_hash, is_active, email_verified)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, 'test@example.com', 'Test User', hash_password('test_password'), True, True)
    )

    conn.commit()
    conn.close()

    yield {'user_id': user_id, 'email': 'test@example.com', 'name': 'Test User'}


@pytest.fixture
def admin_token(test_user):
    """
    Create admin access token
    """
    token = create_access_token(test_user['user_id'], test_user['email'])
    return token
    """
    Create sample knowledge entry
    """
    entry = {
        'title': 'Test Knowledge Entry',
        'content': 'This is a test knowledge entry for testing purposes.',
        'domain': 'tech',
        'project': 'test_project',
        'content_type': 'note',
        'tags': ['test', 'unit-test'],
        'is_srs_eligible': False
    }
    return entry


@pytest.fixture
def sample_transaction(test_user):
    """
    Create sample transaction
    """
    txn = {
        'merchant': 'Test Merchant',
        'amount': 99.99,
        'currency': 'EUR',
        'category': 'lifestyle',
        'impact_score': 3,
        'split_type': 'solo',
        'notes': 'Test transaction for unit tests'
    }
    return txn


@pytest.fixture
def sample_contact(test_user):
    """
    Create sample contact
    """
    contact = {
        'name': 'Test Person',
        'relationship': 'friend',
        'inner_circle': False,
        'contact_frequency': 'monthly',
        'phone': '+1234567890',
        'email': 'test@example.com',
        'notes': 'Test contact for unit tests'
    }
    return contact


@pytest.fixture
def sample_health_log(test_user):
    """
    Create sample health log
    """
    log = {
        'owner': 'gaby',
        'symptom_type': 'allergy',
        'severity': 5,
        'trigger': 'peanuts',
        'notes': 'Test allergy log for unit tests',
        'location': 'home'
    }
    return log


@pytest.fixture
def sample_blueprint_log(test_user):
    """
    Create sample Blueprint log
    """
    log = {
        'owner': 'faza',
        'date': '2026-02-24',
        'supplements_taken': True,
        'supplement_list': ['vitamin_d', 'omega3'],
        'super_veggie_eaten': True,
        'nutty_pudding_eaten': True,
        'exercise_done': True,
        'meals_logged': ['breakfast', 'lunch', 'dinner'],
        'water_intake_ml': 2500
    }
    return log
