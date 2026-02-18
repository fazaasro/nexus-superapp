"""
Module 4: The Vessel (Health Tracking)
Blueprint protocol, Empire Fit workouts, biometrics, sobriety tracking
"""
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any
from collections import Counter
from pathlib import Path

from core.database import get_db, generate_uuid, log_audit


class VesselModule:
    """Health tracking module for Blueprint protocol, workouts, biometrics"""
    
    WORKOUT_TYPES = ['hyperpump', 'cardio', 'recovery', 'mobility']
    HABIT_TYPES = ['alcohol', 'nicotine', 'caffeine', 'social_media', 'gaming', 'other']
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "levy.db"
    
    # ========== BLUEPRINT PROTOCOL ==========
    
    def log_blueprint(self, data: Dict, user_id: str) -> Dict:
        """Log Blueprint protocol compliance for a day"""
        # Calculate compliance score
        compliance_score = self._calculate_blueprint_score(data)
        
        # Check if entry exists
        with get_db() as conn:
            existing = conn.execute(
                "SELECT id FROM blueprint_logs WHERE date = ? AND owner = ?",
                (data['date'], data['owner'])
            ).fetchone()
            
            if existing:
                # Update existing entry
                log_id = existing['id']
                conn.execute(
                    """UPDATE blueprint_logs
                       SET supplements_taken = ?, super_veggie_eaten = ?,
                           nutty_pudding_eaten = ?, exercise_done = ?,
                           supplement_list = ?, meals_logged = ?,
                           water_intake_ml = ?, compliance_score = ?
                       WHERE id = ?""",
                    (
                        data.get('supplements_taken', False),
                        data.get('super_veggie_eaten', False),
                        data.get('nutty_pudding_eaten', False),
                        data.get('exercise_done', False),
                        json.dumps(data.get('supplement_list', [])),
                        json.dumps(data.get('meals_logged', [])),
                        data.get('water_intake_ml'),
                        compliance_score,
                        log_id
                    )
                )
            else:
                # Create new entry
                log_id = f"bpl_{generate_uuid()}"
                
                conn.execute(
                    """INSERT INTO blueprint_logs
                       (id, owner, date, supplements_taken, super_veggie_eaten,
                        nutty_pudding_eaten, exercise_done, supplement_list,
                        meals_logged, water_intake_ml, compliance_score)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        log_id,
                        data['owner'],
                        data['date'],
                        data.get('supplements_taken', False),
                        data.get('super_veggie_eaten', False),
                        data.get('nutty_pudding_eaten', False),
                        data.get('exercise_done', False),
                        json.dumps(data.get('supplement_list', [])),
                        json.dumps(data.get('meals_logged', [])),
                        data.get('water_intake_ml'),
                        compliance_score
                    )
                )
        
        # Log audit outside database context
        log_audit(user_id, 'vessel', 'create' if not existing else 'update', 'blueprint_log', log_id,
                 {'owner': data['owner'], 'date': data['date'], 'score': compliance_score})
        
        return {'id': log_id, 'compliance_score': compliance_score, 'status': 'updated' if existing else 'created'}
    
    def get_blueprint_logs(self, user_id: str, owner: str = None,
                          start_date: str = None, end_date: str = None,
                          limit: int = 30) -> List[Dict]:
        """Get Blueprint logs"""
        query = """
            SELECT * FROM blueprint_logs
            WHERE 1=1
        """
        params = []
        
        if owner:
            query += " AND owner = ?"
            params.append(owner)
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC LIMIT ?"
        params.append(limit)
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        logs = []
        for row in rows:
            log = dict(row)
            if log.get('supplement_list'):
                log['supplement_list'] = json.loads(log['supplement_list'])
            if log.get('meals_logged'):
                log['meals_logged'] = json.loads(log['meals_logged'])
            logs.append(log)
        
        return logs
    
    def get_blueprint_log(self, log_date: str, owner: str, user_id: str) -> Optional[Dict]:
        """Get Blueprint log for a specific date"""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM blueprint_logs WHERE date = ? AND owner = ?",
                (log_date, owner)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            log = dict(row)
            if log.get('supplement_list'):
                log['supplement_list'] = json.loads(log['supplement_list'])
            if log.get('meals_logged'):
                log['meals_logged'] = json.loads(log['meals_logged'])
            
            return log
    
    def _calculate_blueprint_score(self, data: Dict) -> int:
        """Calculate Blueprint compliance score (0-100)"""
        score = 0
        if data.get('supplements_taken'):
            score += 20
        if data.get('super_veggie_eaten'):
            score += 20
        if data.get('nutty_pudding_eaten'):
            score += 20
        if data.get('exercise_done'):
            score += 20
        if data.get('water_intake_ml', 0) >= 2500:
            score += 20
        return score
    
    # ========== WORKOUTS ==========
    
    def log_workout(self, data: Dict, user_id: str) -> Dict:
        """Log a workout"""
        workout_id = f"wrk_{generate_uuid()}"
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO workouts
                   (id, owner, workout_type, location, duration_minutes,
                    total_volume_kg, avg_rpe, prs_achieved, exercises)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    workout_id,
                    data['owner'],
                    data['workout_type'],
                    data.get('location'),
                    data.get('duration_minutes', 0),
                    data.get('total_volume_kg', 0),
                    data.get('avg_rpe'),
                    json.dumps(data.get('prs_achieved', [])),
                    json.dumps(data.get('exercises', []))
                )
            )
        
        log_audit(user_id, 'vessel', 'create', 'workout', workout_id,
                 {'owner': data['owner'], 'type': data['workout_type']})
        
        return {'id': workout_id, 'status': 'logged'}
    
    def get_workouts(self, user_id: str, owner: str = None,
                    workout_type: str = None, days: int = 30) -> List[Dict]:
        """Get workout history"""
        query = """
            SELECT * FROM workouts
            WHERE timestamp > datetime('now', ?)
        """
        params = [f'-{days} days']
        
        if owner:
            query += " AND owner = ?"
            params.append(owner)
        
        if workout_type:
            query += " AND workout_type = ?"
            params.append(workout_type)
        
        query += " ORDER BY timestamp DESC"
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        workouts = []
        for row in rows:
            workout = dict(row)
            if workout.get('prs_achieved'):
                workout['prs_achieved'] = json.loads(workout['prs_achieved'])
            if workout.get('exercises'):
                workout['exercises'] = json.loads(workout['exercises'])
            workouts.append(workout)
        
        return workouts
    
    def get_workout_stats(self, owner: str, days: int = 30) -> Dict:
        """Get workout statistics"""
        workouts = self.get_workouts('system', owner=owner, days=days)
        
        if not workouts:
            return {
                'total_workouts': 0,
                'total_minutes': 0,
                'avg_rpe': 0,
                'by_type': {},
                'prs_count': 0
            }
        
        total_minutes = sum(w['duration_minutes'] for w in workouts)
        avg_rpe = sum(w['avg_rpe'] or 0 for w in workouts) / len(workouts)
        
        # Count by workout type
        by_type = Counter(w['workout_type'] for w in workouts)
        
        # Count PRs
        prs_count = sum(len(w.get('prs_achieved', [])) for w in workouts)
        
        return {
            'total_workouts': len(workouts),
            'total_minutes': total_minutes,
            'avg_rpe': round(avg_rpe, 1),
            'by_type': dict(by_type),
            'prs_count': prs_count
        }
    
    # ========== BIOMETRICS ==========
    
    def log_biometrics(self, data: Dict, user_id: str) -> Dict:
        """Log biometric data"""
        bio_id = f"bio_{generate_uuid()}"
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO biometrics
                   (id, owner, date, sleep_score, sleep_hours, deep_sleep_pct,
                    hrv, resting_hr, recovery_score, weight_kg, body_fat_pct, device_source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    bio_id,
                    data['owner'],
                    data['date'],
                    data.get('sleep_score'),
                    data.get('sleep_hours'),
                    data.get('deep_sleep_pct'),
                    data.get('hrv'),
                    data.get('resting_hr'),
                    data.get('recovery_score'),
                    data.get('weight_kg'),
                    data.get('body_fat_pct'),
                    data.get('device_source')
                )
            )
        
        log_audit(user_id, 'vessel', 'create', 'biometrics', bio_id,
                 {'owner': data['owner'], 'date': data['date']})
        
        return {'id': bio_id, 'status': 'logged'}
    
    def get_biometrics(self, user_id: str, owner: str = None,
                      days: int = 30) -> List[Dict]:
        """Get biometric history"""
        query = """
            SELECT * FROM biometrics
            WHERE date > date('now', ?)
        """
        params = [f'-{days} days']
        
        if owner:
            query += " AND owner = ?"
            params.append(owner)
        
        query += " ORDER BY date DESC"
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_biometric_trends(self, owner: str, days: int = 30) -> Dict:
        """Get biometric trends and averages"""
        biometrics = self.get_biometrics('system', owner=owner, days=days)
        
        if not biometrics:
            return {
                'avg_sleep_score': 0,
                'avg_sleep_hours': 0,
                'avg_hrv': 0,
                'avg_resting_hr': 0,
                'avg_recovery_score': 0,
                'avg_weight': 0,
                'weight_change': 0,
                'trend': 'unknown'
            }
        
        # Calculate averages
        sleep_scores = [b['sleep_score'] for b in biometrics if b['sleep_score']]
        sleep_hours = [b['sleep_hours'] for b in biometrics if b['sleep_hours']]
        hrv_values = [b['hrv'] for b in biometrics if b['hrv']]
        resting_hr = [b['resting_hr'] for b in biometrics if b['resting_hr']]
        recovery_scores = [b['recovery_score'] for b in biometrics if b['recovery_score']]
        weights = [b['weight_kg'] for b in biometrics if b['weight_kg']]
        
        avg_sleep_score = sum(sleep_scores) / len(sleep_scores) if sleep_scores else 0
        avg_sleep_hours = sum(sleep_hours) / len(sleep_hours) if sleep_hours else 0
        avg_hrv = sum(hrv_values) / len(hrv_values) if hrv_values else 0
        avg_resting_hr = sum(resting_hr) / len(resting_hr) if resting_hr else 0
        avg_recovery = sum(recovery_scores) / len(recovery_scores) if recovery_scores else 0
        avg_weight = sum(weights) / len(weights) if weights else 0
        
        # Calculate weight change (first vs last)
        weight_change = 0
        if len(weights) >= 2:
            weight_change = weights[0] - weights[-1]  # Recent - oldest
        
        # Determine trend (recovery score based)
        if recovery_scores:
            recent_avg = sum(recovery_scores[:len(recovery_scores)//3]) / (len(recovery_scores)//3 or 1)
            early_avg = sum(recovery_scores[-len(recovery_scores)//3:]) / (len(recovery_scores)//3 or 1)
            
            if recent_avg > early_avg + 5:
                trend = 'improving'
            elif recent_avg < early_avg - 5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'
        
        return {
            'avg_sleep_score': round(avg_sleep_score, 1),
            'avg_sleep_hours': round(avg_sleep_hours, 1),
            'avg_hrv': round(avg_hrv, 1),
            'avg_resting_hr': round(avg_resting_hr, 1),
            'avg_recovery_score': round(avg_recovery, 1),
            'avg_weight': round(avg_weight, 1),
            'weight_change_kg': round(weight_change, 1),
            'trend': trend
        }
    
    # ========== SOBRIETY TRACKER ==========
    
    def start_sobriety_tracker(self, data: Dict, user_id: str) -> Dict:
        """Start tracking sobriety for a habit"""
        tracker_id = f"sob_{generate_uuid()}"
        
        start_date = data['start_date']
        
        with get_db() as conn:
            # Check if tracker already exists for this habit
            existing = conn.execute(
                "SELECT id FROM sobriety_tracker WHERE owner = ? AND habit_type = ?",
                (data['owner'], data['habit_type'])
            ).fetchone()
            
            if existing:
                return {'error': 'Tracker already exists for this habit'}
            
            conn.execute(
                """INSERT INTO sobriety_tracker
                   (id, owner, habit_type, start_date, current_streak_days,
                    longest_streak_days, relapse_log, why_i_started)
                   VALUES (?, ?, ?, ?, 0, 0, ?, ?)""",
                (
                    tracker_id,
                    data['owner'],
                    data['habit_type'],
                    start_date,
                    json.dumps([]),
                    data.get('why_i_started')
                )
            )
        
        log_audit(user_id, 'vessel', 'create', 'sobriety_tracker', tracker_id,
                 {'owner': data['owner'], 'habit': data['habit_type']})
        
        # Update streak
        self._update_sobriety_streak(tracker_id)
        
        return {'id': tracker_id, 'status': 'created'}
    
    def get_sobriety_tracker(self, tracker_id: str, user_id: str) -> Optional[Dict]:
        """Get sobriety tracker status"""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM sobriety_tracker WHERE id = ?",
                (tracker_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            tracker = dict(row)
            if tracker.get('relapse_log'):
                tracker['relapse_log'] = json.loads(tracker['relapse_log'])
            
            return tracker
    
    def log_relapse(self, tracker_id: str, relapse_data: Dict, user_id: str) -> Dict:
        """Log a relapse"""
        tracker = self.get_sobriety_tracker(tracker_id, user_id)
        if not tracker:
            return {'error': 'Tracker not found'}
        
        relapse_entry = {
            'date': relapse_data['relapse_date'],
            'reason': relapse_data.get('reason'),
            'triggers': relapse_data.get('triggers', []),
            'cost': relapse_data.get('cost', 0)
        }
        
        # Update tracker
        with get_db() as conn:
            # Update last relapse
            conn.execute(
                "UPDATE sobriety_tracker SET last_relapse = ? WHERE id = ?",
                (relapse_data['relapse_date'], tracker_id)
            )
            
            # Add to relapse log (tracker['relapse_log'] is already a list from get_sobriety_tracker)
            relapse_log = tracker['relapse_log'] if isinstance(tracker['relapse_log'], list) else []
            relapse_log.append(relapse_entry)
            conn.execute(
                "UPDATE sobriety_tracker SET relapse_log = ? WHERE id = ?",
                (json.dumps(relapse_log), tracker_id)
            )
        
        # Recalculate streak
        self._update_sobriety_streak(tracker_id)
        
        log_audit(user_id, 'vessel', 'log_relapse', 'sobriety_tracker', tracker_id,
                 {'habit': tracker['habit_type'], 'date': relapse_data['relapse_date']})
        
        return {'id': tracker_id, 'status': 'relapse_logged'}
    
    def _update_sobriety_streak(self, tracker_id: str):
        """Update sobriety streak calculation"""
        tracker = self.get_sobriety_tracker(tracker_id, 'system')
        if not tracker:
            return
        
        today = date.today()
        
        # Calculate current streak
        if tracker['last_relapse']:
            last_relapse_date = datetime.strptime(tracker['last_relapse'], '%Y-%m-%d').date()
            current_streak = (today - last_relapse_date).days - 1
            if current_streak < 0:
                current_streak = 0
        else:
            start_date = datetime.strptime(tracker['start_date'], '%Y-%m-%d').date()
            current_streak = (today - start_date).days
        
        # Update longest streak if needed
        longest_streak = max(tracker['longest_streak_days'], current_streak)
        
        # Calculate savings (placeholder - would need habit-specific cost per day)
        # For now, set to 0
        savings = 0
        
        with get_db() as conn:
            conn.execute(
                """UPDATE sobriety_tracker
                   SET current_streak_days = ?, longest_streak_days = ?, savings_calculated = ?
                   WHERE id = ?""",
                (current_streak, longest_streak, savings, tracker_id)
            )
    
    # ========== ANALYTICS ==========
    
    def get_analytics(self, owner: str, days: int = 30) -> Dict:
        """Get overall health analytics"""
        # Blueprint compliance
        blueprint_logs = self.get_blueprint_logs('system', owner=owner, limit=days)
        avg_compliance = 0
        if blueprint_logs:
            avg_compliance = sum(log['compliance_score'] for log in blueprint_logs) / len(blueprint_logs)
        
        # Workout stats
        workout_stats = self.get_workout_stats(owner, days=days)
        
        # Biometric trends
        biometric_trends = self.get_biometric_trends(owner, days=days)
        
        # Generate insights
        insights = []
        
        if avg_compliance < 60:
            insights.append("Blueprint compliance is below 60% - focus on daily habits")
        elif avg_compliance > 90:
            insights.append("Excellent Blueprint compliance - keep it up!")
        
        if workout_stats['total_workouts'] < 8:  # Less than 2x/week on average
            insights.append(f"Workout frequency is low ({workout_stats['total_workouts']} in {days} days)")
        
        if biometric_trends['avg_recovery_score'] < 60:
            insights.append("Recovery score is low - prioritize rest and sleep")
        
        if biometric_trends['trend'] == 'declining':
            insights.append("Health metrics are declining - review lifestyle factors")
        elif biometric_trends['trend'] == 'improving':
            insights.append("Health metrics are improving - great progress!")
        
        return {
            'owner': owner,
            'period_days': days,
            'blueprint': {
                'avg_compliance': round(avg_compliance, 1),
                'logged_days': len(blueprint_logs)
            },
            'workouts': workout_stats,
            'biometrics': biometric_trends,
            'insights': insights
        }
    
    # ========== STATISTICS ==========
    
    def get_stats(self, user_id: str, owner: str = None) -> Dict:
        """Get Vessel module statistics"""
        with get_db() as conn:
            # Blueprint logs
            blueprint_30d = conn.execute(
                """SELECT COUNT(*) as count
                   FROM blueprint_logs
                   WHERE date > date('now', '-30 days')"""
            ).fetchone()['count']
            
            # Workouts
            workouts_30d = conn.execute(
                """SELECT COUNT(*) as count
                   FROM workouts
                   WHERE timestamp > datetime('now', '-30 days')"""
            ).fetchone()['count']
            
            # Biometrics
            biometrics_30d = conn.execute(
                """SELECT COUNT(*) as count
                   FROM biometrics
                   WHERE date > date('now', '-30 days')"""
            ).fetchone()['count']
            
            # Sobriety trackers
            sobriety_trackers = conn.execute(
                "SELECT COUNT(*) as count FROM sobriety_tracker"
            ).fetchone()['count']
            
            # Longest streak
            longest_streak = conn.execute(
                "SELECT MAX(longest_streak_days) as max_streak FROM sobriety_tracker"
            ).fetchone()['max_streak'] or 0
            
            return {
                'blueprint_logs_30d': blueprint_30d,
                'workouts_30d': workouts_30d,
                'biometrics_30d': biometrics_30d,
                'sobriety_trackers': sobriety_trackers,
                'longest_sobriety_streak_days': longest_streak
            }
