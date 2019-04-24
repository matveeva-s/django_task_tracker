from django.shortcuts import render
from django.views import generic
from .models import Users, Tasks, Projects, Description
from .forms import CreateNewTask, CreateNewDescription, UpdateTask, FilterTask
from django.db.models import Count

import random
from datetime import date

def fill_test_base(request):
    for i in range(10):
        firstname = 'name'+str(i+1)
        lastname = 'fam'+str(i+1)
        user=Users(id = i+1, first_name= firstname, last_name= lastname)
        user.save()
        print(user.id)
    for i in range(5):
        proj_name = 'project' + str(i+1)
        author = Users.objects.get(id = random.randint(1,10))
        project = Projects(name = proj_name, author = author)
        project.save()
        for j in range(10):
            purpose = 'task' + str(j+1)
            status = random.choice(['New', 'In progress', 'Ready', 'Completed', 'Canceled', 'Being tested'])
            worker = Users.objects.get(id=random.randint(1, 10))
            author = Users.objects.get(id=random.randint(1, 10))
            added_at = date(2019, 4, random.choice([16,17,18,19]))
            task = Tasks(purpose = purpose, project = project, status = status, author = author, worker = worker, added_at = added_at)
            task.save()
            for k in range(5):
                descr = 'description' + str(k+1)
                author = Users.objects.get(id=random.randint(1, 10))
                added_at = date(2019, 4, random.choice([20, 21, 22]))
                description = Description(description = descr, author = author, task = task, added_at= added_at)
                description.save()
    return render(request, 'task_added.html', {'text': 'Test base successfully created!'})

def create_task(request):
    if request.method == 'GET':
        form = CreateNewTask()
        return render(request, 'create_task_form.html', {'form': form})
    else:
        form = CreateNewTask(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'task_added.html', {'text': 'Task successfully added!'})

def delete_task(request, pk):
    Tasks.objects.get(id = pk).delete()
    return render(request, 'task_deleted.html')

def update_task(request, pk):
    if request.method == 'GET':
        form = UpdateTask()
        return render(request, 'update_task_form.html', {'form': form})
    else:
        form = UpdateTask(request.POST)
        task = Tasks.objects.get(id=pk)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            new_worker = form.cleaned_data['worker']
            task.status = new_status
            task.worker = new_worker
            task.save()
        return render(request, 'task_added.html', {'text': 'Task successfully updated!'})

def create_description(request, pk):
    if request.method == 'GET':
        form = CreateNewDescription()
        return render(request, 'create_description_form.html', {'form': form})
    else:
        form = CreateNewDescription(request.POST)
        task = Tasks.objects.get(id=pk)
        if form.is_valid():
            new_desc = form.cleaned_data['description']
            author = form.cleaned_data['author']
            description = Description(description = new_desc, author = author, task = task)
            description.save()
        return render(request, 'task_added.html', {'text': 'Description successfully added!'})

def tasks_list(request):
    tasks = Tasks.objects.all()
    url_create_task = 'location.href="http://127.0.0.1:8000/create_task/"'
    form = FilterTask(request.GET)
    if form.is_valid():
        if form.cleaned_data['project']:
            tasks = tasks.filter(project = form.cleaned_data['project'])
        if form.cleaned_data['author']:
            tasks = tasks.filter(author = form.cleaned_data['author'])
        if form.cleaned_data['worker']:
            tasks = tasks.filter(worker = form.cleaned_data['worker'])
        if form.cleaned_data['status']:
            tasks = tasks.filter(status = form.cleaned_data['status'])
        if form.cleaned_data['search_text']:
            tasks = tasks.filter(purpose__icontains = form.cleaned_data['search_text'])
    return render(request, 'catalog/tasks_list.html', {'tasks_list': tasks,'form': form, 'url_create_task': url_create_task})

class TaskDetailView(generic.DetailView):
    model = Tasks
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task_descriptions = Description.objects.filter(task__id = self.kwargs['pk'])
        context['desc'] = task_descriptions
        context['url_add_desc'] = 'location.href="http://127.0.0.1:8000' + self.request.path + '/create_description"'
        context['url_update'] = 'location.href="http://127.0.0.1:8000' + self.request.path + '/update"'
        context['url_delete'] = 'location.href="http://127.0.0.1:8000' + self.request.path + '/delete"'
        descriptions_by_day = task_descriptions.values('added_at').annotate(descs=Count('description'))
        authors_distinct_by_day = task_descriptions.values('added_at').annotate(users = Count('author', distinct = True))
        statistics = []
        for i in range(len(descriptions_by_day)):
            d = {'date': str(descriptions_by_day[i]['added_at']), 'descr_count': descriptions_by_day[i]['descs'], 'authors_count': authors_distinct_by_day[i]['users']}
            statistics.append(d)
        context['statistics'] = statistics
        return context


