from django.test import TestCase
from ..models import Users,Projects,Tasks,Description
from datetime import date
from django.urls import reverse

class ModelTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create(first_name='TestName', last_name='TestFam')
        self.project = Projects.objects.create(name='TestProject', author=self.user)
        worker = Users.objects.create(first_name='TestNameWorker', last_name='TestFamWorker')
        self.task = Tasks.objects.create(purpose= 'TestPurpose', project= self.project, status= 'New', author= self.user, worker= worker, added_at= date.today())
        self.description = Description(description = 'TestDescription', task = self.task, author = self.user, added_at = date.today())


    def test_str_Users(self):
        self.assertEqual(str(self.user), 'TestName TestFam')

    def test_str_Projects(self):
        self.assertEqual(str(self.project), 'TestProject')

    def test_str_Tasks(self):
        self.assertEqual(str(self.task), 'TestPurpose')

    def test_get_absolute_url_Tasks(self):
        self.assertEqual(self.task.get_absolute_url(), '/task/'+str(self.task.id))

    def test_str_Description(self):
        self.assertEqual(str(self.description), 'TestDescription')

    def test_length_fields(self):
        user_first_name_length = self.user._meta.get_field('first_name').max_length
        user_last_name_length = self.user._meta.get_field('last_name').max_length
        project_name_length = self.project._meta.get_field('name').max_length
        task_purpose_length = self.task._meta.get_field('purpose').max_length
        task_status_length = self.task._meta.get_field('status').max_length
        description_length = self.description._meta.get_field('description').max_length
        self.assertEqual(user_first_name_length, 30)
        self.assertEqual(user_last_name_length, 30)
        self.assertEqual(project_name_length, 30)
        self.assertEqual(task_purpose_length, 150)
        self.assertEqual(task_status_length, 15)
        self.assertEqual(description_length, 500)


