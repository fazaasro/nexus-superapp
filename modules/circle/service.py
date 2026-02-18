"""
Module 3: The Circle (Social CRM)
Contact management, health logs, couple journal, insights
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import Counter
from pathlib import Path

from core.database import get_db, generate_uuid, log_audit


class CircleModule:
    """Social CRM module for relationships and health tracking"""
    
    SYMPTOM_TYPES = ['allergy', 'reflux', 'mood', 'energy', 'pain', 'sleep']
    RELATIONSHIP_TYPES = ['family', 'friend', 'colleague', 'mentor', 'other']
    CONTACT_FREQUENCIES = ['weekly', 'biweekly', 'monthly', 'quarterly']
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "levy.db"
    
    # ========== CONTACT MANAGEMENT ==========
    
    def create_contact(self, data: Dict, user_id: str) -> Dict:
        """Create a new contact"""
        contact_id = f"cnt_{generate_uuid()}"
        
        # Calculate next scheduled ping
        next_ping = self._calculate_next_ping(data.get('contact_frequency'))
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO contacts
                   (id, owner, name, relationship, inner_circle, phone, email,
                    telegram_handle, contact_frequency, next_scheduled_ping,
                    birthday, important_dates, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    contact_id,
                    data.get('owner', user_id),
                    data['name'],
                    data['relationship'],
                    data.get('inner_circle', False),
                    data.get('phone'),
                    data.get('email'),
                    data.get('telegram_handle'),
                    data.get('contact_frequency'),
                    next_ping,
                    data.get('birthday'),
                    json.dumps(data.get('important_dates', [])),
                    data.get('notes')
                )
            )
        
        log_audit(user_id, 'circle', 'create', 'contact', contact_id,
                 {'name': data['name'], 'relationship': data['relationship']})
        
        return {'id': contact_id, 'status': 'created', 'next_scheduled_ping': next_ping}
    
    def get_contacts(self, user_id: str, inner_circle_only: bool = False,
                    relationship: str = None) -> List[Dict]:
        """Get contacts for user"""
        query = "SELECT * FROM contacts WHERE owner = ?"
        params = [user_id]
        
        if inner_circle_only:
            query += " AND inner_circle = 1"
        
        if relationship:
            query += " AND relationship = ?"
            params.append(relationship)
        
        query += " ORDER BY inner_circle DESC, name ASC"
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        contacts = []
        for row in rows:
            contact = dict(row)
            if contact.get('important_dates'):
                contact['important_dates'] = json.loads(contact['important_dates'])
            contacts.append(contact)
        
        return contacts
    
    def get_contact(self, contact_id: str, user_id: str) -> Optional[Dict]:
        """Get a single contact by ID"""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM contacts WHERE id = ?",
                (contact_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            contact = dict(row)
            if contact.get('important_dates'):
                contact['important_dates'] = json.loads(contact['important_dates'])
            
            return contact
    
    def update_contact(self, contact_id: str, data: Dict, user_id: str) -> Dict:
        """Update a contact"""
        update_fields = []
        params = []
        
        for field in ['name', 'relationship', 'inner_circle', 'phone', 'email',
                     'telegram_handle', 'last_contact_date', 'contact_frequency',
                     'notes']:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])
        
        if 'important_dates' in data:
            update_fields.append("important_dates = ?")
            params.append(json.dumps(data['important_dates']))
        
        # Recalculate next ping if frequency changed
        if 'contact_frequency' in data:
            next_ping = self._calculate_next_ping(data['contact_frequency'])
            update_fields.append("next_scheduled_ping = ?")
            params.append(next_ping)
        
        if not update_fields:
            return {'error': 'No fields to update'}
        
        params.append(contact_id)
        
        with get_db() as conn:
            conn.execute(
                f"UPDATE contacts SET {', '.join(update_fields)} WHERE id = ?",
                params
            )
        
        log_audit(user_id, 'circle', 'update', 'contact', contact_id, data)
        
        return {'id': contact_id, 'status': 'updated'}
    
    def record_contact(self, contact_id: str, user_id: str) -> Dict:
        """Record that you contacted this person"""
        contact = self.get_contact(contact_id, user_id)
        if not contact:
            return {'error': 'Contact not found'}
        
        # Update last contact date
        with get_db() as conn:
            conn.execute(
                "UPDATE contacts SET last_contact_date = ? WHERE id = ?",
                (datetime.now().date().isoformat(), contact_id)
            )
        
        # Recalculate next ping
        next_ping = self._calculate_next_ping(contact.get('contact_frequency'))
        
        with get_db() as conn:
            conn.execute(
                "UPDATE contacts SET next_scheduled_ping = ? WHERE id = ?",
                (next_ping, contact_id)
            )
        
        log_audit(user_id, 'circle', 'contact', 'contact', contact_id,
                 {'contact_name': contact['name']})
        
        return {'id': contact_id, 'last_contact_date': datetime.now().date().isoformat(),
                'next_scheduled_ping': next_ping}
    
    def _calculate_next_ping(self, frequency: str) -> Optional[str]:
        """Calculate next scheduled ping date"""
        if not frequency:
            return None
        
        days_map = {
            'weekly': 7,
            'biweekly': 14,
            'monthly': 30,
            'quarterly': 90
        }
        
        days = days_map.get(frequency, 30)
        next_date = datetime.now() + timedelta(days=days)
        return next_date.date().isoformat()
    
    # ========== HEALTH LOGS ==========
    
    def create_health_log(self, data: Dict, logged_by: str) -> Dict:
        """Create a health log entry"""
        log_id = f"hlg_{generate_uuid()}"
        
        # Validate severity
        severity = data.get('severity', 5)
        if not (1 <= severity <= 10):
            return {'error': 'Severity must be between 1 and 10'}
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO health_logs
                   (id, owner, logged_by, symptom_type, severity, triggers,
                    location, meal_before, stress_level, sleep_quality,
                    description, remedy_tried, remedy_effectiveness)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    log_id,
                    data['owner'],
                    logged_by,
                    data['symptom_type'],
                    severity,
                    json.dumps(data.get('triggers', [])),
                    data.get('location'),
                    data.get('meal_before'),
                    data.get('stress_level'),
                    data.get('sleep_quality'),
                    data.get('description'),
                    data.get('remedy_tried'),
                    data.get('remedy_effectiveness')
                )
            )
        
        log_audit(logged_by, 'circle', 'create', 'health_log', log_id,
                 {'owner': data['owner'], 'symptom': data['symptom_type'], 'severity': severity})
        
        return {'id': log_id, 'status': 'created'}
    
    def get_health_logs(self, user_id: str, owner: str = None,
                       symptom_type: str = None, days: int = 30) -> List[Dict]:
        """Get health logs"""
        query = """
            SELECT * FROM health_logs
            WHERE timestamp > datetime('now', ?)
        """
        params = [f'-{days} days']
        
        if owner:
            query += " AND owner = ?"
            params.append(owner)
        
        if symptom_type:
            query += " AND symptom_type = ?"
            params.append(symptom_type)
        
        query += " ORDER BY timestamp DESC"
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        logs = []
        for row in rows:
            log = dict(row)
            if log.get('triggers'):
                log['triggers'] = json.loads(log['triggers'])
            logs.append(log)
        
        return logs
    
    def get_health_log(self, log_id: str, user_id: str) -> Optional[Dict]:
        """Get a single health log by ID"""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM health_logs WHERE id = ?",
                (log_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            log = dict(row)
            if log.get('triggers'):
                log['triggers'] = json.loads(log['triggers'])
            
            return log
    
    def analyze_health(self, owner: str, symptom_type: str, days: int = 30) -> Dict:
        """Analyze health logs for patterns and triggers"""
        logs = self.get_health_logs('system', owner=owner, symptom_type=symptom_type, days=days)
        
        if not logs:
            return {
                'symptom_type': symptom_type,
                'episode_count': 0,
                'avg_severity': 0,
                'common_triggers': [],
                'severity_trend': 'unknown',
                'insights': ['No data available for analysis']
            }
        
        # Calculate statistics
        total_severity = sum(log['severity'] for log in logs)
        avg_severity = total_severity / len(logs)
        
        # Find common triggers
        all_triggers = []
        for log in logs:
            all_triggers.extend(log.get('triggers', []))
        
        trigger_counts = Counter(all_triggers)
        common_triggers = [{'trigger': t, 'count': c} for t, c in trigger_counts.most_common(5)]
        
        # Determine trend (compare first half vs second half)
        mid = len(logs) // 2
        if mid > 0:
            early_avg = sum(log['severity'] for log in logs[:mid]) / mid
            late_avg = sum(log['severity'] for log in logs[mid:]) / (len(logs) - mid)
            
            if late_avg < early_avg - 1:
                trend = 'improving'
            elif late_avg > early_avg + 1:
                trend = 'worsening'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'
        
        # Generate insights
        insights = []
        if common_triggers:
            insights.append(f"Most common trigger: {common_triggers[0]['trigger']} "
                          f"({common_triggers[0]['count']} episodes)")
        
        if avg_severity > 7:
            insights.append(f"Average severity is high ({avg_severity:.1f}/10)")
        elif avg_severity < 4:
            insights.append(f"Average severity is low ({avg_severity:.1f}/10)")
        
        if trend == 'improving':
            insights.append("Severity trend: Improving over time")
        elif trend == 'worsening':
            insights.append("Severity trend: Worsening over time")
        
        return {
            'symptom_type': symptom_type,
            'episode_count': len(logs),
            'avg_severity': round(avg_severity, 1),
            'common_triggers': common_triggers,
            'severity_trend': trend,
            'insights': insights
        }
    
    # ========== RELATIONSHIP CHECK-INS ==========
    
    def create_checkin(self, data: Dict, user_id: str) -> Dict:
        """Create a relationship check-in"""
        checkin_id = f"rchk_{generate_uuid()}"
        
        # Validate mood scores
        for field in ['faza_mood', 'gaby_mood', 'relationship_vibe']:
            if field not in data:
                return {'error': f'Missing field: {field}'}
            if not (1 <= data[field] <= 10):
                return {'error': f'{field} must be between 1 and 10'}
        
        # Calculate sentiment score
        avg_mood = (data['faza_mood'] + data['gaby_mood']) / 2
        sentiment_score = (avg_mood + data['relationship_vibe']) / 20  # Normalize to 0-1
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO relationship_checkins
                   (id, owner, faza_mood, gaby_mood, relationship_vibe,
                    topics_discussed, friction_points, wins, sentiment_score)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    checkin_id,
                    'shared',
                    data['faza_mood'],
                    data['gaby_mood'],
                    data['relationship_vibe'],
                    json.dumps(data.get('topics_discussed', [])),
                    data.get('friction_points'),
                    data.get('wins'),
                    sentiment_score
                )
            )
        
        log_audit(user_id, 'circle', 'create', 'checkin', checkin_id,
                 {'faza_mood': data['faza_mood'], 'gaby_mood': data['gaby_mood'],
                  'vibe': data['relationship_vibe']})
        
        return {'id': checkin_id, 'status': 'created', 'sentiment_score': sentiment_score}
    
    def get_checkins(self, start_date: str = None, end_date: str = None,
                    min_vibe: int = None, limit: int = 50) -> List[Dict]:
        """Get relationship check-ins"""
        query = "SELECT * FROM relationship_checkins WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date(timestamp) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date(timestamp) <= ?"
            params.append(end_date)
        
        if min_vibe:
            query += " AND relationship_vibe >= ?"
            params.append(min_vibe)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        checkins = []
        for row in rows:
            checkin = dict(row)
            if checkin.get('topics_discussed'):
                checkin['topics_discussed'] = json.loads(checkin['topics_discussed'])
            checkins.append(checkin)
        
        return checkins
    
    def get_checkin_trends(self, days: int = 30) -> Dict:
        """Get mood and relationship trends"""
        checkins = self.get_checkins(limit=days)
        
        if not checkins:
            return {
                'faza_avg_mood': 0,
                'gaby_avg_mood': 0,
                'relationship_avg_vibe': 0,
                'trend': 'unknown',
                'insights': []
            }
        
        # Calculate averages
        faza_avg = sum(c['faza_mood'] for c in checkins) / len(checkins)
        gaby_avg = sum(c['gaby_mood'] for c in checkins) / len(checkins)
        vibe_avg = sum(c['relationship_vibe'] for c in checkins) / len(checkins)
        
        # Determine trend
        recent = checkins[:len(checkins)//3] if len(checkins) >= 3 else checkins
        early = checkins[-len(checkins)//3:] if len(checkins) >= 3 else checkins
        
        if len(recent) > 0 and len(early) > 0:
            recent_vibe = sum(c['relationship_vibe'] for c in recent) / len(recent)
            early_vibe = sum(c['relationship_vibe'] for c in early) / len(early)
            
            if recent_vibe > early_vibe + 0.5:
                trend = 'improving'
            elif recent_vibe < early_vibe - 0.5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'
        
        # Generate insights
        insights = []
        if faza_avg > gaby_avg:
            insights.append(f"Faza's average mood ({faza_avg:.1f}) is higher than Gaby's ({gaby_avg:.1f})")
        elif gaby_avg > faza_avg:
            insights.append(f"Gaby's average mood ({gaby_avg:.1f}) is higher than Faza's ({faza_avg:.1f})")
        
        if vibe_avg < 6:
            insights.append("Relationship vibe is below average - consider a check-in")
        elif vibe_avg > 8:
            insights.append("Relationship vibe is strong - keep it up!")
        
        if trend == 'improving':
            insights.append("Relationship health is improving over time")
        elif trend == 'declining':
            insights.append("Relationship health is declining - consider addressing friction points")
        
        return {
            'faza_avg_mood': round(faza_avg, 1),
            'gaby_avg_mood': round(gaby_avg, 1),
            'relationship_avg_vibe': round(vibe_avg, 1),
            'trend': trend,
            'checkin_count': len(checkins),
            'insights': insights
        }
    
    # ========== REMINDERS ==========
    
    def get_reminders(self, user_id: str) -> Dict:
        """Get pending reminders (contacts, birthdays, health alerts)"""
        today = datetime.now().date()
        today_str = today.isoformat()
        
        reminders = {
            'contacts_to_ping': [],
            'upcoming_birthdays': [],
            'health_alerts': [],
            'relationship_alerts': []
        }
        
        # Contact reminders (overdue pings)
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT * FROM contacts
                   WHERE owner = ? AND next_scheduled_ping IS NOT NULL
                   AND next_scheduled_ping <= ?
                   ORDER BY next_scheduled_ping""",
                (user_id, today_str)
            )
            
            for row in cursor:
                contact = dict(row)
                reminders['contacts_to_ping'].append({
                    'id': contact['id'],
                    'name': contact['name'],
                    'relationship': contact['relationship'],
                    'last_contact': contact['last_contact_date'],
                    'next_scheduled_ping': contact['next_scheduled_ping'],
                    'overdue_days': (today - datetime.fromisoformat(contact['next_scheduled_ping']).date()).days
                })
        
        # Birthday reminders (next 30 days)
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT * FROM contacts
                   WHERE owner = ? AND birthday IS NOT NULL""",
                (user_id,)
            )
            
            for row in cursor:
                contact = dict(row)
                birthday = datetime.strptime(contact['birthday'], '%Y-%m-%d').date()
                birthday_this_year = birthday.replace(year=today.year)
                
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                
                days_until = (birthday_this_year - today).days
                
                if 0 <= days_until <= 30:
                    reminders['upcoming_birthdays'].append({
                        'id': contact['id'],
                        'name': contact['name'],
                        'birthday': contact['birthday'],
                        'age': birthday_this_year.year - birthday.year,
                        'days_until': days_until
                    })
        
        # Health alerts (increased severity)
        # Check for reflux episodes in last 7 days
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT owner, symptom_type, COUNT(*) as count, AVG(severity) as avg_severity
                   FROM health_logs
                   WHERE timestamp > datetime('now', '-7 days')
                     AND symptom_type = 'reflux'
                   GROUP BY owner, symptom_type
                   HAVING avg_severity > 6"""
            )
            
            for row in cursor:
                reminders['health_alerts'].append({
                    'owner': row['owner'],
                    'symptom_type': row['symptom_type'],
                    'episode_count': row['count'],
                    'avg_severity': round(row['avg_severity'], 1),
                    'message': f"High reflux severity for {row['owner']} in last 7 days"
                })
        
        # Relationship alerts (declining vibe)
        trends = self.get_checkin_trends(days=14)
        if trends['trend'] == 'declining' and trends['relationship_avg_vibe'] < 6:
            reminders['relationship_alerts'].append({
                'message': "Relationship vibe declining - consider a check-in",
                'current_vibe': trends['relationship_avg_vibe'],
                'trend': 'declining'
            })
        
        return reminders
    
    # ========== STATISTICS ==========
    
    def get_stats(self, user_id: str) -> Dict:
        """Get Circle module statistics"""
        with get_db() as conn:
            # Contacts
            total_contacts = conn.execute(
                "SELECT COUNT(*) as count FROM contacts WHERE owner = ?",
                (user_id,)
            ).fetchone()['count']
            
            inner_circle = conn.execute(
                "SELECT COUNT(*) as count FROM contacts WHERE owner = ? AND inner_circle = 1",
                (user_id,)
            ).fetchone()['count']
            
            # Health logs
            health_logs_30d = conn.execute(
                """SELECT COUNT(*) as count
                   FROM health_logs
                   WHERE timestamp > datetime('now', '-30 days')""",
            ).fetchone()['count']
            
            # Check-ins
            checkins_30d = conn.execute(
                """SELECT COUNT(*) as count
                   FROM relationship_checkins
                   WHERE timestamp > datetime('now', '-30 days')""",
            ).fetchone()['count']
            
            return {
                'total_contacts': total_contacts,
                'inner_circle': inner_circle,
                'health_logs_30d': health_logs_30d,
                'checkins_30d': checkins_30d
            }
