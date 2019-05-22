from django.shortcuts import render, redirect
from django.views import generic
<<<<<<< HEAD
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from catalog.models import User, Task, Project, Description
from catalog.forms import CreateNewTaskForm, CreateNewDescriptionForm, \
    UpdateTaskForm, FilterTaskForm
from catalog.serializers import UserSerializer, ProjectSerializer, \
    TaskSerializer, DescriptionSerializer

# API


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TasksList(generics.ListCreateAPIView):
    model = Task
    queryset = Task.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('project', 'author', 'status', 'worker', 'added_at')
    serializer_class = TaskSerializer
    search_fields = ('purpose', 'status')


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DescriptionList(generics.ListCreateAPIView):
    model = Description
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        task_pk = self.kwargs['pk']
        task = Task.objects.get(id=task_pk)
        queryset = Description.objects.filter(task=task).all()
        return queryset


class DescriptionDetail(generics.RetrieveAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class DescriptionStatistics(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        task_pk = self.kwargs['pk']
        task = Task.objects.get(id=task_pk)
        stat = statistics_dump(Description.objects.filter(task=task).all())
        return Response(stat)

# RENDERING IN TEMPLATES

=======
from .models import Users, Tasks, Projects, Description
from .forms import CreateNewTask, CreateNewDescription, UpdateTask, FilterTask
from django.db.models import Count

import random
from datetime import date
>>>>>>> 6f8fe3e3c48cb7df81d56b22aea08c3df06c58ec

def create_task(request):
    if request.method == 'GET':
        form = CreateNewTaskForm()
        return render(request, 'create_task_form.html', {'form': form})
    elif request.method == 'POST':
        form = CreateNewTaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('root')
    return HttpResponseNotAllowed(['POST', 'GET'])


def delete_task(request, pk):
    if request.method == 'DELETE' or request.method == 'POST':
        task = get_object_or_404(Task, id=pk)
        task.delete()
        return redirect('root')
    return HttpResponseNotAllowed(['POST'])


def update_task(request, pk):
    if request.method == 'GET':
        form = UpdateTaskForm()
        return render(request, 'update_task_form.html', {'form': form})
    elif request.method == 'POST':
        form = UpdateTaskForm(request.POST)
        task = Task.objects.get(id=pk)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            new_worker = form.cleaned_data['worker']
            task.status = new_status
            task.worker = new_worker
            task.save()
        return redirect('task-detail', pk=pk)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


def create_description(request, pk):
    if request.method == 'GET':
        form = CreateNewDescriptionForm()
        return render(request, 'create_description_form.html', {'form': form})
    elif request.method == 'POST':
        form = CreateNewDescriptionForm(request.POST)
        task = Task.objects.get(id=pk)
        if form.is_valid():
            new_desc = form.cleaned_data['description']
            author = form.cleaned_data['author']
            description = Description(description=new_desc, author=author,
                                      task=task)
            description.save()
        return redirect(task.get_absolute_url())
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


def tasks_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        form = FilterTaskForm(request.GET)
        if form.is_valid():
            tasks = tasks_filter(project=form.cleaned_data['project'],
                                 author=form.cleaned_data['author'],
                                 worker=form.cleaned_data['worker'],
                                 status=form.cleaned_data['status'],
                                 search_text=form.cleaned_data['search_text'])
        return render(request, 'catalog/tasks_list.html',
                      {'tasks_list': tasks, 'form': form})
    return HttpResponseNotAllowed(['GET'])


class TaskDetailView(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task_descriptions = Description.objects.filter(
            task__id=self.kwargs['pk'])
        context['all_descriptions'] = task_descriptions
        statistics = statistics_dump(task_descriptions)
        context['statistics'] = statistics
        return context


def tasks_filter(**kwargs):
    tasks = Task.objects.all()
    if kwargs.get('project'):
        tasks = tasks.filter(project=kwargs.get('project'))
    if kwargs.get('author'):
        tasks = tasks.filter(author=kwargs.get('author'))
    if kwargs.get('worker'):
        tasks = tasks.filter(worker=kwargs.get('worker'))
    if kwargs.get('status'):
        tasks = tasks.filter(status=kwargs.get('status'))
    if kwargs.get('search_text'):
        tasks = tasks.filter(purpose__icontains=kwargs.get('search_text'))
    return tasks


def statistics_dump(descriptions):
    statistic = {}
    for descr in descriptions:
        key = descr.added_at.date().strftime("%Y-%m-%d")
        if key in statistic:
            statistic[key][0] += 1
            statistic[key][1].append(descr.author)
        else:
            statistic[key] = [1, [descr.author]]
    for day in statistic:
        statistic[day][1] = len(set(statistic[day][1]))
    return statistic
