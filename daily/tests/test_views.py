from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.core.exceptions import ValidationError

from daily.models import Weather, Entry


# class EntryCreateViewTest(TestCase):

#     def setUp(self):
#         self.weather = Weather.objects.create(name="Sunny")
#         self.url = reverse('entry_create')

#     def test_create_entry_with_valid_data(self):
#         """Test that a valid form submission creates a new Entry and redirects."""
#         response = self.client.post(self.url, {
#             'title': 'Test Entry',
#             'date': timezone.now().date(),
#             'content': 'This is a test content.',
#             'weather': self.weather.id,
#             'image': SimpleUploadedFile(
#                 name="test_image.jpg",
#                 content=b"dummy_image_content",
#                 content_type="image/jpeg"
#             )
#         })

#         self.assertEqual(Entry.objects.count(), 1)
#         entry = Entry.objects.first()
#         self.assertEqual(entry.title, 'Test Entry')
#         self.assertEqual(entry.content, 'This is a test content.')

#         self.assertTrue(entry.images.exists())
#         self.assertRedirects(response, '/daily')

#     def test_create_entry_with_invalid_data(self):
#         """Test that invalid form data does not create an Entry and returns form errors."""
#         response = self.client.post(self.url, {
#             'title': '',
#             'date': '',
#             'content': '',
#             'weather': '',
#             'image': None
#         })

#         self.assertEqual(Entry.objects.count(), 0)
#         self.assertFormError(response, 'form', 'date', 'This field is required.')


class EntryListViewTest(TestCase):

    def setUp(self):
        self.weather = Weather.objects.create(
            name="Sunny",
            icon=SimpleUploadedFile(name='test_icon.jpg', content=b'test_icon_content', content_type='image/jpeg')
        )
        self.url = reverse('all_entries')

        for i in range(15):
            Entry.objects.create(
                title=f'Entry {i}',
                date=timezone.now().date() + timezone.timedelta(days=i+1),
                content=f'Content {i}',
                weather=self.weather
            )

    def test_list_view_renders_template(self):
        """Test that the list view renders the correct template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daily/all_entries.html')

    def test_list_view_context_data(self):
        """Test that the list view context contains recent and older entries."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        context = response.context

        recent_entries = context['recent_entries']
        self.assertEqual(len(recent_entries), 10)
        self.assertEqual(recent_entries[0].title, 'Entry 14')

        older_entries = context['older_entries']
        self.assertEqual(len(older_entries), 5)
        self.assertEqual(older_entries[0].title, 'Entry 4')

    def test_weather_icon_required(self):
        """Test that an Entry cannot be created if Weather does not have an icon."""
        weather_without_icon = Weather(name="Sunny", icon=None)
        with self.assertRaises(ValidationError):
            weather_without_icon.clean()
