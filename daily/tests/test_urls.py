from django.test import TestCase
from django.urls import reverse, resolve
from ..views import EntryListView


class TestUrls(TestCase):

    def test_allentries_url_resolves(self):
        view = resolve('/daily/')
        self.assertEqual(view.func.view_class, EntryListView)
