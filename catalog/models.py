from django.db import models
from django.urls import reverse


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Project(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])


class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested')
    )
    purpose = models.TextField(max_length=150)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author")
    worker = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="worker")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.purpose

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


class Description(models.Model):
    description = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('description-detail', args=[str(self.id)])
