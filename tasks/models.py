from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(help_text="YYYY-MM-DD")
    estimated_hours = models.FloatField()
    importance = models.IntegerField(default=5, help_text="1-10 Scale")
    dependencies = models.JSONField(default=list, blank=True) 

    def __str__(self):
        return self.title