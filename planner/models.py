from django.db import models
from account.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField()  # Duration in minutes
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Day(models.Model):
    date = models.DateField()
    tasks = models.ManyToManyField(Task)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_hours(self):
        total_minutes = sum(task.duration_minutes for task in self.tasks.all())
        return total_minutes / 60

    def __str__(self):
        return f"{self.date}"


class Week(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.ManyToManyField(Day)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_hours(self):
        total_minutes = sum(day.total_hours() * 60 for day in self.days.all())
        return total_minutes / 60

    def __str__(self):
        return f"start : {self.start_date}, End : {self.end_date}"
