from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    description = models.TextField()
    categories = models.ForeignKey(
        "Categories",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta():
        ordering = ["year"]


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    titles = models.ForeignKey(
        Titles,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres'
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:15]