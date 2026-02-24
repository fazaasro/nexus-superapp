"""
Core database connection and utilities for AAC
"""
import os
import sqlite3
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional, Any

# Database path (check for TEST_DB_PATH for testing)
DB_PATH = Path(os.environ.get('TEST_DB_PATH', __file__)).parent.parent / "data" / "levy.db"

# User mapping from emails
USER_MAP = {
    "fazaasro@gmail.com": "faza",
    "gabriela.servitya@gmail.com": "gaby"
}

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database with schema"""
    schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
    with open(schema_path) as f:
        schema = f.read()
    
    with get_db() as conn:
        conn.executescript(schema)
    
    print(f"✅ Database initialized at {DB_PATH}")

def get_user_from_email(email: str) -> Optional[str]:
    """Map email to user ID"""
    return USER_MAP.get(email)

def log_audit(
    user_id: str,
    module: str,
    action: str,
    entity_type: str,
    entity_id: str,
    metadata: Dict = None,
    ip_address: str = None
):
    """Log an audit entry"""
    with get_db() as conn:
        conn.execute(
            """INSERT INTO audit_log 
               (user_id, module, action, entity_type, entity_id, metadata, ip_address)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, module, action, entity_type, entity_id, 
             json.dumps(metadata) if metadata else None, ip_address)
        )

class MultiTenantQuery:
    """Helper for multi-tenant queries"""
    
    @staticmethod
    def get_owners(user_context: str, include_shared: bool = True) -> List[str]:
        """Get list of owners for query filtering"""
        owners = [user_context]
        if include_shared:
            owners.append('shared')
        return owners
    
    @staticmethod
    def build_in_clause(owners: List[str]) -> str:
        """Build SQL IN clause for owners"""
        placeholders = ','.join(['?' for _ in owners])
        return f"({placeholders})"

# Utility functions
def generate_uuid() -> str:
    """Generate a unique ID"""
    import uuid
    return str(uuid.uuid4())[:8]  # Short UUID

def now_iso() -> str:
    """Current timestamp in ISO format"""
    from datetime import datetime
    return datetime.now().isoformat()

def safe_json_loads(data: Optional[str]) -> Optional[Dict]:
    """Safely parse JSON, return None if invalid"""
    if not data:
        return None
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None
