from django.db import models

from .validators import validate_title_year, validate_score_or_rating


class BaseCategoryGenreModel(models.Model):
    """Базовая модель для жанров и категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True


class Category(BaseCategoryGenreModel):
    """ Модель категорий. """

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genre(BaseCategoryGenreModel):
    """Модель жанров."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=(validate_title_year,),
        verbose_name='Год выпуска'
    )
    rating = models.SmallIntegerField(
        default=models.SET_NULL,
        null=True,
        validators=(validate_score_or_rating,),
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'


class GenreTitle(models.Model):
    """Вспомогательная модель жанров и произведений"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('title', 'genre'),
            name='genre_title_uniq'),
        )
