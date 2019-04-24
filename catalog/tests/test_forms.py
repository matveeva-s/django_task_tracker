from django.test import TestCase
from ..forms import CreateNewTask, CreateNewDescription, UpdateTask, FilterTask


class CreateNewTaskFormTest(TestCase):

    def setUp(self):
        self.form = CreateNewTask()

    def test_purpose_field_label(self):
        self.assertTrue(self.form.fields['purpose'].label == 'Task purpose')

    def test_purpose_field_length(self):
        self.assertEqual(self.form.fields['purpose'].max_length, 150)

    def test_project_field_label(self):
        self.assertTrue(self.form.fields['project'].label == 'Own project')

    def test_status_field_label(self):
        self.assertTrue(self.form.fields['status'].label == 'Current status')

    def test_author_field_label(self):
        self.assertTrue(self.form.fields['author'].label == 'Task author')

    def test_worker_field_label(self):
        self.assertTrue(self.form.fields['worker'].label == 'Executor')


class CreateNewDescriptionFormTest(TestCase):

    def setUp(self):
        self.form = CreateNewDescription()

    def test_description_field_label(self):
        self.assertEqual(self.form.fields['description'].label, 'Your description(comment)')

    def test_description_field_length(self):
        self.assertEqual(self.form.fields['description'].max_length, 500)

    def test_author_field_label(self):
        self.assertEqual(self.form.fields['author'].label, 'You are')


class UpdateTaskFormTest(TestCase):

    def setUp(self):
        self.form = UpdateTask()

    def test_status_field_label(self):
        self.assertEqual(self.form.fields['status'].label, 'Select new status')

    def test_worker_field_label(self):
        self.assertEqual(self.form.fields['worker'].label, 'Select new executor')


class FilterTaskFormTest(TestCase):

    def setUp(self):
        self.form = FilterTask()

    def test_search_field_length(self):
        self.assertEqual(self.form.fields['search_text'].max_length, 150)
