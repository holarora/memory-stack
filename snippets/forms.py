from django import forms
from .models import Task, Step

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["taskName", "memo", "duedate"]
        labels = {
            "taskName": "Task Name",
            "memo": "Your Memo",
            'duedate': "Due Date",
        }
        error_messages = {
            "taskName": {
                "required": "Your task must not be empty!",
                "max_length": "Please enter a shorter task name!"
            }
        }
        widgets = {
            'duedate': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["taskName", "memo", "duedate"]
        labels = {
            "taskName": "Task Name",
            "memo": "Your Memo",
            'duedate': "Due Date",
        }
        error_messages = {
            "taskName": {
                "required": "Your task must not be empty!",
                "max_length": "Please enter a shorter task name!"
            }
        }
        widgets = {
            'duedate': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ["description"]
        labels = {
            "description": "Step description",
        }
        error_messages = {
            "description": {
                "required": "Your step must not be empty!",
            }
        }

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')