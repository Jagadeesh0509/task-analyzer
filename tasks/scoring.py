from datetime import date, datetime

def calculate_priority_score(task):
    score = 0
    explanation = []
    
    # 1. Parse Date safely
    try:
        d_val = task.get('due_date')
        if isinstance(d_val, str):
            due_date = datetime.strptime(d_val, "%Y-%m-%d").date()
        else:
            due_date = d_val
    except (ValueError, TypeError):
        due_date = date(2099, 12, 31)

    # 2. Urgency
    days_until = (due_date - date.today()).days
    if days_until < 0:
        score += 150
        explanation.append("OVERDUE")
    elif days_until == 0:
        score += 100
        explanation.append("Due Today")
    elif days_until <= 3:
        score += (100 - (days_until * 15))
        explanation.append(f"Due in {days_until} days")
    
    # 3. Importance (x6 multiplier)
    imp = int(task.get('importance', 5))
    score += (imp * 6)
    if imp >= 8: explanation.append("High Importance")

    # 4. Effort (Quick Wins)
    effort = float(task.get('estimated_hours', 0))
    if effort > 0 and effort <= 2:
        score += 20
        explanation.append("Quick Win")
        
    # 5. Dependency Penalty
    if task.get('dependencies'):
        score -= 15
        explanation.append("Blocked")

    task['score'] = round(score, 2)
    task['explanation'] = ", ".join(explanation)
    return task