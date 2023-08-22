from django.db import models


class BaseCategoryGenreModel(models.Model):
    """Базовая модель для жанров и категорий."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Category(BaseCategoryGenreModel):
    """ Модель категорий. """

    def __str__(self):
        return self.name


class Genre(BaseCategoryGenreModel):
    """Модель жанров."""

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.SmallIntegerField(default=0)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre,
                                   related_name='titles')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles')

    def __str__(self):
        return self.name
