from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Titles(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    categories = models.ForeignKey(
        "Categories",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
  

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Categories(models.Model):
    title = models.Choices()

    def __str__(self):
        return self.title


class Genres(models.Model):
    title = models.CharField(max_length=200)
    titles = models.ForeignKey(
        Titles,
        on_delete=models.SET_NULL,
        related_name='genres'
    )
    def __str__(self):
        return self.title
