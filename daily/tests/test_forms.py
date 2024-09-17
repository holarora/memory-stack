from django.test import TestCase

from daily.forms import EntryForm
from daily.models import Weather


class EntryFormTest(TestCase):

    def setUp(self):
        self.weather_instance = Weather.objects.create(name="Sunny", icon="path/to/icon.png")
        self.valid_data = {
            'title': 'Test Entry',
            'date': '2024-09-10',
            'content': 'Test content',
            'weather': self.weather_instance.id,
        }

    def test_missing_date(self):
        """Test that the form is invalid with missing required date field."""
        partial_data = {
            'title': 'Test Entry',
            'content': 'Test content',
            'weather': self.weather_instance.id,
        }
        form = EntryForm(data=partial_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_valid_form_with_missing_image(self):
        """Test that the form is valid with only required fields provided."""
        partial_data = {
            'title': 'Test Entry',
            'date': '2024-09-10',
            'content': 'Test content',
            'weather': self.weather_instance.id,
        }
        form = EntryForm(data=partial_data)
        print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())
        entry = form.save()
        self.assertEqual(entry.title, 'Test Entry')
        self.assertEqual(entry.date.strftime('%Y-%m-%d'), '2024-09-10')
        self.assertEqual(entry.content, 'Test content')
        self.assertEqual(entry.weather, self.weather_instance)
