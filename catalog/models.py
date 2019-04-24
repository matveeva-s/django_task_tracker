from django.db import models
from django.urls import reverse


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    author = models.ForeignKey(Users, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested')
    )
    id = models.AutoField(primary_key=True)
    purpose = models.TextField(max_length=150)
    project = models.ForeignKey(Projects, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    author = models.ForeignKey(Users, on_delete=models.PROTECT)
    worker = models.ForeignKey(Users, on_delete=models.PROTECT, related_name="workers")
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


class Description(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=500)
    task= models.ForeignKey(Tasks, on_delete=models.CASCADE)
    author = models.ForeignKey(Users, on_delete=models.PROTECT)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description
