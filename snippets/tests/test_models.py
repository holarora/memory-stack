from django.test import TestCase
from snippets.models import Task, Step


class TaskModelTests(TestCase):

    def test_is_empty(self):
      """初期状態では何も登録されていないことをチェック"""
      saved_tasks = Task.objects.all()
      self.assertEqual(saved_tasks.count(), 0)

    def test_task_creation(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        Task.objects.create(
            taskName="Sample Task",
            duedate="2024-09-30 12:00:00",
            memo="This is a test task",
            slug="sample-task",
        )

        self.assertEqual(Task.objects.count(), 1)

    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        Task.objects.create(
            taskName="Task to be retrieved",
            duedate="2024-09-30 12:00:00",
            memo="This task should be retrieved",
            slug="retrieved-task",
        )

        saved_tasks = Task.objects.all()
        actual_task = saved_tasks[0]

        self.assertEqual(actual_task.taskName, "Task to be retrieved")
        self.assertEqual(actual_task.memo, "This task should be retrieved")

class StepModelTests(TestCase):
    def test_fields_task_name(self):
        task = Task(
            taskName="Sample Task",
            duedate="2024-09-30 12:00:00",
            memo="This is a test task",
            slug="sample-task",
        )
        task.save()
        step = Step(
            task=task,
            description="sample step",
        )
        step.save()

        record = Step.objects.get(id=1)
        self.assertEqual(record.task.taskName, "Sample Task")