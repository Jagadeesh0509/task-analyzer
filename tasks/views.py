import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from .models import Task
from .scoring import calculate_priority_score

@csrf_exempt
def analyze_tasks(request):
    """ POST: Calculate scores AND Save to DB (Preventing Duplicates) """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            processed_tasks = []

            for task_data in data:
                # 1. Save or Update to DB
                # This prevents duplicates if you analyze the same JSON twice
                Task.objects.update_or_create(
                    title=task_data.get('title'),
                    due_date=task_data.get('due_date'),
                    defaults={
                        'estimated_hours': task_data.get('estimated_hours'),
                        'importance': task_data.get('importance', 5),
                        'dependencies': task_data.get('dependencies', [])
                    }
                )

                # 2. Calculate Score
                scored_task = calculate_priority_score(task_data)
                processed_tasks.append(scored_task)
            
            # 3. Sort
            sorted_tasks = sorted(processed_tasks, key=lambda x: x['score'], reverse=True)
            return JsonResponse(sorted_tasks, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST required'}, status=405)


def suggest_tasks(request):
    """ GET: Fetch top 3 from DB """
    try:
        tasks = list(Task.objects.all().values())
        if not tasks:
            return JsonResponse({'date': str(date.today()), 'suggestions': [], 'message': 'Database empty'})

        scored = [calculate_priority_score(t) for t in tasks]
        top_3 = sorted(scored, key=lambda x: x['score'], reverse=True)[:3]
        
        return JsonResponse({'date': str(date.today()), 'suggestions': top_3})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)