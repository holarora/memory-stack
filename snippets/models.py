from django.db import models
from django.utils.text import slugify


# Create your models here.
class Task(models.Model):
    taskName = models.CharField(max_length=20)
    duedate = models.DateTimeField(null=True)
    memo = models.TextField(null=True, max_length=200, verbose_name="メモの追加")
    slug = models.SlugField(
        default="", null=False, unique=True, db_index=True, editable=False
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.taskName)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.taskName}({self.duedate})"


class Step(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField(
        null=True, max_length=200, verbose_name="ステップの追加"
    )

    def __str__(self):
        return self.description
