import random
import json
from django.test import TestCase
from catalog.models import User, Project, Task, Description
from catalog.serializers import UserSerializer, ProjectSerializer, \
    TaskSerializer, DescriptionSerializer


class TasksListViewTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Filter by or search:')
        self.assertContains(resp, 'Tasks list:')
        tasks_number = len(Task.objects.all())
        self.assertEqual(tasks_number, 10)
        for i in range(tasks_number):
            self.assertContains(resp, 'purpose{}'.format(i+1))
            self.assertContains(resp, 'firstname{} lastname{}'.
                                format(i+1, i+1))


class TaskDetailViewTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        tasks_number = len(Task.objects.all())
        for i in range(tasks_number):
            id = i+1
            resp = self.client.get('/task/{}/'.format(id))
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, 'purpose{}'.format(id))
            self.assertContains(resp, 'firstname')
            self.assertContains(resp, 'lastname')
            self.assertContains(resp, 'Create new description')
            self.assertContains(resp, 'Update this task')
            self.assertContains(resp, 'Delete this task')

    def test_DELETE(self):
        id = random.randint(1, len(Task.objects.all()))
        resp = self.client.delete('/task/{}/'.format(id))
        self.assertEqual(resp.status_code, 405)


class CreateTaskViewTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        resp = self.client.get('/create_task/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Please fill out the form to create a task:')
        self.assertContains(resp, 'Task purpose:')
        self.assertContains(resp, 'Submit')

    def test_POST(self):
        data = {
            'purpose': 'some_test_purpose',
            'project': random.randint(1, len(Project.objects.all())),
            'status': 'New',
            'author': random.randint(1, len(User.objects.all())),
            'worker': random.randint(1, len(User.objects.all())),
        }
        resp = self.client.post('/create_task/', data)
        self.assertEqual(resp.status_code, 302)
        new_task_object = Task.objects.filter(purpose='some_test_purpose')
        self.assertIsNotNone(new_task_object)
        self.assertEqual(len(Task.objects.all()), 11)

    def test_PUT(self):
        resp = self.client.put('/create_task/')
        self.assertEqual(resp.status_code, 405)


class CreateDescriptionViewTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.get('/task/{}/create_description/'.format(task_id))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Please fill out the form')
        self.assertContains(resp, 'Submit')

    def test_POST(self):
        task_id = random.randint(1, len(Task.objects.all()))
        author_id = random.randint(1, len(User.objects.all()))
        resp = self.client.post('/task/{}/create_description/'.format(task_id),
                                {
                                    'description': 'some_test_description',
                                    'author': author_id
                                })
        self.assertEqual(resp.status_code, 302)
        new_descr_object = Description.objects.filter(
            description='some_test_purpose')
        self.assertIsNotNone(new_descr_object)
        self.assertEqual(len(Description.objects.all()), 101)

    def test_DELETE(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.delete('/task/{}/create_description/'.
                                  format(task_id))
        self.assertEqual(resp.status_code, 405)


class DeleteTaskViewTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_DELETE(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.delete('/task/{}/delete/'.format(task_id))
        self.assertEqual(resp.status_code, 302)
        deleted_obj = Task.objects.filter(id=task_id)
        self.assertEqual(len(deleted_obj), 0)

    def test_GET(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.get('/task/{}/delete/'.format(task_id))
        self.assertEqual(resp.status_code, 405)


class UpdateTaskViewTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.get('/task/{}/update/'.format(task_id))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Please select new status or executor:')

    def test_POST(self):
        task_id = random.randint(1, len(Task.objects.all()))
        new_worker_id = random.randint(1, len(User.objects.all()))
        resp = self.client.post('/task/{}/update/'.format(task_id),
                                {'status': 'Ready', 'worker': new_worker_id})
        self.assertEqual(resp.status_code, 302)
        task = Task.objects.get(id=task_id)
        self.assertEqual(task.status, 'Ready')
        self.assertEqual(task.worker.id, new_worker_id)

    def test_PUT(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.put('/task/{}/update/'.format(task_id))
        self.assertEqual(resp.status_code, 405)


class API_UserListTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        resp = self.client.get('/API/users/')
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)

    def test_POST(self):
        data = {"first_name": "TestFirstName", "last_name": "TestLastName"}
        resp = self.client.post('/API/users/', data)
        self.assertEqual(resp.status_code, 201)
        new_user = User.objects.get(first_name="TestFirstName")
        self.assertEqual(new_user.last_name, 'TestLastName')


class API_UserDetailTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        user_id = random.randint(1, len(User.objects.all()))
        resp = self.client.get('/API/users/{}/'.format(user_id))
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)


class API_ProjectDetailTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        project_id = random.randint(1, len(Project.objects.all()))
        resp = self.client.get('/API/projects/{}/'.format(project_id))
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)


class API_TaskListTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        resp = self.client.get('/API/tasks/')
        serializer = TaskSerializer(Task.objects.all(), many=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)

    def test_POST(self):
        data = {
            "purpose": "TestPurpose",
            "project": 1,
            "status": "Canceled",
            "author": 5,
            "worker": 7
        }
        resp = self.client.post('/API/tasks/', data)
        self.assertEqual(resp.status_code, 201)
        new_task = Task.objects.get(purpose="TestPurpose")
        self.assertEqual(new_task.status, "Canceled")


class API_TaskDetailTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.get('/API/tasks/{}/'.format(task_id))
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)

    def test_PUT(self):
        task_id = random.randint(1, len(Task.objects.all()))
        data = {
            "status": "Canceled",
            "worker": 5
        }
        resp = self.client.put('/API/tasks/{}/'.format(task_id),
                               data, content_type="application/json")
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)

    def test_DELETE(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.delete('/API/tasks/{}/'.format(task_id))
        task = Task.objects.filter(id=task_id).all()
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(task), 0)


class API_DescriptionListTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        task_id = random.randint(1, len(Task.objects.all()))
        resp = self.client.get('/API/tasks/{}/descriptions/'.format(task_id))
        serializer = DescriptionSerializer(Description.objects.filter(
                                            task_id=task_id).all(), many=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(serializer.data, resp.data)

    def test_POST(self):
        task_id = random.randint(1, len(Task.objects.all()))
        data = {
            "description": "TestDescription",
            "task": task_id,
            "author": 4
        }
        resp = self.client.post('/API/tasks/{}/descriptions/'.format(task_id),
                                data)
        self.assertEqual(resp.status_code, 201)
        new_desc = Description.objects.get(description="TestDescription")
        self.assertEqual(new_desc.author.id, 4)


class API_DescriptionStatisticsTest(TestCase):
    fixtures = ['dumpdata.json']

    def test_GET(self):
        resp = self.client.get('/API/tasks/1/descriptions_statistic/')
        data = {
            '2019-05-09': [4, 3],
            '2019-05-10': [1, 1],
            '2019-05-06': [3, 2],
            '2019-05-07': [1, 1],
            '2019-05-08': [1, 1],
        }
        self.assertEqual(json.dumps(resp.data), json.dumps(data))
