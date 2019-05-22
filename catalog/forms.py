from django.forms import ModelForm, Form
from django import forms
from catalog.models import Task, Description, Project, User


class CreateNewTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['purpose', 'project', 'status', 'author', 'worker']
        labels = {
            'purpose': 'Task purpose',
            'project': 'Own project',
            'status': 'Current status',
            'author': 'Task author',
            'worker': 'Executor',
        }


class FilterTaskForm(Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False)
    author = forms.ModelChoiceField(User.objects.all(), required=False)
    worker = forms.ModelChoiceField(User.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested'),
        (None, '------')), required=False)
    search_text = forms.CharField(max_length=150, required=False)


class CreateNewDescriptionForm(ModelForm):
    class Meta:
        model = Description
        fields = ['description', 'author']
        labels = {
            'description': 'Your description(comment)',
            'author': 'You are',
        }


class UpdateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'worker']
        labels = {
            'status': 'Select new status',
            'worker': 'Select new executor',
        }
