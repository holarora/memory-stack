from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Weather(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="天気の呼び名")
    icon = models.ImageField(
        upload_to="weather_icons/", blank=False, null=False, verbose_name="アイコン"
    )

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not self.icon:
            raise ValidationError("An icon is required for the Weather instance.")

class Entry(models.Model):
    title = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="一言があれば"
    )
    date = models.DateField(primary_key=True)
    content = models.TextField(max_length=500, null=False, verbose_name="今日の記録")
    weather = models.ForeignKey(
        Weather, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="天気"
    )
    slug = models.SlugField(
        default="", null=False, unique=True, db_index=True, editable=False
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.date)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.content and not self.images.exists():
            raise ValidationError("Either content or an image must be provided.")

    def __str__(self):
        return f"{self.date}({self.title})"


class Image(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(
        upload_to="images", blank=True, null=True, verbose_name="画像"
    )

    def __str__(self):
        return f"Image for entry {self.entry.date}"
