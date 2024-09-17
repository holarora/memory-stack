from django.test import TestCase
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from daily.models import Weather, Entry, Image

class EntryImageModelTest(TestCase):

    def setUp(self):
        self.unique_date = timezone.now().date() + timedelta(days=1)
        self.weather = Weather.objects.create(name="Sunny")
        self.entry = Entry.objects.create(
            title="Test Entry",
            date=self.unique_date,
            content="This is a test content.",
            weather=self.weather
        )

    def test_entry_creation_with_slug(self):
        """Test that the slug is generated from the date."""
        self.assertEqual(self.entry.slug, slugify(self.entry.date))

    def test_entry_without_content_or_image(self):
        """Test that validation error is raised if neither content nor image is provided."""
        entry_no_content = Entry.objects.create(
            title="Empty Entry",
            date=timezone.now().date(),
            content="",
            weather=self.weather
        )

        entry_no_content.content = ""
        with self.assertRaises(ValidationError):
            entry_no_content.clean()

    def test_entry_with_image(self):
        """Test that entry passes validation if it has an image, even without content."""
        # Simulate an image file upload
        image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"dummy_image_content",
            content_type="image/jpeg"
        )
        image = Image.objects.create(entry=self.entry, file=image_file)

        self.entry.content = ""
        self.entry.clean()

    def test_entry_str_method(self):
        """Test the __str__ method of the Entry model."""
        expected_str = f"{self.entry.date}({self.entry.title})"
        self.assertEqual(str(self.entry), expected_str)

    def test_image_creation(self):
        """Test that an Image object can be created and associated with an entry."""
        # Simulate an image file upload
        image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"dummy_image_content",
            content_type="image/jpeg"
        )

        image = Image.objects.create(entry=self.entry, file=image_file)
        print("Uploaded file path:", image.file.path)
        print("Uploaded file name:", image.file.name)

        self.assertEqual(image.entry, self.entry)
        self.assertTrue("test_image" in image.file.name)

    def test_image_str_method(self):
        """Test the __str__ method of the Image model."""
        image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"dummy_image_content",
            content_type="image/jpeg"
        )
        image = Image.objects.create(entry=self.entry, file=image_file)

        expected_str = f"Image for entry {self.entry.date}"
        self.assertEqual(str(image), expected_str)
