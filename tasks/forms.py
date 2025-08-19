from django import forms
from .models import Task


class TaskCreationForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    title = forms.CharField(max_length=300)
    description = forms.CharField(required=False, widget=forms.Textarea)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, initial="medium")

    class Meta:
        model = Task
        fields = ("title", "description", "priority", "due_date")
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }