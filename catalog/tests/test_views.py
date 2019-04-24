from ..models import Users, Projects, Tasks, Description
from django.test import Client, TestCase
from datetime import date


class TasksListViewTest(TestCase):

    def setUp(self):
        user_author = Users.objects.create(first_name='firstnameAuthor', last_name='lastnameAuthor')
        user_worker = Users.objects.create(first_name='firstnameWorker', last_name='lastnameWorker')
        project = Projects.objects.create(name='project_name', author=user_author)
        for i in range(10):
            Tasks.objects.create(purpose='purpose{}'.format(i), project=project, status='New', author=user_author, worker=user_worker, added_at=date.today())
        self.client = Client()

    def test_page_content(self):
        resp = self.client.get('')
        self.assertContains(resp, 'Filter by or search:')
        self.assertContains(resp, 'Tasks list:')
        for i in range(10):
            self.assertContains(resp, 'purpose{}'.format(i))
        self.assertEqual(resp.status_code, 200)


class TaskDetailViewTest(TestCase):

    def setUp(self):
        user_author = Users.objects.create(first_name='firstnameAuthor', last_name='lastnameAuthor')
        user_worker = Users.objects.create(first_name='firstnameWorker', last_name='lastnameWorker')
        project = Projects.objects.create(name='project_name', author=user_author)
        self.task = Tasks.objects.create(purpose='purpose', project=project, status='New', author=user_author, worker=user_worker, added_at=date.today())
        self.client = Client()

    def test_page_content(self):
        id = self.task.id
        resp = self.client.get('/task/{}'.format(id))
        self.assertContains(resp, 'Task:')
        self.assertContains(resp, 'purpose')
        self.assertContains(resp, 'project_name')
        self.assertContains(resp, 'New')
        self.assertContains(resp, 'firstnameWorker lastnameWorker')
        self.assertContains(resp, 'firstnameAuthor lastnameAuthor')
        self.assertContains(resp, 'Comment statistics:')
        self.assertContains(resp, 'Descriptions:')
        self.assertContains(resp, 'Add description')
        self.assertContains(resp, 'Update task')
        self.assertContains(resp, 'Delete task')
        self.assertEqual(resp.status_code, 200)


class CreateTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_content_GET(self):
        resp = self.client.get('/create_task/')
        self.assertContains(resp, 'Please fill out the form to create a task:')
        self.assertContains(resp, 'Task purpose:')
        self.assertContains(resp, 'Submit')
        self.assertEqual(resp.status_code, 200)

    def test_page_content_POST(self):
        user_author = Users.objects.create(first_name='firstnameAuthor', last_name='lastnameAuthor')
        user_worker = Users.objects.create(first_name='firstnameWorker', last_name='lastnameWorker')
        project = Projects.objects.create(name='project_name', author=user_author)
        data = {'purpose': 'some_purpose', 'project': project, 'status': 'New', 'author': user_author, 'worker': user_worker}
        resp = self.client.post('/create_task/', data)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Task successfully added!')
        self.assertContains(resp, 'Return to tasks')

class CreateDescriptionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        user_author = Users.objects.create(first_name='firstnameAuthor', last_name='lastnameAuthor')
        user_worker = Users.objects.create(first_name='firstnameWorker', last_name='lastnameWorker')
        self.user = user_worker
        project = Projects.objects.create(name='project_name', author=user_author)
        project.save()
        self.task = Tasks.objects.create(purpose='some_purpose', project=project, status='New', author=user_author,
                                    worker=user_worker)

    def test_page_content(self):
        resp = self.client.get('/task/{}/create_description/'.format(self.task.id))
        self.assertContains(resp, 'Please fill out the form to create a description:')
        self.assertContains(resp, 'Your description(comment):')
        self.assertContains(resp, 'Submit')
        self.assertEqual(resp.status_code, 200)

    def test_page_content_POST(self):
        resp = self.client.post('/task/{}/create_description/'.format(self.task.id), {'description': 'TestDescription', 'author': self.user})
        self.assertContains(resp, 'Description successfully added!')
        self.assertEqual(resp.status_code, 200)


class DeleteTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_content(self):
        user_author = Users(first_name='firstnameAuthor', last_name='lastname')
        user_worker = Users(first_name='firstnameWorker', last_name='lastnameWorker')
        user_worker.save()
        user_author.save()
        project = Projects(name='proj_name', author=user_author)
        project.save()
        task = Tasks.objects.create(purpose='some_purpose', project= project, status= 'New', author= user_author, worker= user_worker)
        resp = self.client.get('/task/{}/delete/'.format(task.id))
        self.assertContains(resp, 'Task was deleted!')
        self.assertContains(resp, 'Return to tasks')
        self.assertEqual(resp.status_code, 200)

class UpdateTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        user_author = Users.objects.create(first_name='firstnameAuthor', last_name='lastnameAuthor')
        user_worker = Users.objects.create(first_name='firstnameWorker', last_name='lastnameWorker')
        self.user = user_author
        project = Projects.objects.create(name='proj_name', author=user_author)
        self.task = Tasks.objects.create(purpose='some_purpose', project=project, status='New', author=user_author,
                                    worker=user_worker)

    def test_page_content_GET(self):
        resp = self.client.get('/task/{}/update/'.format(self.task.id))
        self.assertContains(resp, 'Please select new status or executor:')
        self.assertContains(resp, 'Select new')
        self.assertContains(resp, 'Update')
        self.assertEqual(resp.status_code, 200)


    def test_page_content_POST(self):
        resp = self.client.post('/task/{}/update/'.format(self.task.id), {'status': 'Ready', 'worker': self.user_author})
        self.assertContains(resp, 'Task successfully updated!')
        self.assertContains(resp, 'Return to tasks')
        self.assertEqual(resp.status_code, 200)
