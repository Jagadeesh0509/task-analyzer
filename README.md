# Smart Task Analyzer 
A task management system that helps you decide what to work on next. It uses a custom algorithm to score tasks based on deadlines, importance, and effort.

##  Setup Instructions

Follow these steps to run the project on your computer.

### Prerequisites
* Python installed
* Git installed

### Steps
1. **Clone the repository:**
   ```bash
   git clone <PASTE_YOUR_GITHUB_URL_HERE>
   cd task-analyzer
2. Create a virtual environment: Windows
python -m venv tasks
venv\Scripts\activate


3. Setup the Database:

python manage.py makemigrations
python manage.py migrate

4. Run the Server:
   
python manage.py runserver


5. Open the App: Open frontend/index.html in your web browser.


***Algorithm Explanation***

The main goal of this project is to answer the question: "What should I do right now?"

To answer this, I wrote a scoring function in tasks/scoring.py. It assigns a number (Priority Score) to every task. A higher number means you should do it sooner.

The Formula: ***Total Score = Urgency Score + (Importance * 6) + Quick Win Bonus - Dependency Penalty***

Here is how each part works:

1. Urgency (The most important factor) Deadlines are strict constraints, so they have the biggest impact on the score.

Overdue Tasks: If a task is past its due date, it gets +150 points. This guarantees it goes to the top of the list.

Due Today: If it is due today, it gets +100 points.

Due Soon (1-3 days): The score slowly goes down as the date gets further away. For example, a task due tomorrow gets more points than a task due in 3 days.

Future Tasks: If a task is due far in the future, it gets 0 urgency points.

2. Importance (User Rating) The user gives a rating from 1 to 10.

I multiply this rating by 6.

Why? A maximum importance task (10) becomes 60 points. This is high, but not higher than a "Due Today" task (100). This ensures that we prioritize deadlines over general importance.

3. Effort (Quick Wins) I used the "Quick Win" strategy.

If a task takes less than or equal to 2 hours, it gets a +20 point bonus.

Why? If two tasks are equally important, it is better to finish the short one first to clear it off the list.

4. Dependencies (Blocking) Some tasks cannot be started because they are waiting for other tasks.

If a task has a dependency list (it is blocked), I subtract -15 points.

Why? We should not prioritize tasks that we cannot work on yet.




***BULK JSON DATA***

[
    {
        "title": "CRITICAL: Payment Gateway Down",
        "due_date": "2025-11-29",
        "estimated_hours": 4,
        "importance": 10,
        "dependencies": []
    },
    {
        "title": "Update Homepage Banner",
        "due_date": "2025-11-30",
        "estimated_hours": 0.5,
        "importance": 6,
        "dependencies": []
    },
    {
        "title": "Renew SSL Certificate",
        "due_date": "2025-11-30",
        "estimated_hours": 1,
        "importance": 10,
        "dependencies": []
    },
    {
        "title": "Launch v2.0 (Blocked)",
        "due_date": "2025-11-30",
        "estimated_hours": 2,
        "importance": 10,
        "dependencies": [999]
    },
    {
        "title": "Write Weekly Blog Post",
        "due_date": "2025-12-01",
        "estimated_hours": 3,
        "importance": 7,
        "dependencies": []
    },
    {
        "title": "Clean Up Codebase",
        "due_date": "2025-12-05",
        "estimated_hours": 0.5,
        "importance": 3,
        "dependencies": []
    },
    {
        "title": "Interview Intern Candidates",
        "due_date": "2025-12-02",
        "estimated_hours": 1,
        "importance": 8,
        "dependencies": []
    },
    {
        "title": "Refactor Legacy Backend",
        "due_date": "2026-01-01",
        "estimated_hours": 40,
        "importance": 9,
        "dependencies": []
    },
    {
        "title": "Prepare Q4 Financials",
        "due_date": "2025-12-15",
        "estimated_hours": 5,
        "importance": 9,
        "dependencies": []
    },
    {
        "title": "Buy Office Coffee",
        "due_date": "2025-12-10",
        "estimated_hours": 0.2,
        "importance": 2,
        "dependencies": []
    }
]



***Design Decisions & Trade-offs***

1. Using Standard Django instead of DRF

Decision: I used Django's built-in JsonResponse instead of Django Rest Framework (DRF).

Reason: Since the requirements were simple (receive JSON, return JSON), using plain Django was faster to implement and easier to debug. It avoids the complexity of Serializers for a small project.

2. Handling Duplicates

Decision: I used Task.objects.update_or_create().

Reason: If a user clicks "Analyze" twice on the same data, we don't want to fill the database with duplicates. This function updates the task if it exists or creates it if it is new.

3. Dependency Logic

Decision: I used a "Score Penalty" instead of complex Graph Theory.

Reason: Calculating a full dependency tree (Directed Acyclic Graph) is computationally heavy. For a personal task manager, simply penalizing blocked tasks achieves the same goal (pushing them down the list) but keeps the code very fast.



***Future Improvements***

User Login: So different users can have their own private task lists.

Edit/Delete: Buttons on the frontend to remove tasks from the database.

