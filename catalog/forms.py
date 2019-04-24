from django.forms import ModelForm, Form
from django import forms
from .models import Tasks, Description, Projects, Users

class CreateNewTask(ModelForm):
    class Meta:
        model = Tasks
        fields = ['purpose', 'project', 'status', 'author', 'worker']
        labels = {
            'purpose': 'Task purpose',
            'project': 'Own project',
            'status': 'Current status',
            'author': 'Task author',
            'worker': 'Executor',
        }

class FilterTask(Form):
    project = forms.ModelChoiceField(Projects.objects.all(), required=False)
    author = forms.ModelChoiceField(Users.objects.all(), required=False)
    worker = forms.ModelChoiceField(Users.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested'),
        (None, '------')),
    required=False)
    search_text = forms.CharField(max_length=150, required=False)


class CreateNewDescription(ModelForm):
    class Meta:
        model = Description
        fields = ['description', 'author']
        labels = {
            'description': 'Your description(comment)',
            'author': 'You are',
        }

class UpdateTask(ModelForm):
    class Meta:
        model = Tasks
        fields = ['status', 'worker']
        labels = {
            'status': 'Select new status',
            'worker': 'Select new executor',
        }


