from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from snippets.models import Task, Step
from snippets.forms import SearchForm, TaskForm, StepForm

class AllTasksTests(TestCase):

    def setUp(self):
        self.task1 = Task.objects.create(
            taskName="Task One",
            duedate=timezone.now() + timezone.timedelta(days=1),
            memo="First task",
        )
        self.task2 = Task.objects.create(
            taskName="Task Two",
            duedate=timezone.now() + timezone.timedelta(days=2),
            memo="Second task",
        )
        self.search_url = reverse('alltasks')
        self.create_task_url = reverse('alltasks')

    def test_alltasks_get(self):
        """Test that the alltasks page renders with the correct template and context"""
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "snippets/alltasks.html")
        self.assertContains(response, "Task One")
        self.assertContains(response, "Task Two")
        self.assertIsInstance(response.context['search_form'], SearchForm)
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_search_tasks(self):
        """Test that searching for tasks filters results correctly"""
        response = self.client.get(self.search_url, {'query': 'One'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task One")
        self.assertNotContains(response, "Task Two")

    def test_post_create_task(self):
        """Test that submitting a valid POST request creates a new task"""
        post_data = {
            'taskName': 'New Task',
            'duedate': timezone.now() + timezone.timedelta(days=3),
            'memo': 'New task memo'
        }
        response = self.client.post(self.create_task_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(taskName='New Task').exists())

    def test_post_create_task_invalid(self):
        """Test that submitting an invalid POST request does not create a new task"""
        post_data = {
            'taskName': '',
            'duedate': '',
            'memo': ''
        }
        response = self.client.post(self.create_task_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(taskName='').exists())


class OneTaskViewTests(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            taskName="Sample Task",
            duedate=timezone.now() + timezone.timedelta(days=1),
            memo="This is a sample task",
        )
        self.step_form_url = reverse("onetask", args=[self.task.slug])
        self.valid_step_data = {
            'description': 'Step description',
        }

    def test_onetask_get(self):
        """Test that the one task page renders with correct template and context"""
        response = self.client.get(self.step_form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "snippets/task.html")
        self.assertContains(response, self.task.taskName)
        self.assertContains(response, self.task.memo)
        self.assertIsInstance(response.context['form'], StepForm)

    def test_onetask_post_valid(self):
        """Test that submitting a valid POST request adds a new step to the task"""
        response = self.client.post(self.step_form_url, self.valid_step_data)
        self.assertEqual(response.status_code, 302)
        step = Step.objects.get(description='Step description')
        self.assertEqual(step.task, self.task)
        self.assertEqual(Step.objects.count(), 1)

    def test_onetask_post_invalid(self):
        """Test that submitting an invalid POST request does not add a new step"""
        invalid_data = {
            'description': ''
        }
        response = self.client.post(self.step_form_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Step.objects.filter(description='').exists())


class EditTaskTests(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            taskName="Old Task",
            duedate=timezone.now() + timezone.timedelta(days=1),
            memo="Old memo",
        )
        self.edit_form_data = {
            "taskName": "Updated Task",
            "duedate": timezone.now() + timezone.timedelta(days=2),
            "memo": "Updated memo",
        }

    def test_edit_task_get(self):
        """Test for showing form for editting task"""
        response = self.client.get(reverse("edit_task", args=[self.task.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "snippets/editTask.html")
        self.assertContains(response, "Old Task")

    def test_edit_task_post(self):
        """Test for updating task"""
        response = self.client.post(
            reverse("edit_task", args=[self.task.slug]), self.edit_form_data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.taskName, "Updated Task")
        self.assertEqual(self.task.memo, "Updated memo")

        def test_edit_task_post_invalid(self):
            """Test that submitting invalid POST data does not update the task"""
            invalid_data = {
                "taskName": "",
                "duedate": "",
                "memo": ""
            }
            response = self.client.post(reverse("edit_task", args=[self.task.slug]), invalid_data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "snippets/editTask.html")
            self.assertFormError(response, 'form', 'taskName', 'This field is required.')