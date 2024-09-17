from django.test import TestCase
from django.urls import reverse, resolve
from snippets import views


class TestUrls(TestCase):

    def test_alltasks_url_resolves(self):
        url = reverse("alltasks")
        self.assertEqual(resolve(url).func, views.alltasks)

    def test_onetask_url_resolves(self):
        url = reverse("onetask", args=["sample-task"])
        self.assertEqual(resolve(url).func, views.onetask)

    def test_edit_task_url_resolves(self):
        url = reverse("edit_task", args=["sample-task"])
        self.assertEqual(resolve(url).func, views.edit_task)
