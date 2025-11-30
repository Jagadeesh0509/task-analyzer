from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_priority_score

class ScoringEngineTest(TestCase):
    
    def test_overdue_task_is_critical(self):
        """Test that past due dates trigger the highest urgency score"""
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        task = {
            'title': 'Overdue Task', 
            'due_date': yesterday, 
            'estimated_hours': 5, 
            'importance': 5
        }
        result = calculate_priority_score(task)
        # Base urgency (150) + Importance(30) = 180+
        self.assertTrue(result['score'] >= 150)
        self.assertIn("OVERDUE", result['explanation'])

    def test_quick_win_bonus(self):
        """Test that tasks under 2 hours get a bonus"""
        future_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        task = {
            'title': 'Quick Task',
            'due_date': future_date,
            'estimated_hours': 1.0, 
            'importance': 5
        }
        result = calculate_priority_score(task)
        self.assertIn("Quick Win", result['explanation'])

    def test_dependency_penalty(self):
        """Test that blocked tasks receive a score penalty"""
        future_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        task = {
            'title': 'Blocked Task',
            'due_date': future_date,
            'estimated_hours': 5,
            'importance': 5,
            'dependencies': [1, 2] # Has dependencies
        }
        result = calculate_priority_score(task)
        self.assertIn("Blocked", result['explanation'])

    def test_invalid_date_handling(self):
        """Edge Case: Ensure the system doesn't crash on bad dates"""
        task = {
            'title': 'Bad Date Task',
            'due_date': 'not-a-date',
            'estimated_hours': 5
        }
        try:
            result = calculate_priority_score(task)
            self.assertIsNotNone(result['score'])
        except Exception:
            self.fail("Algorithm crashed on invalid date input")